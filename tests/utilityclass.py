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
            except subprocess.CalledProcessError:
                pass

        try:
            os.remove(file_name)
        except (PermissionError, OSError, FileNotFoundError):
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
                except subprocess.CalledProcessError:
                    pass
            elif platform.system().lower() == 'linux' or platform.system().lower() == 'darwin':
                try:
                    os.chmod(file_name, 0o400)
                except (PermissionError, OSError):
                    pass
