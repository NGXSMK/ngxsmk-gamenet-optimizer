from setuptools import setup, find_packages # type: ignore

setup(
    name="ngxsmk-gamenet-optimizer",
    version="2.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "psutil>=5.9.0",
        "pywin32>=307",
        "speedtest-cli>=2.1.0",
        "ping3>=4.0.0",
        "matplotlib>=3.8.0",
        "numpy>=1.26.0",
        "netifaces>=0.11.0",
        "requests>=2.31.0",
        "customtkinter>=5.2.0",
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ngx-optimizer-api=ngx_optimizer.api:run_server",
        ],
    },
    python_requires=">=3.8",
    author="NGXSMK",
    description="A comprehensive network and system optimization tool for gamers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NGXSMK/ngxsmk-gamenet-optimizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
