from setuptools import setup


setup(
    name='lab',
    version='0.1',
    py_modules=['lab'],
    install_requires=[
        'fire==0.1.3',
        'GitPython==2.1.11',
        'requests == 2.20.1',

    ],
    entry_points={
        'console_scripts': [
            'lab=lab:main'
        ]
    }
)
