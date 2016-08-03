import os
import logging


class FileAccess(object):
    """Class that handles access to files on the disk.
    """

    @staticmethod
    def read_lines(path):
        """Read the lines in the given helper and returns them as a list

        :param path: Path of the helper to read from
        :type path: str
        :return: List of lines contained in the helper
        :rtype: list[str]
        """
        logger = logging.getLogger(__name__)
        path = os.path.expanduser(path)
        path = os.path.abspath(path)

        if not os.path.isfile(path):
            error = "File %s doesn't exist" % path
            logger.error(error)
            raise IOError(error)

        # Read helper and remove new line chars
        logger.info("Reading content of %s", path)
        with open(path, "r") as text_file:
            operations_lines = text_file.read().splitlines()

        return operations_lines

    @staticmethod
    def write_lines(path, data):
        """Write the given list into the given helper.

        Each element of the list will be on a different line

        :param path: Path of the helper to write to
        :type path: str
        :param data: List of string to write in the helper
        :type data: list[str]
        """
        logger = logging.getLogger(__name__)
        path = os.path.expanduser(path)
        path = os.path.abspath(path)

        logger.info("Writing data into %s", path)
        with open(path, "w") as text_file:
            text_file.write("\n".join(data) + "\n")
