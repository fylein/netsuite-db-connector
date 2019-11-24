import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='netsuite-db-connector',
    version='0.0.2',
    author='Siva Narayanan',
    author_email='siva@fyle.in',
    description='Connects Xero to a database connector to transfer information to and fro',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['netsuite', 'api', 'python', 'sdk', 'sqlite'],
    url='https://github.com/fylein/netsuite-db-connector',
    packages=setuptools.find_packages(),
    install_requires=['netsuitesdk==1.0.1'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
