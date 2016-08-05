# arithmetic-computing

[![Licence](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/?branch=master)
[![Code Coverage](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/?branch=master)
[![Build Status](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/badges/build.png?b=master)](https://scrutinizer-ci.com/g/Darkheir/arithmetic-computing/build-status/master)

A simple client/server system to compute arithmetic operations

The client is sending a list of arithmetic operations as strings that the server must calculate. The server will perform the arithmetic operations and then return the results as a list.

Unix socket are used to communicate between the client and the server.

The server is using multiple processes to speedup arithmetic operations.

## Installation

Since no dependencies are required to run this application it should be possible to run it directly from the git repository.

To install it as a python module the easiest way is to run the following command in the terminal once located in the git repo:

```python
python setup.py install
```


## Server side

### Usage

To launch the server run the following command:

```python
python server.py [-p PROCESSES] socket_address
```

Where:
* `-p` option is an integer between 1 and 10 representing the number of processes to launch to perform arithmetic operations.
* `socket_address` is the path to the  unix socket to use.

### Example

The following command will run the server with 4 processes on a socket located in `/tmp/arithmetic_socket`

```python
python server.py -p 4 /tmp/arithmetic_socket
```

## Client side

### Usage

To launch the client run the following command:

```python
python client.py operation_file result_file socket_address
```
Where:
* `operation_file` is a text file containing the arithmetic operations to compute
* `result_file` is the file path where the operations results will be written to
* `socket_address` is the path of the unix socket to use.

### Example

The following command will run the client with an operation file located in `~/misc/operations.txt` on a socket located in `/tmp/arithmetic_socket`. It will write the results in `results.txt`

```python
python client.py ~/misc/operations.txt results.txt /tmp/arithmetic_socket
```
