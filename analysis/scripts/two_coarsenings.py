"""Two partially observed modalities: do independently trained spectral JEPAs agree on the SHARED factor?

World: three binary factors (f1, f2, f3). Modality A observes (f1, f2); modality B observes (f2, f3).
Shared information = f2. Kernel: product of 2-state Markov kernels (independent factors) or a coupled variant.
Also checks the authors' Thm. 3 machinery with roles reassigned: state := shared factor, private factors := nuisance.
"""
import importlib.util
import itertools
import numpy as np

np.set_printoptions(precision=4, suppress=True)
import os
AUTH = os.environ.get("PRH_PROOF", "prh-proof")  # path to a checkout of galilai-group/prh-proof
_spec = importlib.util.spec_from_file_location("theory", AUTH + "/prh/theory.py")
th = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(th)
rng = np.random.default_rng(1)


def two_state(stay):
    return np.array([[stay, 1 - stay], [1 - stay, stay]])


def spectrum(pi):
    p = pi.sum(1)
    S = pi / np.sqrt(np.outer(p, p))
    mu, U = np.linalg.eigh(S)
    o = np.argsort(mu)[::-1]
    return mu[o], U[:, o] / np.sqrt(p)[:, None]


def coarse_and_lift(pi, g, n_obs):
    p = pi.sum(1)
    M = np.eye(n_obs)[g]
    pi2 = M.T @ pi @ M
    p2 = pi2.sum(1)
    return pi2, pi2[np.ix_(g, g)] * np.outer(p / p2[g], p / p2[g])


def principal_cosines(f, g, p):
    Qf = np.linalg.qr(np.sqrt(p)[:, None] * f)[0]
    Qg = np.linalg.qr(np.sqrt(p)[:, None] * g)[0]
    return np.linalg.svd(Qf.T @ Qg, compute_uv=False)


def run(pi, label):
    p = pi.sum(1)
    states = list(itertools.product((0, 1), repeat=3))           # z index = 4 f1 + 2 f2 + f3
    gA = np.array([2 * f1 + f2 for f1, f2, f3 in states])       # modality A sees (f1, f2): 4 observations
    gB = np.array([2 * f2 + f3 for f1, f2, f3 in states])       # modality B sees (f2, f3): 4 observations
    shared = np.array([1.0 if f2 else -1.0 for f1, f2, f3 in states])[:, None]  # f2 indicator (centred, unit var)
    mu, phi = spectrum(pi)
    print("=" * 78)
    print(label)
    print("full-world eigenvalues:", mu)
    piA, liftA = coarse_and_lift(pi, gA, 4)
    piB, liftB = coarse_and_lift(pi, gB, 4)
    print("modality A coarse eigenvalues:", spectrum(piA)[0], " modality B:", spectrum(piB)[0])
    for k in (1, 2, 3):
        fA = th.spectral_solution(piA, k)[gA]                     # A's encoder pulled back to Z
        fB = th.spectral_solution(piB, k)[gB]
        dAB = th.rotation_distance(fA, fB, p) ** 2                 # squared min-rotation distance, in [0, 2k]
        cos_shared_A = principal_cosines(fA, shared, p)[0]
        cos_shared_B = principal_cosines(fB, shared, p)[0]
        cosAB = principal_cosines(fA, fB, p)
        # Thm 2 between the two lifted kernels (both legitimate kernels on Z with marginal p)
        muB = spectrum(liftB)[0]
        gapB = muB[k] - (muB[k + 1] if k + 1 < len(muB) else -np.inf)
        dk = th.davis_kahan_bound(liftA, liftB, k) if gapB > 1e-9 else np.inf
        # shared-subspace alignment: project both encoders on the f2 direction and compare signs/scales
        print(f" k={k}: squared min-rotation distance A vs B = {dAB:.3f} (max {2*k}); principal cosines A vs B = {cosAB};"
              f" |cos| of span(A) with the shared f2 direction = {cos_shared_A:.3f}, span(B) = {cos_shared_B:.3f}; Thm-2 bound(liftA, liftB) = {dk:.3f}")
    # Thm 3 with roles reassigned: state = f2 (shared), nuisance of A = f1, of B = f3
    # A's observation index 2 f1 + f2 -> state-major layout (f2 * 2 + f1) is needed by state_explained_covariance
    pA_state = np.array([0.5, 0.5])
    for name, g, nuis in (("A", gA, 0), ("B", gB, 2)):
        pi_obs, _ = coarse_and_lift(pi, g, 4)
        for k in (1, 2):
            f_obs = th.spectral_solution(pi_obs, k)              # [4, k] on observations (index 2 x + y)
            # reorder observations to (state f2, nuisance) layout: obs index for A is 2 f1 + f2, for B is 2 f2 + f3
            if name == "A":
                order = [2 * n + s for s in (0, 1) for n in (0, 1)]   # state f2 outer, nuisance f1 inner
            else:
                order = [2 * s + n for s in (0, 1) for n in (0, 1)]   # state f2 outer, nuisance f3 inner
            f_sn = f_obs[order]
            q = np.array([0.5, 0.5])
            bound = th.nuisance_bound(f_sn, pA_state, q)
            c = np.linalg.eigvalsh(th.state_explained_covariance(f_sn, pA_state, q))
            print(f"  Thm 3 reassigned, modality {name}, k={k}: state(f2)-explained eigenvalues {np.sort(c)[::-1]}, lower bound on cross-modal error vs ANY other modality = {bound:.3f}")


# independent factors: f1 slow, f2 medium, f3 fast -> product kernel
P = np.kron(np.kron(two_state(0.95), two_state(0.8)), two_state(0.6))
p = np.full(8, 1 / 8)
pi_prod = np.diag(p) @ P
run(pi_prod, "PRODUCT world: f1 stay .95 (A-private), f2 stay .80 (shared), f3 stay .60 (B-private)")
P = np.kron(np.kron(two_state(0.8), two_state(0.95)), two_state(0.6))
run(np.diag(p) @ P, "PRODUCT world: shared factor f2 is the SLOWEST (stay .95); f1 .80, f3 .60")
P = np.kron(np.kron(two_state(0.95), two_state(0.6)), two_state(0.8))
run(np.diag(p) @ P, "PRODUCT world: shared factor f2 is the FASTEST (stay .60); f1 .95, f3 .80")
# coupled world: a random symmetric perturbation that couples the factors (non-product), with uniform marginal
K = np.kron(np.kron(two_state(0.95), two_state(0.8)), two_state(0.6))
R = rng.random((8, 8)); R = (R + R.T) / 2
pi_coupled = th.with_marginal(K + 0.6 * R, p)
run(pi_coupled, "COUPLED world: product kernel plus a random symmetric coupling (factors no longer independent)")
# same-scene positives only (identity kernel): the repository's four-scene situation with three factors
run(np.diag(p), "IDENTITY kernel (same-scene positives only)")
