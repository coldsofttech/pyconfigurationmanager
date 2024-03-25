# `pyconfigurationmanager`
The pyconfigurationmanager package provides a set of utilities for managing configuration settings in Python applications. It includes classes and functions for loading configuration data from files, auditing configuration changes, and ensuring secure access to configuration files.

## Installation
Configuration Manager can be installed using pip:
```bash
pip install git+https://github.com/coldsofttech/pyconfigurationmanager.git
```

## Usage
````python
from pyconfigurationmanager import ConfigurationManager

# Load the configuration file
ConfigurationManager.load_config(file_path='config.json')

# Retrieve a string value
string_value = ConfigurationManager.get_config_value('sample_string')
print(string_value)  # Output: 'string_of_sample'

# Retrieve an integer value
integer_value = ConfigurationManager.get_config_value('sample_integer')
print(integer_value)  # Output: 100

# Retrieve a dictionary value
dict_value = ConfigurationManager.get_config_value('sample_others')
print(dict_value)
# Output:
# {'sample_boolean': True, 'sample_list': ['list_1', 'list_2']}

# Retrieve a boolean value
boolean_value = ConfigurationManager.get_config_value('sample_others.sample_boolean')
print(boolean_value)  # Output: True

# Retrieve a list value
list_value = ConfigurationManager.get_config_value('sample_others.sample_list')
print(list_value)  # Output: ['list_1', 'list_2']
````

# Documentation
## `pyconfigurationmanager`
### `ConfigurationManager`
The ConfigurationManager class is the heart of the package, offering a suite of functionalities for managing configuration settings.

#### Methods
- `load_config(file_path: Optional[str] = 'config.json', secure: Optional[bool] = True, audit: Optional[bool] = False, audit_file_path: Optional[str] = 'audit.log')`: Loads configuration settings from a file into memory, with options to enable secure mode and auditing. By default, secure mode is enabled, ensuring that the configuration file has only readable permissions for the user. If auditing is enabled, all configuration accesses are logged for future audit purposes.
- `get_config_value(key: Optional[str] = None)`: Retrieves the value of a specific configuration setting or the entire configuration if no key is provided. Hierarchical keys can be accessed by separating them with '.'.

### `ConfigurationManagerError`
This error class is employed to signal any issues or errors encountered during the execution of ConfigurationManager methods.

#### Methods
- `__init__(message: Optional[str])` - Initialize a ConfigurationManagerError