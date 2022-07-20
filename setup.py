import re
from setuptools import find_packages, setup


def get_requirements():
    RGX_COMMENT = re.compile(r" *#.*$")
    with open("requirements.txt") as f:
        requirements = [line for raw in f.readlines()
                        if (line := RGX_COMMENT.sub(raw, "").strip()) != ""]
    return requirements


setup(
    name='app',
    packages=find_packages(),
    version="0.0.1",
    description='Use fastAPI with mongoDB',
    python_requires='>=3.9',
    install_requires=get_requirements(),
    entry_points={'console_scripts': ["app=app.cli:main"]}
)
