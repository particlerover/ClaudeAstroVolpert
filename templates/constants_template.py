# Created: YYYY-MM-DD HH:MM:SS
# Last Modified: YYYY-MM-DD HH:MM:SS
# Description: Central repository for all physical, astronomical, and
#   project-specific constants. Import this module in every analysis script
#   rather than defining local copies. Change a value here and it propagates
#   everywhere. All entries include units, source, and brief justification.
# Last Edit: Initial template — fill in project-specific sections.

"""
constants.py — Centralised constants for [PROJECT_NAME].

Usage
-----
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import constants as C

    distance_cm = C.DISTANCE_KPC * 1e3 * C.PC_CM
    physical_size_pc = angular_size_arcsec * C.PC_PER_ARCSEC

Add project-specific constants below as you determine them. Document each
one with its units, adopted value, justification, and primary citation.
"""

import numpy as np


# =============================================================================
# 1. FUNDAMENTAL PHYSICAL CONSTANTS (CGS)
# =============================================================================
# CODATA 2018 values; not expected to change.

PC_CM = 3.085677581e18
"""Parsec in centimetres [cm pc⁻¹]."""

AU_CM = 1.495978707e13
"""Astronomical unit in centimetres [cm AU⁻¹]. Exact (IAU 2012)."""

LY_CM = 9.460730472580800e17
"""Light year in centimetres [cm ly⁻¹]."""

M_H_G = 1.6735575e-24
"""Hydrogen atom mass [g]. CODATA 2018."""

M_P_G = 1.67262192369e-24
"""Proton mass [g]. CODATA 2018."""

M_E_G = 9.1093837015e-28
"""Electron mass [g]. CODATA 2018."""

K_B_CGS = 1.380649e-16
"""Boltzmann constant [erg K⁻¹]. CODATA 2018 (exact)."""

G_CGS = 6.67430e-8
"""Gravitational constant [cm³ g⁻¹ s⁻²]. CODATA 2018."""

H_PLANCK_CGS = 6.62607015e-27
"""Planck constant [erg s]. CODATA 2018 (exact)."""

H_BAR_CGS = H_PLANCK_CGS / (2.0 * np.pi)
"""Reduced Planck constant [erg s]."""

C_LIGHT_CGS = 2.99792458e10
"""Speed of light [cm s⁻¹]. Exact (SI definition)."""

SIGMA_SB_CGS = 5.670374419e-5
"""Stefan-Boltzmann constant [erg cm⁻² s⁻¹ K⁻⁴]. CODATA 2018."""

ARCSEC_PER_RAD = 206264.806247
"""Arcseconds per radian."""

DEG_PER_RAD = 180.0 / np.pi
"""Degrees per radian."""


# =============================================================================
# 2. ASTRONOMICAL CONSTANTS
# =============================================================================

M_SUN_G = 1.98892e33
"""Solar mass [g]. IAU 2015 nominal."""

R_SUN_CM = 6.957e10
"""Solar radius [cm]. IAU 2015 nominal."""

L_SUN_CGS = 3.828e33
"""Solar luminosity [erg s⁻¹]. IAU 2015 nominal."""

T_SUN_EFF_K = 5772.0
"""Solar effective temperature [K]. IAU 2015 nominal."""

T_CMB_K = 2.7255
"""
CMB temperature [K].
Fixsen (2009, ApJ 707, 916). Used in excitation corrections for molecular
line radiative transfer (J(T_ex) - J(T_CMB) correction).
"""

H0_KMS_MPC = 70.0
"""
Hubble constant [km s⁻¹ Mpc⁻¹].
Round value consistent with Planck 2018 (67.4) and local measurements (~73).
Update if your project requires a specific adopted value and citation.
"""


# =============================================================================
# 3. GAS MICROPHYSICS
# =============================================================================

