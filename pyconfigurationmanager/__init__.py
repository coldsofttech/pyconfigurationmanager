__all__ = [
    "ConfigurationManager",
    "ConfigurationManagerError",
    "__author__",
    "__description__",
    "__name__",
    "__version__"
]
__author__ = "coldsofttech"
__description__ = """
The pyconfigurationmanager package provides a set of utilities for managing configuration settings in
Python applications. It includes classes and functions for loading configuration data from files,
auditing configuration changes, and ensuring secure access to configuration files.
"""
__name__ = "pyconfigurationmanager"
__version__ = "0.1.2"

from pyconfigurationmanager.__main__ import ConfigurationManager, ConfigurationManagerError
