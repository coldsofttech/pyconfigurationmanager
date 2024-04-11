import unittest
from pyconfigurationmanager import ConfigurationManagerError


class TestConfigurationManagerError(unittest.TestCase):
    """Unit test cases for ConfigurationManagerError"""

    def test_init_valid(self):
        """Test if init method works as expected"""
        with self.assertRaises(ConfigurationManagerError):
            raise ConfigurationManagerError('Test error')


if __name__ == "__main__":
    unittest.main()
