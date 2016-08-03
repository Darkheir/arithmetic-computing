import argparse


class ArgumentsParser(object):
    """Class that handles parsing of command line arguments
    for both client and server.
    """

    @staticmethod
    def parse_client_arguments():
        """Parse client arguments
        :return: Parsed arguments
        :rtype: tuple[string]
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("operation_file", help="File containing the operations to calculate")
        parser.add_argument("result_file", help="File to write the results to")
        parser.add_argument("socket_address", help="Socket to use to communicate with the server")
        args = parser.parse_args()
        return args.operation_file, args.result_file, args.socket_address

    @staticmethod
    def parse_server_arguments():
        """Parse server arguments

        :return: Parsed arguments
        :rtype: tuple[mixed]
        """
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("socket_address", help="Socket to use to communicate with the server")
        parser.add_argument("-p", "--processes", type=ArgumentsParser.check_processes, default=4,
                            help="Number of processes to start to run arithmetic. Maximum is 10")
        args = parser.parse_args()
        return args.socket_address, args.processes

    @staticmethod
    def check_processes(value):
        """Check the processes value.

        The processes value must be between 1 and 10.
        Since this method is added as a type in the ArgumentParser
        it must also cast the string into an int.

        :param value: Value to check
        :type value: str
        :return: Value casted as an int
        :rtype: int
        """
        processes = int(value)
        if processes < 1 or processes > 10:
            raise argparse.ArgumentTypeError("%s is an invalid int value between 1 and 10" % value)
        return processes
