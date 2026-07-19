from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ai-se-os",
    version="12.0.0",
    author="AI-SE OS Team",
    description="Engineering Intelligence Platform with OpenRouter Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ai-se-os/ai-se-os",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pydantic>=2.0.0",
        "redis>=5.0.0",
        "sqlalchemy>=2.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "opentelemetry-api>=1.20.0",
        "prometheus-client>=0.19.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "click>=8.1.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-se-os=cli.main:cli",
        ],
    },
)