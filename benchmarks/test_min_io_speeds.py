"""
This module foo.
"""

import unittest

# Standard lib imports
import tempfile
from pathlib import Path
import timeit

# Addon imports
import humanfriendly as hf

FNAME = 'file_to_read'

QUITE_BIG = int(1e9)


class Foo(unittest.TestCase):


    def setUp(self):
        # A working directory that gets automatically cleaned up.
        self.dir = tempfile.TemporaryDirectory()

        # Make a file we can read back in later.
        self.file_to_read = Path(self.dir.name).joinpath(FNAME)
        with self.file_to_read.open('w+b') as f:
            f.write(b'\x00' * QUITE_BIG)


    def tearDown(self):
        self.dir.cleanup()


    """ 
    Bar
    """
    def test_something(self):
        in_mem_data_to_write = b'\x00' * QUITE_BIG
        file = Path(self.dir.name).joinpath(FNAME)

        def writing_operation():
            nonlocal file
            with file.open('w+b') as f:
                f.write(in_mem_data_to_write)

        def reading_operation():
            nonlocal file
            with file.open() as f:
                bytes_read = f.read()

        time_to_write = timeit.timeit(writing_operation, number = 1)
        time_to_read = timeit.timeit(reading_operation, number = 1)
        print('Seconds to open and write a %s file: %s' % 
            (hf.format_size(QUITE_BIG), time_to_write))
        print('Seconds to open and read a %s file: %s' % 
            (hf.format_size(QUITE_BIG), time_to_read))



if __name__ == '__main__':
    unittest.main()
