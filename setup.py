"""
Setup script for Phin AI Assistant
"""
from setuptools import setup, find_packages

setup(
    name="phin-ai-assistant",
    version="1.0.0",
    description="Phin AI Assistant - Your intelligent AI companion",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "groq>=0.4.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'phin-ai=phin_main:main',
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
