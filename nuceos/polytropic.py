"""
    polytropic.py

    A simple polytropic equation of state.
"""

import numpy as _np

from .eos_base import EOSBase


class PolytopricEOS(EOSBase):
    """A simple polytropic equation of state.

    This class implements a polytropic EOS:

    .. math::
        P(\rho) = K \rho^\gamma
    """

    def __init__(self, K, gamma):
        """Initialize a polytropic EOS.
        Parameters
        ----------
        K : float
            The polytropic constant for the gas.
        gamma : float
            The adiabatic exponent of the gas.
        """
        self.K = K
        self.gamma = gamma

        # These get used for the specific energy and density calculations
        self.inv_gamma = 1.0/gamma
        self.inv_gamma_m1 = 1.0/(gamma - 1.0)
        self.inv_K = 1.0/K

    def from_density(self, rho):
        """Calculate the pressure and specific energy from a specified density.

        Parameters
        ----------
        rho : float (or array of floats)
            The density of the gas.

        Returns
        -------
        tuple of floats (or tuple of array of floats)
            The pressure and specific energy
        """
        P = self.K*rho**self.gamma
        eps = self.inv_gamma_m1*P/rho

        return P, eps

    def from_pressure(self, P):
        """Calculate the density and specific energy from a specified pressure.

        Parameters
        ----------
        P : float (or array of floats)
            The pressure of the gas.

        Returns
        -------
        tuple of floats (or tuple of array of floats)
            The density and specific energy
        """
        rho = (P*self.inv_K)**(self.inv_gamma)
        eps = self.inv_gamma_m1*P/rho

        return rho, eps
