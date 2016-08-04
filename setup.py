from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries',
]

setup(
    name='arithmetic_computing',
    author='Raphael Cohen',
    author_email='raphael.cohen.utt@gmail.com',
    url='https://github.com/darkheir/arithmetic-computing',
    version='0.0.1',
    classifiers=classifiers,
    description='A simple client/server system to compute arithmetic operations',
    long_description=open('README.md').read(),
    keywords='server process arithmetic',
    packages=find_packages(include=('arithmetic_computing*',)),
    include_package_data=True,
    license='MIT',
    scripts=['client.py', 'server.py'],
)
