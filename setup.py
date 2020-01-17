import setuptools

setuptools.setup(
    name='oi_bus',
    version='0.1.0',
    packages=setuptools.find_packages(),
    package_data={
        '': ['templates/*.html'],
    },
    install_requires=['Django>=1.11,<1.12', 'django-macaddress'],
)
