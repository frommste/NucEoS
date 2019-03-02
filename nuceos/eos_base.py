"""
    eos_base.py

    The script contains the base class for all EOS classes; it exposes a 
    common (required) interface that must be implemented for each new EOS 
    class.
"""

import abc as _abc


class EOSBase(_abc.ABC):

    def from_density(self, rho):
        """Calculate the pressure and specific energy for a given density.

        Parameters
        ----------
        rho : float (or array of floats)
            The density at which to calculate the equation of state.
        """
        pass

    def from_pressure(self, P):
        """Calculate the density and specific energy for a given pressure.

        Parameters
        ----------
        P : float (or array of floats)
            The pressure at which to calculate the equation of state.
        """
        pass
