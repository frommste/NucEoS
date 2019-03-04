from setuptools import setup

setup(name="nuceos",
      version="0.1",
      description="Python interface for tabulated nuclear equations of state.",
      author="Steven Fromm",
      author_email="fromm@nscl.msu.edu",
      packages=["nuceos"],
      install_requires=["numpy", "scipy", "h5py"],
      license="MIT")
