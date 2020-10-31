from setuptools import setup, find_packages

def load_readme() -> str:
    with open("README.md", encoding="utf-8") as f:
        return f.read()

setup(
    name='ranjg',
    version='0.1.0.2',
    url='https://github.com/unaguna/random-json-generator',
    author='k-izumi',
    author_email='k.izumi.ysk@gmail.com',
    maintainer='k-izumi',
    maintainer_email='k.izumi.ysk@gmail.com',
    description='Generate json text randomly',
    long_description=load_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['test_*.py']),
    install_requires=[
        'rstr',
    ],
    license="MIT",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
    ],
)
