# Created: 2026-04-01 09:15:00
# Last Modified: 2026-04-15 14:32:00
# Description: Library of spectral line fitting functions for HI 21 cm profiles
#   in Local Group dwarf galaxy cubes. Wraps GaussPy+ decomposition and provides
#   utilities for multi-component Gaussian fitting, moment computation, and
#   quality filtering. Unlike gaussdecomp_lib.py (which handles GaussPy+ training
#   and parameter sweeps), this file handles the downstream fitting and validation.
# Last Edit: Added get_quality_mask() function to filter by chi2_red and SNR.

"""
spectral_fitting_lib.py — HI spectral analysis utilities.

Functions
---------
fit_single_spectrum(spectrum, velocity_axis, n_components, p0)
    Fit n Gaussian components to a single HI spectrum.

compute_moment_maps(cube, velocity_axis, snr_mask, order)
    Compute moment 0, 1, 2 maps from a masked spectral cube.

get_quality_mask(chi2_red, snr_mom0, chi2_max, snr_min)
    Return a boolean mask of pixels passing quality thresholds.

estimate_noise_rms(spectrum, line_free_channels)
    Estimate per-spectrum RMS noise from line-free channels.
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import warnings


# ─── Gaussian model ──────────────────────────────────────────────────────────

def gaussian_1d(v, amp, v0, sigma):
    """Single Gaussian in velocity space. Returns brightness temperature [K]."""
    return amp * np.exp(-0.5 * ((v - v0) / sigma) ** 2)


def multi_gaussian(v, *params):
    """
    Sum of n Gaussian components.
    params: flat array [amp1, v0_1, sigma1, amp2, v0_2, sigma2, ...]
    """
    if len(params) % 3 != 0:
        raise ValueError("params must have 3 × n_components entries")
    result = np.zeros_like(v, dtype=float)
    for i in range(0, len(params), 3):
        result += gaussian_1d(v, params[i], params[i + 1], params[i + 2])
    return result


# ─── Fitting ─────────────────────────────────────────────────────────────────

def fit_single_spectrum(spectrum, velocity_axis, n_components, p0=None,
                        amp_bounds=(0, np.inf), sigma_bounds=(0.5, 100.0)):
    """
    Fit n_components Gaussians to a single HI spectrum via scipy curve_fit.

    Parameters
    ----------
    spectrum : 1D array
        Brightness temperature [K] as a function of channel.
    velocity_axis : 1D array
        Velocity values [km/s] for each channel.
    n_components : int
        Number of Gaussian components to fit.
    p0 : array-like or None
        Initial parameter guess: [amp, v0, sigma] × n_components.
        If None, peaks are auto-detected.
    amp_bounds : tuple
        (min, max) amplitude bounds [K].
    sigma_bounds : tuple
        (min, max) sigma bounds [km/s].

    Returns
    -------
    popt : 1D array
        Best-fit parameters [amp, v0, sigma] × n_components.
    pcov : 2D array
        Parameter covariance matrix.
    chi2_red : float
        Reduced chi-squared (requires noise estimate; set to NaN here,
        compute with estimate_noise_rms externally).
    success : bool
        True if curve_fit converged without raising RuntimeError.
    """
    v = np.asarray(velocity_axis, dtype=float)
    s = np.asarray(spectrum, dtype=float)

    if p0 is None:
        p0 = _auto_initial_params(s, v, n_components)

    # Build bounds for all components
    lo = [amp_bounds[0], v.min(), sigma_bounds[0]] * n_components
    hi = [amp_bounds[1], v.max(), sigma_bounds[1]] * n_components

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            popt, pcov = curve_fit(multi_gaussian, v, s, p0=p0,
                                   bounds=(lo, hi), maxfev=5000)
        success = True
    except RuntimeError:
        popt = np.full(3 * n_components, np.nan)
        pcov = np.full((3 * n_components, 3 * n_components), np.nan)
        success = False

    return popt, pcov, np.nan, success


def _auto_initial_params(spectrum, velocity_axis, n_components):
    """
    Auto-detect initial parameters from spectrum peaks.
    Falls back to evenly-spaced guesses if fewer than n_components peaks found.
    """
    peaks, props = find_peaks(spectrum, height=0.01 * spectrum.max(),
                              distance=max(1, len(spectrum) // (2 * n_components)))
    peak_amps = spectrum[peaks]
    peak_vels = velocity_axis[peaks]

    # Sort by amplitude, take top n_components
    order = np.argsort(peak_amps)[::-1]
    peaks_use = order[:n_components]

    p0 = []
    for i in range(n_components):
        if i < len(peaks_use):
            amp = peak_amps[peaks_use[i]]
            v0 = peak_vels[peaks_use[i]]
        else:
            amp = spectrum.max() * 0.1
            v0 = velocity_axis[len(velocity_axis) // 2]
        sigma = 5.0  # km/s initial guess
        p0.extend([amp, v0, sigma])

    return p0


# ─── Moment maps ─────────────────────────────────────────────────────────────

def compute_moment_maps(cube, velocity_axis, snr_mask=None, channel_width_kms=None):
    """
    Compute moment 0, 1, and 2 maps from a spectral cube.

    Parameters
    ----------
    cube : 3D array, shape (n_channels, n_y, n_x)
        Brightness temperature cube [K].
    velocity_axis : 1D array, shape (n_channels,)
        Velocity values [km/s].
    snr_mask : 3D bool array or None
        True where signal is significant (applied per voxel). If None,
        all voxels are included.
    channel_width_kms : float or None
        Channel width for moment 0 integration [km/s].
        If None, inferred from velocity_axis spacing.

    Returns
    -------
    mom0 : 2D array   — integrated intensity [K km/s]
    mom1 : 2D array   — intensity-weighted mean velocity [km/s]
    mom2 : 2D array   — intensity-weighted velocity dispersion [km/s]
    """
    v = np.asarray(velocity_axis, dtype=float)
    dv = np.abs(np.median(np.diff(v))) if channel_width_kms is None else channel_width_kms
    c = np.asarray(cube, dtype=float)

    if snr_mask is not None:
        c = np.where(snr_mask, c, 0.0)

    # Moment 0: integral of T dv
    mom0 = np.nansum(c, axis=0) * dv

    # Moment 1: intensity-weighted mean velocity
    v_3d = v[:, np.newaxis, np.newaxis] * np.ones_like(c)
    with np.errstate(invalid='ignore', divide='ignore'):
        mom1 = np.nansum(c * v_3d, axis=0) / np.nansum(c, axis=0)
    mom1[mom0 == 0] = np.nan

    # Moment 2: intensity-weighted RMS velocity dispersion
    with np.errstate(invalid='ignore', divide='ignore'):
        mom2 = np.sqrt(
            np.nansum(c * (v_3d - mom1[np.newaxis, :, :]) ** 2, axis=0)
            / np.nansum(c, axis=0)
        )
    mom2[mom0 == 0] = np.nan

    return mom0, mom1, mom2


# ─── Quality masking ─────────────────────────────────────────────────────────

def get_quality_mask(chi2_red, snr_mom0, chi2_max=10.0, snr_min=3.0):
    """
    Boolean mask of pixels passing fit quality thresholds.

    Parameters
    ----------
    chi2_red : 2D array
        Per-pixel reduced chi-squared from spectral fitting.
    snr_mom0 : 2D array
        Per-pixel moment-0 signal-to-noise ratio.
    chi2_max : float
        Maximum acceptable reduced chi-squared.
    snr_min : float
        Minimum acceptable SNR.

    Returns
    -------
    mask : 2D bool array
        True where the pixel passes both thresholds.
    """
    mask = (np.isfinite(chi2_red) & (chi2_red <= chi2_max) &
            np.isfinite(snr_mom0) & (snr_mom0 >= snr_min))
    return mask


# ─── Noise estimation ─────────────────────────────────────────────────────────

def estimate_noise_rms(spectrum, line_free_channels):
    """
    Estimate per-spectrum RMS noise from designated line-free channels.

    Parameters
    ----------
    spectrum : 1D array
        Brightness temperature spectrum [K].
    line_free_channels : array-like of int
        Channel indices known to be line-free (off-line channels).

    Returns
    -------
    rms : float
        RMS noise estimate [K].
    """
    off_line = np.asarray(spectrum)[line_free_channels]
    return float(np.sqrt(np.nanmean(off_line ** 2)))
