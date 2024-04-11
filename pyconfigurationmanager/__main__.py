import getpass
import json
import os.path
import platform
import socket
import subprocess
from types import NoneType
from typing import Optional, Any, Union


class UtilityClass:
    """
    Utility class providing methods to retrieve information about the local machine and current user.
    """

    @staticmethod
    def get_ip_address() -> str:
        """
        Get the IP address of the local machine.

        :return: The IP address of the local machine as a string.
        :rtype: str
        """
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except socket.gaierror:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 80))
                ip_address = s.getsockname()[0]
                s.close()
            except socket.error:
                ip_address = '127.0.0.1'

        return ip_address

    @staticmethod
    def get_username() -> str:
        """
        Get the username of the current user.

        :return: The username of the current user as a string.
        :rtype: str
        """
        username = getpass.getuser()
        return username


class ConfigurationManagerError(RuntimeError):
    """
    Error class raised when there is an issue with ConfigurationManager.
    """

    def __init__(
            self,
            message: Optional[str] = 'ConfigurationManager load_config is not set.'
    ):
        """
        Initialize a ConfigurationManagerError.

        :param message: The error message to be associated with the exception.
        Defaults to 'ConfigurationManager load_config is not set.'
        :type message: Optional[str]
        """
        if not isinstance(message, str):
            raise TypeError('message should be a string.')

        self.message = message
        super().__init__(self.message)


class ConfigurationManager:
    """
    Class for managing configuration settings.
    """

    _audit = False
    _audit_file_path = None
    _audit_logger = None
    _config = None
    _file_full_path = ''

    @classmethod
    def _configure_audit_logger(cls) -> None:
        """
       Configure the audit logger.
       """
        import pyloggermanager

        if cls._audit:
            formatter = pyloggermanager.formatters.DefaultFormatter(
                format_str='%(time)s :: %(message)s'
            )
            handler = pyloggermanager.handlers.FileHandler(
                file_name=cls._audit_file_path,
                level=pyloggermanager.LogLevel.INFO,
                formatter=formatter
            )
            cls._audit_logger = pyloggermanager.Logger(name='audit_logger', level=pyloggermanager.LogLevel.INFO)
            cls._audit_logger.add_handler(handler)

    @classmethod
    def _configure_loggers(cls) -> None:
        """
        Configure all loggers.
        """
        cls._configure_audit_logger()

    @classmethod
    def _check_file_permissions(cls, file_path: str) -> None:
        """
        Check the permissions of the configuration file.

        :param file_path: The path of the configuration file.
        :type file_path: str
        """
        error = f'Configuration file "{file_path}" should be readable only by the user.'
        if platform.system().lower() == "windows":
            command = f'powershell.exe icacls "{file_path}"'
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
            )
            output, _ = process.communicate()
            permissions = output.decode().strip().replace(file_path, '')
            permissions_list = [p.strip() for p in permissions.split('\n') if p.strip()]

            if len(permissions_list) > 2:
                raise OSError(error)
            elif not UtilityClass.get_username() in permissions_list[0]:
                raise OSError(error)
            elif any(perm in permissions_list[0] for perm in ['(F)', '(M)']):
                raise OSError(error)
        elif platform.system().lower() == 'linux' or platform.system().lower() == 'darwin':
            file_stat = os.stat(file_path)
            if file_stat.st_mode & 0o777 != 0o400:
                raise OSError(error)
        else:
            raise OSError("Unsupported operating system.")

    @classmethod
    def _log_audit(cls, method: str, message: str) -> None:
        """
        Log audit messages.

        :param method: The method name.
        :type method: str
        :param message: The message to be logged.
        :type message: str
        """
        if cls._audit:
            source_ip = UtilityClass.get_ip_address()
            username = UtilityClass.get_username()
            formatted_message = f'{method} :: {source_ip} :: {username} :: {message}'
            cls._audit_logger.info(formatted_message, ignore_display=True)

    @classmethod
    def load_config(
            cls,
            file_path: Optional[str] = 'config.json',
            secure: Optional[bool] = True,
            audit: Optional[bool] = False,
            audit_file_path: Optional[str] = 'audit.log'
    ) -> None:
        """
        Load configuration settings from a file.

        :param file_path: The path of the configuration file. Defaults to 'config.json'.
        :type file_path: Optional[str]
        :param secure: Flag indicating whether secure mode is enabled. Defaults to True.
        :type secure: Optional[bool]
        :param audit: Flag indicating whether auditing is enabled. Defaults to False.
        :type audit: Optional[bool]
        :param audit_file_path: The file path for storing audit logs. Defaults to 'audit.log'.
        :type audit_file_path: Optional[str]
        """
        if not isinstance(file_path, str):
            raise TypeError('file_path should be a string.')
        elif not isinstance(secure, bool):
            raise TypeError('secure should be a boolean.')
        elif not isinstance(audit, bool):
            raise TypeError('audit should be a boolean.')
        elif not isinstance(audit_file_path, str):
            raise TypeError('audit_file_path should be a string.')

        try:
            cls._file_full_path = os.path.abspath(file_path)

            if secure:
                cls._check_file_permissions(cls._file_full_path)

            with open(cls._file_full_path, 'r') as config_file:
                cls._config = json.load(config_file)
        except FileNotFoundError:
            raise ConfigurationManagerError(f'Configuration file "{file_path}" not found.')
        except json.JSONDecodeError:
            raise ConfigurationManagerError(f'Error decoding JSON in the configuration file "{file_path}".')
        except OSError as e:
            raise ConfigurationManagerError(str(e))

        cls._audit = audit
        cls._audit_file_path = audit_file_path
        cls._configure_loggers()

    @classmethod
    def get_config_value(cls, key: Optional[str] = None) -> Any:
        """
        Get the value of a configuration setting.

        :param key: The key (separated by '.') to access a specific configuration value.
        If None, returns the entire configuration.
        :type key: Optional[str]
        :return: The value of the configuration key
        :rtype: Any
        """
        if not isinstance(key, Union[str, NoneType]):
            raise TypeError('key should be a string.')

        if cls._config is None:
            raise ConfigurationManagerError()

        if key is None:
            cls._log_audit(cls.__name__, 'Returning entire configuration.')
            return cls._config
        else:
            keys = key.split('.')
            value = cls._config
            for k in keys:
                value = value[k]

            cls._log_audit(cls.__name__, f'Accessed configuration value for {key}.')
            return value
