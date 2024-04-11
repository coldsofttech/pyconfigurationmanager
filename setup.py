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
        'pyloggermanager@ git+https://github.com/coldsofttech/pyloggermanager.git'
    ]
)
