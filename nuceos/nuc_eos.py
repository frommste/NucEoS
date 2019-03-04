"""
    nuc_eos.py

    This script implements equations of state classes based on the tabulated equations of state on stellarcollapse.org.
"""

import numpy as _np
import h5py as _h5py

from scipy.interpolate import interp1d

from .eos_base import EOSBase
from .units import convert, CGS, REL


class BetaEquilibriumEOS(EOSBase):
    """A beta equilibrium EOS from a stellarcollapse.org table."""

    def __init__(self, eos_table_file, T0=0.01):
        # Open the EOS table and load needed values
        hf = _h5py.File(eos_table_file)

        logpress = hf["/logpress"][()]
        logtemp = hf["/logtemp"][()]
        logenergy = hf["/logenergy"][()]
        self.logrho = hf["/logrho"][()]

        ye = hf["/ye"][()]

        # Note: using all three potentials since the munu field is not
        # consistent between all tables; the LS220 table has an erroneous
        # shift due to proton-neutron rest mass differences
        mue = hf["/mu_e"][()]
        mun = hf["/mu_n"][()]
        mup = hf["/mu_p"][()]

        self.energy_shift = hf["/energy_shift"][0]

        hf.close()

        self.logpress = _np.zeros_like(self.logrho)
        self.logenergy = _np.zeros_like(self.logrho)
        self.ye = _np.zeros_like(self.logrho)

        # Find the index of the first temperature above the requested
        # temperature
        logT0 = _np.log10(T0)
        iT0 = _np.searchsorted(logtemp, logT0)

        self.T0 = 10.0**logtemp[iT0]

        # Calculate beta equilibrium for every density (at specified T)
        for irho in range(self.logrho.size):
            munu = mue[:, iT0, irho] - mun[:, iT0, irho] + mup[:, iT0, irho]
            press_func = interp1d(munu, logpress[:, iT0, irho])
            energy_func = interp1d(munu, logenergy[:, iT0, irho])
            ye_func = interp1d(munu, ye[:])

            self.logpress[irho] = press_func(0.0)
            self.logenergy[irho] = energy_func(0.0)
            self.ye[irho] = ye_func(0.0)

        # Convert to relativistic units and log (not log10) scale
        self.logpress = \
            _np.log(convert(10.0**self.logpress, CGS.pressure, REL.pressure))
        self.logenergy = \
            _np.log(convert(10.0**self.logenergy,
                            CGS.specific_energy, REL.specific_energy))
        self.logrho = \
            _np.log(convert(10.0**self.logrho, CGS.density, REL.density))

        self.energy_shift = \
            convert(self.energy_shift, CGS.specific_energy,
                    REL.specific_energy)

        # Store min/max values (and in log space)
        self.logrho_min = self.logrho.min()
        self.logrho_max = self.logrho.max()

        self.rho_min = _np.exp(self.logrho_min)
        self.rho_max = _np.exp(self.logrho_max)

        self.logpress_min = self.logpress.min()
        self.logpress_max = self.logpress.max()
        self.press_min = _np.exp(self.logpress_min)
        self.press_max = _np.exp(self.logpress_max)

        print(self.press_min, self.press_max)

        self.ye_min = self.ye.min()
        self.ye_max = self.ye.max()

        # Create interpolators for later use
        self.__P_from_rho_func = interp1d(self.logrho, self.logpress)
        self.__eps_from_rho_func = interp1d(self.logrho, self.logenergy)

        self.__rho_from_P_func = interp1d(self.logpress, self.logrho)
        self.__eps_from_P_func = interp1d(self.logpress, self.logenergy)

    def from_density(self, rho):
        """Calculate the pressure and specific energy for a given density.

        Parameters
        ----------
        rho : float (or array of floats)
            The density at which to calculate the equation of state.

        Returns
        -------
        tuple of floats (or tuple of array of floats)
            The pressure and specific energy.
        """
        lrho = _np.log(rho)
        lP = self.__P_from_rho_func(lrho)
        leps = self.__eps_from_rho_func(lrho)

        P = _np.exp(lP)
        eps = _np.exp(leps) - self.energy_shift

        return P, eps

    def from_pressure(self, P):
        """Calculate the density and specific energy for a given pressure.

        Parameters
        ----------
        P : float (or array of floats)
            The pressure at which to calculate the equation of state.

        Returns
        -------
        tuple of floats (or tuple of array of floats)
            The density and specific energy.
        """
        lP = _np.log(P)
        lrho = self.__rho_from_P_func(lP)
        leps = self.__eps_from_P_func(lP)

        rho = _np.exp(lrho)
        eps = _np.exp(leps) - self.energy_shift

        return rho, eps
