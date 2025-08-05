from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="product-finder-bot",
    version="1.0.0",
    author="ProductFinderBot Team",
    author_email="contact@productfinderbot.com",
    description="Automated Product Discovery from Reddit to TikTok",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/product-finder-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "product-finder-bot=product_finder_bot:main",
        ],
    },
    keywords="reddit tiktok automation scraping product-discovery social-media",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/product-finder-bot/issues",
        "Source": "https://github.com/yourusername/product-finder-bot",
        "Documentation": "https://github.com/yourusername/product-finder-bot#readme",
    },
)