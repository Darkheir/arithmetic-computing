# arithmetic-computing

[![Licence](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/?branch=master)
[![Code Coverage](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/?branch=master)
[![Build Status](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/badges/build.png?b=master)](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/build-status/master)

A simple client/server system to compute arithmetic operations

The client is sending a list of arithmetic operations as strings that the server must calculate. The server will perform the arithmetic operations and then return the results as a list.

Unix socket are used to communicate between the client and the server.

The server is using multiple processes to speedup arithmetic operations.

## Requirements

Python 2.7 is the only supported version.
No external python modules are needed to run this programm.

For tests one module must be installed: `mock`. Another is optional and may be installed to check tests coverage: `coverage`.

## Installation

Since no dependencies are required to run this application it should be possible to run it directly from the git repository.

To install it as a python module the easiest way is to run the following command in the terminal once located in the git repo:

```bash
python setup.py install
```

## Testing

To run tests the easiest way is type the following command once in the git repository:

```bash
python setup.py test
```
It should automatically install tests dependencies (covarage and mock) and run all tests.

Another way is to type:

```bash
python -m unittest discover
```

To display code coverage tests may be run using the following command:

```bash
coverage run -m unittest discover
```

The report can be displayed by typing:

```bash
coverage report
```

## Usage

### Server side


To launch the server run the following command:

```bash
python server.py [-p PROCESSES] socket_address
```

Where:
* `-p` option is an integer between 1 and 10 representing the number of processes to launch to perform arithmetic operations.
* `socket_address` is the path to the  unix socket to use.

#### Example

The following command will run the server with 4 processes on a socket located in `/tmp/arithmetic_socket`

```bash
python server.py -p 4 /tmp/arithmetic_socket
```

### Client side

To launch the client run the following command:

```bash
python client.py operation_file result_file socket_address
```
Where:
* `operation_file` is a text file containing the arithmetic operations to compute
* `result_file` is the file path where the operations results will be written to
* `socket_address` is the path of the unix socket to use.

#### Example

The following command will run the client with an operation file located in `~/misc/operations.txt` on a socket located in `/tmp/arithmetic_socket`. It will write the results in `results.txt`

```bash
python client.py ~/misc/operations.txt results.txt /tmp/arithmetic_socket
```
