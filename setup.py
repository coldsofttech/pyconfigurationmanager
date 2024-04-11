from setuptools import setup
import pyconfigurationmanager

setup(
    name=pyconfigurationmanager.__name__,
    version=pyconfigurationmanager.__version__,
    packages=[
        pyconfigurationmanager.__name__
    ],
    url='https://github.com/coldsofttech/pyconfigurationmanager',
    license='MIT',
    author='coldsofttech',
    description=pyconfigurationmanager.__description__,
    install_requires=[
        'pyloggermanager'
    ],
    requires_python=">=3.10",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=["configuration", "configuration-management", "config-manager"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities :: Configuration Management",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ]
)
