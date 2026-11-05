"""Illustrate why same-scene positives alone do not identify common geometry.

This checks a finite, whitened squared-loss example. It does not reproduce
LeJEPA training or contradict a theorem that assumes uniqueness up to rotation.
Run with Python 3; no third-party packages are required.
"""

import json
from math import isclose


def mean(values):
    return sum(values) / len(values)


def variance(values):
    center = mean(values)
    return mean([(value - center) ** 2 for value in values])


def same_scene_loss(encoding):
    # The two independently sampled observations share scene identity.
    # These encoders ignore their nuisance and return the same scene value.
    return mean([(encoding[scene] - encoding[scene]) ** 2
                 for scene in range(len(encoding))])


def main():
    first = [-1.0, -1.0, 1.0, 1.0]
    second = [-1.0, 1.0, -1.0, 1.0]
    alignment_errors = {
        str(sign): mean([(left - sign * right) ** 2
                         for left, right in zip(first, second)])
        for sign in (-1, 1)
    }
    result = {
        "world": "four equally likely scenes; same-scene positives only",
        "means": [mean(first), mean(second)],
        "variances": [variance(first), variance(second)],
        "same_scene_losses": [same_scene_loss(first), same_scene_loss(second)],
        "orthogonal_alignment_MSE_by_sign": alignment_errors,
        "best_orthogonal_alignment_MSE": min(alignment_errors.values()),
        "normalized_scene_kernel_eigenvalues": [1, 1, 1, 1],
        "eigengap_after_first_nonconstant_eigenvalue": 0,
        "interpretation": "Uniqueness fails; the stated theorem is not refuted.",
    }
    assert all(isclose(value, 0.0) for value in result["means"])
    assert all(isclose(value, 1.0) for value in result["variances"])
    assert all(isclose(value, 0.0) for value in result["same_scene_losses"])
    assert isclose(result["best_orthogonal_alignment_MSE"], 2.0)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
