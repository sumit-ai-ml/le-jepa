"""Independent derivation of the le-jepa four-scene example and a partial-observability extension.

Self-contained numpy; cross-checks against the authors' prh.theory where noted.
"""
import sys
import numpy as np

np.set_printoptions(precision=4, suppress=True)
import os
AUTH = os.environ.get("PRH_PROOF", "prh-proof")  # path to a checkout of galilai-group/prh-proof
import importlib.util
_spec = importlib.util.spec_from_file_location("theory", AUTH + "/prh/theory.py")
th = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(th)  # authors' numpy-only module, loaded without the torch-dependent package __init__

rng = np.random.default_rng(0)


def spectrum(pi):
    p = pi.sum(1)
    S = pi / np.sqrt(np.outer(p, p))
    mu, U = np.linalg.eigh(S)
    o = np.argsort(mu)[::-1]
    return mu[o], U[:, o] / np.sqrt(p)[:, None]  # eigenfunctions, orthonormal in L2(p)


def whiten(h, p):
    h = h - p @ h
    C = h.T @ (p[:, None] * h)
    w, V = np.linalg.eigh(C)
    return h @ V @ np.diag(w ** -0.5) @ V.T


def loss(h, pi):
    d = h[:, None, :] - h[None, :, :]
    return float((pi * (d ** 2).sum(-1)).sum())


def best_rot_mse(h1, h2, p):
    """min over orthogonal Q of E_p ||h1 - h2 Q^T||^2 (squared distance, not its root)."""
    M = h1.T @ (p[:, None] * h2)
    s = np.linalg.svd(M, compute_uv=False)
    return float(h1.shape[1] + h2.shape[1] - 2 * s.sum())


print("=" * 78)
print("(a) four equally likely scenes, same-scene positives: pi = diag(p)")
p = np.full(4, 0.25)
pi = np.diag(p)
mu, phi = spectrum(pi)
print("eigenvalues of S = D^-1/2 pi D^-1/2:", mu)
print("gap mu_k - mu_{k+1}: k=1:", mu[1] - mu[2], " k=2:", mu[2] - mu[3], " k=3: (mu_4 undefined -> treated as -inf by authors)")
h1 = np.array([-1., -1., 1., 1.])[:, None]
h2 = np.array([-1., 1., -1., 1.])[:, None]
for name, h in (("h1", h1), ("h2", h2)):
    print(f"{name}: mean {p @ h[:, 0]:+.3f}, variance {p @ (h[:, 0] ** 2):.3f}, JEPA loss {loss(h, pi):.3f}")
corr = float(p @ (h1[:, 0] * h2[:, 0]))
print("corr(h1,h2) =", corr, " -> whitened scalars: min_q E(h1 - q h2)^2 = 2 - 2|corr| =", 2 - 2 * abs(corr))
print("direct: q=+1:", float(p @ ((h1 - h2) ** 2).sum(1)), " q=-1:", float(p @ ((h1 + h2) ** 2).sum(1)))
print("authors' rotation_distance (root of the MSE):", th.rotation_distance(h1, h2, p), " -> squared:", th.rotation_distance(h1, h2, p) ** 2)
print("authors' spectral_solution(pi, 1) is some unit vector in the 3-dim tied eigenspace:", th.spectral_solution(pi, 1)[:, 0])
print("-- k = 3 = |Z| - 1: any two whitened encoders are rotations of each other --")
d = [best_rot_mse(whiten(rng.standard_normal((4, 3)), p), whiten(rng.standard_normal((4, 3)), p), p) for _ in range(20)]
print("max over 20 random pairs of min-rotation squared distance (k=3):", max(d))
d1 = [best_rot_mse(whiten(rng.standard_normal((4, 1)), p), whiten(rng.standard_normal((4, 1)), p), p) for _ in range(2000)]
print("k = 1: random whitened pairs: squared distance ranges over [%.3f, %.3f] (any value in [0, 2])" % (min(d1), max(d1)))
print("-- Thm-3 version: several observations per scene (nuisance), good views --")
q = np.array([0.5, 0.3, 0.2])
W = th.good_views(pi, q)
muW, _ = spectrum(W)
print("good_views(pi, q) eigenvalues:", muW, " (1 x4 then 0: same tie among the scene directions)")

print("=" * 78)
print("(c) structured 2x2 factor world: shape slow (stay .95), colour fast (stay .6)")
A = np.array([[.95, .05], [.05, .95]])
B = np.array([[.6, .4], [.4, .6]])
P = np.kron(A, B)                      # z = (shape, colour), index 2*shape + colour
pi_s = np.diag(p) @ P                  # symmetric: uniform marginal and symmetric A, B
assert np.allclose(pi_s, pi_s.T) and np.allclose(pi_s.sum(1), p)
mu_s, phi_s = spectrum(pi_s)
print("eigenvalues:", mu_s, " (products of {1,.9} and {1,.2})")
print("k=1 eigenfunction (shape indicator up to sign):", phi_s[:, 1])
print("k=2 eigenfunction (colour):", phi_s[:, 2])
print("gap at k=1:", mu_s[1] - mu_s[2], " at k=2:", mu_s[2] - mu_s[3])
g1 = np.array([7, 2, 9, 4])            # injective renderings into observation spaces of size 10 and 30
g2 = np.array([21, 3, 17, 8])
for k in (1, 2):
    s1, f1 = th.observed_solution(th.render(pi_s, g1, 10), k)
    s2, f2 = th.observed_solution(th.render(pi_s, g2, 30), k)
    e1, e2 = f1[np.searchsorted(s1, g1)], f2[np.searchsorted(s2, g2)]
    print(f"Thm 1, injective renderings, k={k}: rotation distance {th.rotation_distance(e1, e2, p):.2e}")
