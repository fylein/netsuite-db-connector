import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='netsuite-db-connector',
    version='0.3.0',
    author='Siva Narayanan',
    author_email='siva@fyle.in',
    description='Connects NetSuite to a database connector to transfer information to and fro',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['netsuite', 'api', 'python', 'sdk', 'sqlite'],
    url='https://github.com/fylein/netsuite-db-connector',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['netsuitesdk==2.6.1'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
