import setuptools

setuptools.setup(
    name='oi_bus',
    version='0.1.6',
    packages=setuptools.find_packages(),
    package_data={
        '': ['templates/*.html', 'locale/*/LC_MESSAGES/*.po', 'locale/*/LC_MESSAGES/*.mo', 'static/*.css'],
    },
    install_requires=['Django>=1.11,<1.12', 'django-macaddress'],
)
