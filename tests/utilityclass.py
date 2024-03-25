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

import json
import os
import platform
import random
import string
import subprocess


class UtilityClass:
    """Utility class for unit test cases"""

    @staticmethod
    def generate_name(extension: str, length: int = 10) -> str:
        """Generates file name based on the extension provided"""
        letters = string.ascii_lowercase
        file_name = ''.join(random.choice(letters) for _ in range(length))
        return f'{file_name}.{extension}'

    @staticmethod
    def delete_config(file_name: str) -> None:
        """Delete provided file"""
        if platform.system().lower() == 'windows':
            command = f'icacls "{file_name}" /inheritance:r /grant:r "%USERNAME%:F"'
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                pass

        try:
            os.remove(file_name)
        except (PermissionError, OSError, FileNotFoundError) as e:
            pass

    @staticmethod
    def generate_config(file_name: str, limited_permissions: bool = True, invalid_json: bool = False) -> None:
        """Creates sample config json file"""
        config_data = {
            'sample_string': 'string_of_sample',
            'sample_integer': 100,
            'sample_others': {
                'sample_boolean': True,
                'sample_list': [
                    'list_1',
                    'list_2'
                ]
            }
        } if not invalid_json else 100

        with open(file_name, 'w') as config_file:
            config_file.write(json.dumps(config_data, indent=4))

        if limited_permissions:
            if platform.system().lower() == 'windows':
                commands = [
                    f'icacls "{file_name}" /inheritance:r /grant:r "%USERNAME%:RX"',
                    f'icacls "{file_name}" /deny *S-1-1-0:(OI)(CI)(F)'
                ]
                try:
                    for command in commands:
                        subprocess.run(command, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    pass
            elif platform.system().lower() == 'linux':
                try:
                    os.chmod(file_name, 0o400)
                except (PermissionError, OSError) as e:
                    pass
