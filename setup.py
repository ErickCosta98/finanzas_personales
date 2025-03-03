from setuptools import setup, find_packages

setup(
    name="finanzas_personales",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "matplotlib>=3.5.0"
    ],
    entry_points={
        "console_scripts": [
            "finanzas_personales = finanzas_personales.main:main"
        ]
    },
    author="Tu Nombre",
    description="Una aplicación de consola para gestionar finanzas personales",
    license="MIT",
    python_requires=">=3.8"
)
