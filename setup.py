import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()

packages = ["md-formatter"]

setuptools.setup(
    name="md-formatter",
    author="cibere",
    author_email="cibere.dev@gmail.com",
    url="https://github.com/cibere/md-formatter",
    project_urls={
        "Code": "https://github.com/cibere/md-formatter",
        "Issue tracker": "https://github.com/cibere/md-formatter/issues",
        "Discord/Support Server": "https://discord.gg/2MRrJvP42N",
    },
    version="0.1.0",
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    packages=packages,
    description="A package that helps format md files",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
)
