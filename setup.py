import setuptools

setuptools.setup(
    name='oi_bus',
    version='0.2.0',
    packages=setuptools.find_packages(),
    package_data={
        '': ['templates/*.html', 'locale/*/LC_MESSAGES/*.po', 'locale/*/LC_MESSAGES/*.mo', 'static/*.css'],
    },
    include_package_data=True,
    install_requires=[
        'Django>=1.11,<1.12',
        'django-macaddress',
        'click>=7,<8',
        'qrcode>=6,<7',
    ],
    entry_points='''
        [console_scripts]
        oi=oi_bus.oi:main
    ''',
)
