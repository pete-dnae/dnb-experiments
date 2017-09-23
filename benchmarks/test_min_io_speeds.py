"""
This module foo.
"""


# Standard lib imports
import unittest
import tempfile
from pathlib import Path
import timeit
import sys
import shutil
from functools import partial

# Addon imports
import humanfriendly as hf

FNAME = 'file_to_read'

QUITE_BIG = int(3e9)


class Foo(unittest.TestCase):


    def setUp(self):
        # A working directory that gets automatically cleaned up.
        self.dir = tempfile.TemporaryDirectory()
        self.dname = self.dir.name


    def tearDown(self):
        self.dir.cleanup()


    """ 
    Bar
    """
    def test_something(self):
        in_mem_data_to_write = b'\x00' * QUITE_BIG
        file = Path(self.dname).joinpath(FNAME)

        def write_op(f):
            with f.open('w+b') as f:
                f.write(in_mem_data_to_write)

        def read_op(f):
            bytes_read = self._read_file_into_mem(f)

        def copy_op(f):
            dest = Path(self.dname).joinpath('copied_file').as_posix()
            shutil.copyfile(f.as_posix(), dest)

        def iter_op(bytes):
            for byte in bytes:
                pointless = byte | 0xFF


        time_to_write = timeit.timeit(partial(write_op, file), number = 1)
        time_to_read = timeit.timeit(partial(read_op, file), number = 1)
        time_to_copy = timeit.timeit(partial(copy_op, file), number = 1)

        bytes = self._read_file_into_mem(file)
        time_to_iter = timeit.timeit(partial(iter_op, bytes), number = 1)

        print('Seconds to open and write a %s file:  %s' % 
            (hf.format_size(QUITE_BIG), time_to_write))
        print('Seconds to open and read a %s file:   %s' % 
            (hf.format_size(QUITE_BIG), time_to_read))
        print('Seconds to copy a %s file:            %s' % 
            (hf.format_size(QUITE_BIG), time_to_copy))
        print('Seconds to iterate through a %s file: %s' % 
            (hf.format_size(QUITE_BIG), time_to_iter))


    def _read_file_into_mem(self, fname):
        with fname.open('rb') as f:
            bytes_read = f.read()
        return bytes_read


if __name__ == '__main__':
    unittest.main()
