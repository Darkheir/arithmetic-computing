#!/usr/bin/env python
import logging
import sys

from arithmetic_computing.communication.server_socket import ServerSocket
from arithmetic_computing.helper.arguments_parser import ArgumentsParser
from arithmetic_computing.process.list_processing_callback import ListProcessingCallback
from arithmetic_computing.arithmetic.list_arithmetic_callback import ListArithmeticCallback

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    socket_address, processes = ArgumentsParser.parse_server_arguments()

    # Callback that calculate the string arithmetic operations
    # It will be called in multiple processes
    arithmetic_callback = ListArithmeticCallback()

    # Callback that will create processes and give them the arithmetic callback
    processor_callback = ListProcessingCallback(arithmetic_callback, processes)

    # Server that listen on socket
    server = ServerSocket(socket_address)

    try:
        # Serve. Each time the server receives some data it will call the processor callback
        server.serve(processor_callback)
    except KeyboardInterrupt:
        logging.warning("Keyboard interrupt, exiting")
        sys.exit(0)
