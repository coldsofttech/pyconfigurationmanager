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

def pytest_collection_modifyitems(config, items):
    """
    Custom pytest hook to modify the collection of test items.
    This function sorts test items to execute specific tests first.
    """
    def test_order(test_name):
        # Define the desired order of execution for specific test names
        order_mapping = {
            'test_get_config_value_invalid_no_config_set': 1,
            'test_valid_no_params': 2,
            'test_invalid_exposed_permissions': 3,
            'test_valid_insecure': 4,
            'test_invalid_file_not_found': 5,
            'test_invalid_json': 6,
            'test_get_config_value_valid_string': 7,
            'test_get_config_value_valid_integer': 8,
            'test_get_config_value_valid_dict': 9,
            'test_get_config_value_valid_boolean': 10,
            'test_get_config_value_valid_list': 11,
            'test_get_config_value_valid_audit_all': 12,
            'test_get_config_value_valid_audit_specific': 13
        }
        return order_mapping.get(test_name, float('inf'))  # Default to infinity for tests not in the mapping

    items.sort(key=lambda item: (test_order(item.nodeid.split("::")[-1]), item.fspath, item.originalname))
