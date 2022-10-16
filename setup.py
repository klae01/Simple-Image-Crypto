from setuptools import setup

setup(
    name="simc",
    version="0.0.0",
    packages=["simc"],
    install_requires=["Pillow", "cryptography"],
    entry_points={
        "console_scripts": ["simc=simc.core:main"],
    },
)
