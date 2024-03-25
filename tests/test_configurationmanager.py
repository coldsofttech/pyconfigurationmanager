# Copyright (c) 2024 coldsofttech
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest
import unittest
from pyconfigurationmanager import ConfigurationManager, ConfigurationManagerError
from utilityclass import UtilityClass


class TestConfigurationManager(unittest.TestCase):
    """Unit test cases for ConfigurationManager"""

    def setUp(self) -> None:
        self.file_name = UtilityClass.generate_name('json')
        self.audit_file_name = UtilityClass.generate_name('log')
        UtilityClass.generate_config(self.file_name)

    def tearDown(self) -> None:
        UtilityClass.delete_config(self.file_name)
        UtilityClass.delete_config(self.audit_file_name)

    def test_invalid_file_path(self):
        """Test if load config raises TypeError"""
        with self.assertRaises(TypeError):
            ConfigurationManager.load_config(file_path=100)

    def test_invalid_secure(self):
        """Test if load config raises TypeError"""
        with self.assertRaises(TypeError):
            ConfigurationManager.load_config(secure=100)

    def test_invalid_audit(self):
        """Test if load config raises TypeError"""
        with self.assertRaises(TypeError):
            ConfigurationManager.load_config(audit=100)

    def test_invalid_audit_file_path(self):
        """Test if load config raises TypeError"""
        with self.assertRaises(TypeError):
            ConfigurationManager.load_config(audit_file_path=100)

    @pytest.mark.sequential_order
    def test_valid_no_params(self):
        """Test if load config raises TypeError"""
        self.assertEqual(None, ConfigurationManager._config)
        ConfigurationManager.load_config(file_path=self.file_name)
        self.assertIsInstance(ConfigurationManager._config, dict)

    @pytest.mark.sequential_order
    def test_invalid_exposed_permissions(self):
        """Test if load config raises ConfigurationManagerError"""
        UtilityClass.delete_config(self.file_name)
        self.file_name = UtilityClass.generate_name('json')
        UtilityClass.generate_config(self.file_name, False)
        with self.assertRaises(ConfigurationManagerError):
            ConfigurationManager.load_config(file_path=self.file_name)

    @pytest.mark.sequential_order
    def test_valid_insecure(self):
        """Test if load config works as expected"""
        UtilityClass.delete_config(self.file_name)
        self.file_name = UtilityClass.generate_name('json')
        UtilityClass.generate_config(self.file_name, False)
        self.assertIsInstance(ConfigurationManager._config, dict)

    @pytest.mark.sequential_order
    def test_invalid_file_not_found(self):
        """Test if load config raises ConfigurationManagerError"""
        with self.assertRaises(ConfigurationManagerError):
            ConfigurationManager.load_config(file_path='sample.txt')

    @pytest.mark.sequential_order
    def test_invalid_json(self):
        """Test if load config works as expected"""
        UtilityClass.delete_config(self.file_name)
        self.file_name = UtilityClass.generate_name('json')
        UtilityClass.generate_config(self.file_name, invalid_json=True)
        ConfigurationManager.load_config(file_path=self.file_name)

    @pytest.mark.sequential_order
    def test_get_config_value_invalid_no_config_set(self):
        """Test if load config raises ConfigurationManagerError"""
        with self.assertRaises(ConfigurationManagerError):
            ConfigurationManager.get_config_value('sample')

    @pytest.mark.sequential_order
    def test_get_config_value_valid_string(self):
        """Test if load config works as expected"""
        ConfigurationManager.load_config(self.file_name)
        self.assertEqual('string_of_sample', ConfigurationManager.get_config_value('sample_string'))

    @pytest.mark.sequential_order
    def test_get_config_value_valid_integer(self):
        """Test if load config works as expected"""
        ConfigurationManager.load_config(self.file_name)
        self.assertEqual(100, ConfigurationManager.get_config_value('sample_integer'))

    @pytest.mark.sequential_order
    def test_get_config_value_valid_dict(self):
        """Test if load config works as expected"""
        ConfigurationManager.load_config(self.file_name)
        self.assertIsInstance(ConfigurationManager.get_config_value('sample_others'), dict)

    @pytest.mark.sequential_order
    def test_get_config_value_valid_boolean(self):
        """Test if load config works as expected"""
        ConfigurationManager.load_config(self.file_name)
        self.assertTrue(ConfigurationManager.get_config_value('sample_others.sample_boolean'))

    @pytest.mark.sequential_order
    def test_get_config_value_valid_list(self):
        """Test if load config works as expected"""
        ConfigurationManager.load_config(self.file_name)
        self.assertIsInstance(ConfigurationManager.get_config_value('sample_others.sample_list'), list)
        assert 2 == len(ConfigurationManager.get_config_value('sample_others.sample_list'))

    @pytest.mark.sequential_order
    def test_get_config_value_valid_audit_all(self):
        """Test if load config works as expected"""
        ConfigurationManager.load_config(self.file_name, audit=True, audit_file_path=self.audit_file_name)
        ConfigurationManager.get_config_value()
        expected_output = 'Returning entire configuration.'
        with open(self.audit_file_name, 'r') as file:
            file_content = file.read()
            self.assertIn(expected_output, file_content)

    @pytest.mark.sequential_order
    def test_get_config_value_valid_audit_specific(self):
        """Test if load config works as expected"""
        ConfigurationManager.load_config(self.file_name, audit=True, audit_file_path=self.audit_file_name)
        ConfigurationManager.get_config_value('sample_integer')
        expected_output = 'Accessed configuration value for sample_integer.'
        with open(self.audit_file_name, 'r') as file:
            file_content = file.read()
            self.assertIn(expected_output, file_content)


if __name__ == "__main__":
    unittest.main()