HE_CORRECTION = 1.36
"""
Factor by which total gas mass (H₂ + He + metals) exceeds pure-H₂ mass.
Standard ISM composition: ~71% H, ~27% He, ~2% metals by mass.
See Bolatto, Wolfire & Leroy (2013, ARA&A 51, 207), their §2.1.
M_gas = 1.36 × M_H2 when using H₂-only mass estimates.
"""

MU_H2 = 2.0 * HE_CORRECTION  # ≈ 2.72
"""
Mean molecular mass per H₂ molecule [units of m_H], including helium.
rho [g cm⁻³] = MU_H2 × M_H_G × n_H2 [cm⁻³].
See Bolatto et al. (2013) §2.1.
"""

MU_SOUND = MU_H2 / (1.0 + (MU_H2 - 2.0) / 4.0)  # ≈ 2.305
"""
Mean particle mass for sound-speed calculations [units of m_H].
Accounts for particle number (H₂ molecules + He atoms, not just total mass).
c_s = sqrt(gamma × k_B × T / (MU_SOUND × M_H_G)).
"""

ALPHA_VIR_PREFACTOR = 5.0
"""
Prefactor in the virial parameter definition.
alpha_vir = 5 × sigma_v² × R / (G × M)
for a sphere with density profile rho(r) ~ r⁻¹ (Bertoldi & McKee 1992,
ApJ 395, 140). The value 5 gives alpha_vir = 1 at virial equilibrium.
Note: some authors use alpha_vir = 2 sigma² R / (G M) — a factor-of-2
different convention. Document which you use in your analysis.
"""

C_LARSON_KMS_PER_PC05 = 0.7
"""
Larson size-linewidth coefficient [km s⁻¹ pc⁻⁰·⁵].
sigma_v = C_LARSON × R^0.5 for turbulent, virialised GMCs.
From Solomon et al. (1987, ApJ 319, 730) and Larson (1981, MNRAS 194, 809).
Approximately correct for extragalactic GMCs too (Bolatto et al. 2013, Eq. 9),
though may deviate in high-feedback or low-metallicity environments.
"""


# =============================================================================
# 4. CO LINE PROPERTIES
# =============================================================================
# Common rest frequencies for CO rotational lines.

NU_12CO10_HZ = 1.15271202e11
"""12CO J=1→0 rest frequency [Hz] = 115.271202 GHz. CDMS."""

NU_12CO21_HZ = 2.30538000e11
"""12CO J=2→1 rest frequency [Hz] = 230.538000 GHz. CDMS."""

NU_12CO32_HZ = 3.45796000e11
"""12CO J=3→2 rest frequency [Hz] = 345.796000 GHz. CDMS."""

NU_13CO10_HZ = 1.10201354e11
"""13CO J=1→0 rest frequency [Hz] = 110.201354 GHz. CDMS."""

NU_13CO21_HZ = 2.20399e11
"""13CO J=2→1 rest frequency [Hz] = 220.399 GHz. CDMS."""

NU_HI_HZ = 1.42040575e9
"""HI 21 cm hyperfine rest frequency [Hz] = 1420.40575 MHz. NIST."""

NU_HALPHA_HZ = 4.56780e14
"""Hα rest frequency [Hz]. Vacuum wavelength = 656.28 nm."""


# =============================================================================
# 5. CO-TO-H2 CONVERSION FACTORS
# =============================================================================

ALPHA_CO_MW = 4.35
"""
Milky Way CO-to-H₂ conversion factor [M_sun (K km/s pc²)⁻¹].
Includes He (gives total gas mass, not just H₂).
Bolatto, Wolfire & Leroy (2013, ARA&A 51, 207), their Eq. 3 and §3.1.
Equivalent to X_CO_MW ≈ 2.0 × 10²⁰ cm⁻² (K km/s)⁻¹.
"""

X_CO_MW_CM2_PER_KKMS = 2.0e20
"""
Milky Way X_CO [cm⁻² (K km/s)⁻¹].
Bolatto et al. (2013). Does NOT include He.
N_H2 = X_CO × W_CO where W_CO is the integrated line intensity [K km/s].
"""


