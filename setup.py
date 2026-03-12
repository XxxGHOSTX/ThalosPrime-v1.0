"""
Setup script for Thalos Prime Agent Session Management
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="thalos-prime-agent-session",
    version="1.0.0",
    author="Thalos Prime Team",
    author_email="team@thalosprime.ai",
    description="Deterministic AI Agent Session Management System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XxxGHOSTX/ThalosPrime-v1.0",
    project_urls={
        "Bug Tracker": "https://github.com/XxxGHOSTX/ThalosPrime-v1.0/issues",
        "Documentation": "https://github.com/XxxGHOSTX/ThalosPrime-v1.0/blob/main/docs/README.md",
        "Source Code": "https://github.com/XxxGHOSTX/ThalosPrime-v1.0",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "thalos=thalos_prime.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "ai",
        "agent",
        "session-management",
        "deterministic",
        "thalos-prime",
        "synthetic-intelligence",
    ],
)
