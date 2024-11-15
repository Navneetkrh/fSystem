# superblock.py

import struct

class Superblock:
    def __init__(self, total_inodes, total_blocks):
        self.total_inodes = total_inodes
        self.total_blocks = total_blocks
        self.free_inodes = list(range(1, total_inodes + 1))
        self.free_blocks = list(range(total_inodes + 1, total_blocks + 1))
        self.inode_start = 1
        self.data_block_start = total_inodes + 1

    def serialize(self):
        data = struct.pack('I', self.total_inodes)
        data += struct.pack('I', self.total_blocks)
        data += struct.pack('{}I'.format(len(self.free_inodes)), *self.free_inodes)
        data += struct.pack('{}I'.format(len(self.free_blocks)), *self.free_blocks)
        data += struct.pack('I', self.inode_start)
        data += struct.pack('I', self.data_block_start)
        return data

    @staticmethod
    def deserialize(data):
        offset = 0
        total_inodes = struct.unpack_from('I', data, offset)[0]
        offset += 4
        total_blocks = struct.unpack_from('I', data, offset)[0]
        offset += 4
        free_inodes_len = total_inodes
        free_inodes = list(struct.unpack_from('{}I'.format(free_inodes_len), data, offset))
        offset += 4 * free_inodes_len
        free_blocks_len = total_blocks - total_inodes
        free_blocks = list(struct.unpack_from('{}I'.format(free_blocks_len), data, offset))
        offset += 4 * free_blocks_len
        inode_start = struct.unpack_from('I', data, offset)[0]
        offset += 4
        data_block_start = struct.unpack_from('I', data, offset)[0]
        return Superblock(total_inodes, total_blocks)