# =============================================================================
# 6. PROJECT-SPECIFIC CONSTANTS
# =============================================================================
# Fill in the sections below as you establish your project's adopted values.
# Document each one: units, adopted value, justification, key reference.

# ── Target system ──────────────────────────────────────────────────────────

DISTANCE_KPC = None
"""
Distance to the primary target [kpc].
[FILL IN: adopted value, precision, reference]
e.g. 840 kpc for M33 (Freedman et al. 2001, ApJ 553, 47; or TRGB/Cepheid value)
"""

PC_PER_ARCSEC = None  # will be set below once DISTANCE_KPC is filled in
"""Physical scale at the target [pc arcsec⁻¹]."""

TARGET_RA_DEG = None
"""Right ascension of primary target or reference position [deg, J2000]."""

TARGET_DEC_DEG = None
"""Declination of primary target or reference position [deg, J2000]."""


def set_distance(distance_kpc):
    """
    Call this once DISTANCE_KPC is known to set derived geometric quantities.
    e.g. set_distance(840.0) for M33.
    """
    global DISTANCE_KPC, PC_PER_ARCSEC
    DISTANCE_KPC = distance_kpc
    PC_PER_ARCSEC = distance_kpc * 1e3 / ARCSEC_PER_RAD


# ── Beam / resolution ──────────────────────────────────────────────────────

BEAM_FWHM_ARCSEC = None
"""
Angular resolution (FWHM of synthesised or convolved beam) [arcsec].
[FILL IN: value from FITS header BMAJ; for matched-resolution analysis,
 use the common beam of all datasets]
"""

PIX_SCALE_ARCSEC = None
"""Pixel scale of the primary analysis cube [arcsec pixel⁻¹]."""

CHANNEL_WIDTH_KMS = None
"""Spectral channel width of the primary cube [km s⁻¹]."""


# ── Chemistry and abundances ───────────────────────────────────────────────

ALPHA_CO = None
"""
Adopted CO-to-H₂ conversion factor for this target [M_sun (K km/s pc²)⁻¹].
[FILL IN: value and key reference, e.g. Bolatto+2013 for MW; Leroy+2011 for LMC]
"""

ISO_RATIO_12C_13C = None
"""
Adopted [¹²CO/¹³CO] isotopologue abundance ratio.
[FILL IN: value and reference. MW disc: ~60-70; LMC: ~50-55; CMZ: ~25-30]
"""


# ── Analysis quality thresholds ────────────────────────────────────────────

SNR_MIN = 3.0
"""
Minimum signal-to-noise ratio for a pixel/channel to be included in analysis.
A value of 3.0 corresponds to a standard 3σ detection threshold.
"""

CHI2_RED_MAX = 10.0
"""
Maximum reduced chi-squared for a fit to be considered acceptable.
Adjust based on your model complexity and noise characteristics.
"""


# =============================================================================
# 7. CONSISTENCY CHECK
# =============================================================================

def check_constants():
    """Print which project-specific constants have not yet been set."""
    unset = []
    for name, val in [
        ("DISTANCE_KPC",        DISTANCE_KPC),
        ("TARGET_RA_DEG",       TARGET_RA_DEG),
        ("TARGET_DEC_DEG",      TARGET_DEC_DEG),
        ("BEAM_FWHM_ARCSEC",    BEAM_FWHM_ARCSEC),
        ("PIX_SCALE_ARCSEC",    PIX_SCALE_ARCSEC),
        ("CHANNEL_WIDTH_KMS",   CHANNEL_WIDTH_KMS),
        ("ALPHA_CO",            ALPHA_CO),
        ("ISO_RATIO_12C_13C",   ISO_RATIO_12C_13C),
    ]:
        if val is None:
            unset.append(name)
    if unset:
        print("constants.py — unset project-specific values:")
        for name in unset:
            print(f"  {name}")
    else:
        print("constants.py — all project-specific values are set.")
    return unset


if __name__ == "__main__":
    check_constants()
