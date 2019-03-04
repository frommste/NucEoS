# NucEoS
Python interface for tabulated nuclear equations of state found on [stellarcollapse.org](https://stellarcollapse.org/equationofstate).

## Installation
1. Install NucEoS dependencies:
   * `numpy`
   * `scipy`
   * `h5py`
2. Download or clone NucEoS
   ```bash
   git clone https://github.com/frommste/NucEoS.git
   ```
3. From the top NucEoS directory, run the following command to install the package:
   ```bash
   python setup.py install
   ```

## Basic Usage

### Analytic Polytropic EOS
```python
import numpy as np
from nuceos import PolytropicEOS, units

K = 3e4         # Polytropic constant
gamma = 2.75    # Adiabatic index

# Create a polytropic EOS
eos = PolytropicEOS(K, gamma)

# Generate a range of densities in CGS
rho = np.geomspace(2.8e14, 1e16, 50)

# Convert to relativistic units
rho = units.convert(rho, units.CGS.density, units.REL.density)

# Use the eos to calculate pressures and specific energies
P, eps = eos.from_density(rho)
```

### Beta Equilibrium from Tabulated EOS
```python
import numpy as np
from nuceos import BetaEquilibriumEOS, units

# Name of an EOS table file downloaded from stellarcollapse.org
eos_file = "SFHo.h5"

# Create a beta equilibrium EOS at a low temperature (in MeV)
eos = BetaEquilibriumEOS(eos_file, T0=0.01)

# Create a range of densities up to the tables maximum
# Note: the EOS object uses relativistic units
rho_min = 2.8e14
rho_min = units.convert(rho_min, units.CGS.density, units.REL.density)

rho = np.geomspace(rho_min, eos.rho_max, 50)

# Use the eos to calculate pressures and specific energies
P, eps = eos.from_density(rho)
```

## Notes
* Currently only a simple polytropic EOS and a beta equilibrium EOS from [stellarcollapse.org](https://stellarcollapse.org/equationofstate) are implemented.  These two are useful for applications such as TOV solvers.
* Some of the tables (e.g. the LS220 tables), do not always have beta equilibrium values for every density and temperature.
* A full driver for reading the EOS tables will be added at a later date