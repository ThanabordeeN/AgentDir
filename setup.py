from setuptools import setup, find_packages

setup(
    name='agent-dir',
    version='0.1.0',
    author='Thanabordee Nammungkhun',
    author_email='thanabordee.noun@gmail.com',
    description='A project for managing agents with a user interface and LLM integration.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'kivy',
        'dspy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)