# Created: 2026-04-10 11:30:00
# Last Modified: 2026-04-10 11:30:00
# Description: Unit tests for compute_moment_maps() in spectral_fitting_lib.py.
#   Tests moment 0/1/2 computation against analytic Gaussian profiles and
#   verifies SNR masking behaviour. Run before using moment maps in science
#   analysis. Unlike the pipeline script (run_moment_maps.py), this only
#   validates the library function on synthetic data.
# Last Edit: Initial creation.

"""
Tests for spectral_fitting_lib.compute_moment_maps().
Run with: python3 test_moment_maps.py
"""

import sys
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from Analysis.SpectralAnalysis.spectral_fitting_lib import (
    compute_moment_maps,
    gaussian_1d,
)


def make_synthetic_cube(n_chan=64, n_y=8, n_x=8,
                        amp=5.0, v0=0.0, sigma=5.0, noise=0.1):
    """
    Create a synthetic cube with identical Gaussian profiles at every pixel.
    Used for analytic moment comparisons.
    """
    v = np.linspace(-50.0, 50.0, n_chan)
    spectrum = gaussian_1d(v, amp, v0, sigma)
    cube = np.tile(spectrum[:, np.newaxis, np.newaxis],
                   (1, n_y, n_x))
    rng = np.random.default_rng(seed=42)
    cube = cube + rng.normal(0, noise, cube.shape)
    return cube, v


def test_moment0_analytic():
    """Moment 0 should equal amp × sigma × sqrt(2π) within noise tolerance."""
    cube, v = make_synthetic_cube(amp=5.0, sigma=5.0, noise=0.0)
    dv = np.abs(v[1] - v[0])
    mom0, _, _ = compute_moment_maps(cube, v, channel_width_kms=dv)
    expected = 5.0 * 5.0 * np.sqrt(2 * np.pi)
    assert np.allclose(mom0, expected, rtol=0.01), (
        f"Moment 0 error: got {mom0.mean():.3f}, expected {expected:.3f}")
    print(f"  PASS  moment 0: {mom0.mean():.3f} K km/s (expected {expected:.3f})")


def test_moment1_analytic():
    """Moment 1 should equal the Gaussian centre velocity."""
    cube, v = make_synthetic_cube(v0=10.0, noise=0.0)
    _, mom1, _ = compute_moment_maps(cube, v)
    assert np.allclose(mom1, 10.0, atol=0.1), (
        f"Moment 1 error: got {mom1.mean():.3f}, expected 10.0")
    print(f"  PASS  moment 1: {mom1.mean():.3f} km/s (expected 10.0)")


def test_moment2_analytic():
    """Moment 2 should equal the Gaussian sigma."""
    cube, v = make_synthetic_cube(sigma=8.0, noise=0.0)
    _, _, mom2 = compute_moment_maps(cube, v)
    assert np.allclose(mom2, 8.0, rtol=0.02), (
        f"Moment 2 error: got {mom2.mean():.3f}, expected 8.0")
    print(f"  PASS  moment 2: {mom2.mean():.3f} km/s (expected 8.0)")


def test_snr_mask_zeros_out_channels():
    """Applying a mask that zeros all channels should give moment 0 = 0."""
    cube, v = make_synthetic_cube()
    zero_mask = np.zeros_like(cube, dtype=bool)
    mom0, mom1, mom2 = compute_moment_maps(cube, v, snr_mask=zero_mask)
    assert np.all(mom0 == 0.0), "Moment 0 should be 0 when all channels masked"
    assert np.all(np.isnan(mom1)), "Moment 1 should be NaN when all channels masked"
    print("  PASS  SNR masking: all-zero mask produces mom0=0, mom1=NaN")


if __name__ == "__main__":
    print("Running moment map tests...")
    test_moment0_analytic()
    test_moment1_analytic()
    test_moment2_analytic()
    test_snr_mask_zeros_out_channels()
    print("\nAll tests passed.")
