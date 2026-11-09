import unittest

from listkit.seq import chunk


class ChunkTest(unittest.TestCase):
    def test_last_chunk_may_be_short(self):
        self.assertEqual(chunk([1, 2, 3], 2), [[1, 2], [3]])
