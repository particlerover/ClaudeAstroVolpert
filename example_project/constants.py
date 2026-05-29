# Created: 2026-03-15 10:00:00
# Last Modified: 2026-05-10 14:00:00
# Description: Centralised physical and project-specific constants for the Local
#   Group HI Survey. Import this module in every analysis script. Change a value
#   here and it propagates to all scripts. All entries include units and citation.
# Last Edit: Added per-target PC_PER_ARCSEC and BEAM_FWHM_PC lookup dicts.

"""
constants.py — Local Group HI Survey constants.

Usage
-----
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import constants as C

    beam_pc = C.BEAM_FWHM_PC["LMC"]
    n_hi_cm2 = C.X_HI * w_hi_kkms
"""

import numpy as np


# =============================================================================
# 1. FUNDAMENTAL PHYSICAL CONSTANTS (CGS)
# =============================================================================

PC_CM = 3.085677581e18
"""Parsec in centimetres [cm pc⁻¹]."""

K_B_CGS = 1.380649e-16
"""Boltzmann constant [erg K⁻¹]. CODATA 2018."""

M_H_G = 1.6735575e-24
"""Hydrogen atom mass [g]. CODATA 2018."""

M_SUN_G = 1.98892e33
"""Solar mass [g]. IAU 2015 nominal."""

C_LIGHT_CGS = 2.99792458e10
"""Speed of light [cm s⁻¹]. Exact."""

H_PLANCK_CGS = 6.62607015e-27
"""Planck constant [erg s]. CODATA 2018."""

ARCSEC_PER_RAD = 206264.806247
"""Arcseconds per radian."""

T_CMB_K = 2.7255
"""CMB temperature [K]. Fixsen (2009, ApJ 707, 916)."""


# =============================================================================
# 2. HI 21 CM LINE PROPERTIES
# =============================================================================

NU_HI_HZ = 1.42040575177e9
"""HI 21 cm rest frequency [Hz] = 1420.40575177 MHz. NIST."""

A_UL_HI_INV_S = 2.8843e-15
"""HI 21 cm Einstein A coefficient [s⁻¹]."""

X_HI = 1.82e18
"""
HI column density conversion factor [cm⁻² (K km/s)⁻¹].

In the optically thin limit:
    N_HI [cm⁻²] = X_HI × W_HI [K km/s]
where W_HI is the integrated HI brightness temperature.

Value: 1.82 × 10¹⁸ cm⁻² (K km/s)⁻¹.
Derived from the HI Einstein A coefficient and statistical weights.
Standard value; see Dickey & Lockman (1990, ARA&A 28, 215) for derivation.

WARNING: breaks down when HI becomes optically thick (tau > ~1), which
occurs at N_HI > ~10²¹ cm⁻² depending on spin temperature.
"""


# =============================================================================
# 3. TARGET DISTANCES
# =============================================================================

DISTANCE_KPC = {
    "LMC":    50.0,    # Pietrzyński et al. (2019, Nature 567, 200); TRGB
    "SMC":    62.0,    # Graczyk et al. (2014, ApJ 780, 59); eclipsing binary
    "WLM":   933.0,    # McConnachie (2012, AJ 144, 4); RR Lyrae/TRGB
    "NGC6822": 490.0,  # McConnachie (2012); Cepheids
    "IC10":   740.0,   # McConnachie (2012); TRGB
}
"""
Distances to all survey targets [kpc].
Primary references in-line; all from the McConnachie (2012) compilation
or more recent distance-ladder measurements.
"""

PC_PER_ARCSEC = {
    k: v * 1e3 / ARCSEC_PER_RAD for k, v in DISTANCE_KPC.items()
}
"""Physical scale at each target [pc arcsec⁻¹]."""


# =============================================================================
# 4. BEAM AND PIXEL PROPERTIES
# =============================================================================

# VLA D-array at 1.4 GHz — all targets observed at the same nominal resolution
VLA_D_BEAM_FWHM_ARCSEC = 45.0
"""
VLA D-array synthesised beam FWHM at 1.4 GHz [arcsec].
The actual FWHM varies ~40–50" depending on declination and hour angle;
45" is the adopted round value for parameter estimates and OOM checks.
Check the actual BMAJ from each cube header for science-level calculations.
"""

BEAM_FWHM_PC = {
    k: VLA_D_BEAM_FWHM_ARCSEC * PC_PER_ARCSEC[k]
    for k in DISTANCE_KPC
}
"""Physical beam FWHM at each target distance [pc]."""

PIX_SCALE_ARCSEC = 15.0
"""
Pixel scale of the analysis cubes [arcsec pixel⁻¹].
Set to one-third of the nominal beam FWHM (45"/3 = 15") to ensure
adequate spatial sampling of the beam. This is the common grid for
all targets after regridding from the native VLA cube grid.
"""

CHANNEL_WIDTH_KMS = 1.0
"""
Spectral channel width of the analysis cubes [km s⁻¹].
Adopted to match the LMC/SMC VLA D-array native resolution and
provide ~5 channels across a typical HI linewidth (~5 km/s CNM).
"""


# =============================================================================
# 5. QUALITY THRESHOLDS
# =============================================================================

SNR_MIN = 3.0
"""Minimum moment-0 SNR for a pixel to enter science analysis."""

CHI2_RED_MAX = 10.0
"""Maximum reduced chi-squared for an acceptable spectral fit."""

MIN_CLOUD_VOXELS = 50
"""Minimum voxels for a cloud to enter the structure catalogue."""


# =============================================================================
# 6. CONSISTENCY CHECK
# =============================================================================

def check_constants():
    """Print which project-specific constants are still at placeholder values."""
    unset = []
    for target in DISTANCE_KPC:
        if DISTANCE_KPC[target] is None:
            unset.append(f"DISTANCE_KPC['{target}']")
    if unset:
        print("constants.py — unset values:")
        for name in unset:
            print(f"  {name}")
    else:
        print("constants.py — all values set.")
        for target, d_kpc in DISTANCE_KPC.items():
            print(f"  {target:10s}  d={d_kpc:.0f} kpc  "
                  f"beam={BEAM_FWHM_PC[target]:.1f} pc FWHM")
    return unset


if __name__ == "__main__":
    check_constants()
