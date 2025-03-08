# setup.py
from setuptools import setup, find_packages

setup(
    name="finanzas_personales",  # Nombre del paquete en PyPI
    version="0.1.2",  # cámbiala según avances
    packages=find_packages(),  # Encuentra automáticamente los subpaquetes
    install_requires=[
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "matplotlib>=3.5.0"
    ],
    entry_points={
        "console_scripts": [
            "finanzas_personales = finanzas_personales.main:run_main"
        ]
    },
    author="Erick Hernandez",
    author_email="constacto@dvcosta.dev",  
    description="Una aplicación de consola para gestionar finanzas personales",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",
    url="https://github.com/ErickCosta98/finanzas_personales",  # URL del repositorio
    license="MIT",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
