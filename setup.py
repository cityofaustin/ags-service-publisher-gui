from setuptools import setup

setup(
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        'ags_service_publisher',
        'PyQt6',
    ],
    use_scm_version=True,
)