s1, f1 = th.observed_solution(th.render(pi, g1, 10), 1)
s2, f2 = th.observed_solution(th.render(pi, g2, 30), 1)
e1, e2 = f1[np.searchsorted(s1, g1)], f2[np.searchsorted(s2, g2)]
print(f"identity kernel, injective renderings, k=1: rotation distance {th.rotation_distance(e1, e2, p):.3f} (arbitrary; depends on eigh tie-breaking)")
print("Davis-Kahan bound pi_s vs itself (k=1):", th.davis_kahan_bound(pi_s, pi_s, 1), "; identity kernel gap:", mu[1] - mu[2], "-> bound undefined/inf")

print("=" * 78)
print("(d) PARTIAL OBSERVABILITY: modality 1 sees the full state, modality 2 sees a coarsening g2")


def lift(pi, g, n_obs):
    """Coarse observation kernel pi2(a,a') = sum over fibres, and its lift back to Z with marginal p."""
    p = pi.sum(1)
    M = np.eye(n_obs)[g]                       # [n, n_obs] fibre indicator
    pi2 = M.T @ pi @ M                         # law of (g(z), g(z'))
    p2 = pi2.sum(1)
    lifted = pi2[np.ix_(g, g)] * np.outer(p / p2[g], p / p2[g])
    assert np.allclose(lifted.sum(1), p)
    return pi2, lifted


def report_partial(pi, g, n_obs, label):
    p = pi.sum(1)
    pi2, lifted = lift(pi, g, n_obs)
    mu1, phi1 = spectrum(pi)
    mu2, phi2 = spectrum(pi2)
    muL, phiL = spectrum(lifted)
    print(f"--- {label}: g2 = {g}")
    print("  full kernel eigenvalues:", mu1)
    print("  coarse kernel eigenvalues:", mu2, "  lifted kernel eigenvalues:", muL, "(coarse spectrum + zeros)")
    kmax2 = n_obs - 1
    for k in (1, 2):
        f1 = th.spectral_solution(pi, k)                      # full-state JEPA on Z
        f2_obs = th.spectral_solution(pi2, min(k, kmax2))     # coarse JEPA on its observations
        f2 = f2_obs[g]                                        # pulled back to Z (constant on fibres)
        fL = th.spectral_solution(lifted, k)                  # lifted kernel solution on Z
        shared = phi1[:, 1:k + 1]                             # top-k eigenfunctions of pi
        meas = shared - (np.eye(n_obs)[g] @ (np.eye(n_obs)[g].T @ (p[:, None] * shared)) / pi2.sum(1)[g][:, None])
        # 'meas' = component of the top-k eigenfunctions NOT measurable w.r.t. the coarse partition
        private_mass = float((p @ (meas ** 2)).sum())
        dist = best_rot_mse(f1, f2, p) if f2.shape[1] == f1.shape[1] else float("nan")
        # alignment restricted to the coarse-measurable part: principal angles between span(f2) and span(f1)
        Q1 = np.linalg.qr(np.sqrt(p)[:, None] * f1)[0]
        Q2 = np.linalg.qr(np.sqrt(p)[:, None] * f2)[0]
        cosines = np.linalg.svd(Q1.T @ Q2, compute_uv=False)
        dk = th.davis_kahan_bound(pi, lifted, k) if muL[k] - muL[k + 1] > 1e-9 else float("inf")
        print(f"  k={k}: coarse JEPA has {f2.shape[1]} usable dim(s) (max {kmax2}); squared min-rotation distance full vs coarse (same k): {dist:.3f};"
              f" principal cosines span(full) vs span(coarse pulled back): {cosines};"
              f" mass of full top-k eigenfunctions outside the coarse partition: {private_mass:.3f};"
              f" lifted-kernel solution == coarse solution? {np.allclose(abs(np.linalg.svd((np.sqrt(p)[:, None]*fL).T @ (np.sqrt(p)[:, None]*f2), compute_uv=False)).sum(), f2.shape[1], atol=1e-8)};"
              f" Thm-2 bound (full vs lifted, k={k}): {dk:.3f}")


shape_only = np.array([0, 0, 1, 1])
colour_only = np.array([0, 1, 0, 1])
report_partial(pi_s, shape_only, 2, "structured world, modality 2 observes SHAPE (the slow, top eigenfunction)")
report_partial(pi_s, colour_only, 2, "structured world, modality 2 observes COLOUR (the fast factor)")
report_partial(pi, shape_only, 2, "identity kernel (same-scene positives only), modality 2 observes shape")
# a non-factor coarsening of a random structured world
n = 6
Kr = rng.random((n, n)); Kr = Kr + Kr.T + 3 * np.eye(n)
pr = rng.dirichlet(np.ones(n))
pi_r = th.with_marginal(Kr, pr)
g_r = np.array([0, 0, 1, 1, 1, 2])
report_partial(pi_r, g_r, 3, "random 6-state world, arbitrary 3-cell coarsening")
print("=" * 78)
print("Interpretation check: the lifted kernel is a legitimate positive-pair kernel on the full world (marginal p),")
print("so Thm 2 (Davis-Kahan) bounds the full-vs-coarse misalignment by the mismatch ||T_pi - T_lift|| over the gap;")
print("the eigenvalue-0 eigenspace of the lifted kernel is exactly the subspace invisible to modality 2 (private to modality 1).")
