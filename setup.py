from setuptools import setup

setup(
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        'archook',
        'PyQt5',
    ],
    use_scm_version=True,
)
