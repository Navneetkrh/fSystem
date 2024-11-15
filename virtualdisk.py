# virtual_disk.py

import os
from getpass import getpass
from superblock import Superblock
from inode import Inode

BLOCK_SIZE = 1024        # Size of each block in bytes
TOTAL_BLOCKS = 10240     # Total number of blocks in the disk
TOTAL_INODES = 512       # Total number of inodes
DISK_FILE = 'virtual_disk.vdsk'

class VirtualDisk:
    def __init__(self, disk_file=DISK_FILE):
        self.disk_file = disk_file
        self.superblock = None
        self.inode_table = {}
        self.open_files = {}
        self.mounted = False
        self.current_user = None

    def create_disk(self):
        # Check if disk file already exists
        if os.path.exists(self.disk_file):
            print("Disk already exists.")
            return False

        # Create disk file and initialize it
        with open(self.disk_file, 'wb') as f:
            # Initialize superblock
            self.superblock = Superblock(TOTAL_INODES, TOTAL_BLOCKS)
            f.write(self.superblock.serialize())

            # Initialize inodes
            empty_inode = Inode().serialize()
            for _ in range(self.superblock.total_inodes):
                f.write(empty_inode)

            # Initialize data blocks
            empty_block = b'\x00' * BLOCK_SIZE
            for _ in range(self.superblock.total_blocks - self.superblock.total_inodes):
                f.write(empty_block)

        print("Disk created successfully.")
        return True

    def mount_disk(self, username):
        # Check if disk file exists
        if not os.path.exists(self.disk_file):
            print("Disk does not exist.")
            return False

        # Prompt for password (authentication not implemented in this example)
        password = getpass("Enter password: ")

        # Open disk file
        self.disk = open(self.disk_file, 'r+b')

        # Load superblock
        self.disk.seek(0)
        sb_data = self.disk.read(self.superblock_size())
        self.superblock = Superblock.deserialize(sb_data)

        # Load inodes
        self.inode_table = {}
        for i in range(1, self.superblock.total_inodes + 1):
            inode_data = self.read_inode_data(i)
            inode = Inode.deserialize(inode_data)
            self.inode_table[i] = inode

        self.mounted = True
        self.current_user = username
        print("Disk mounted successfully.")
        return True

    def unmount_disk(self):
        if not self.mounted:
            print("Disk is not mounted.")
            return False

        # Write back inodes
        for inode_number, inode in self.inode_table.items():
            self.write_inode_data(inode_number, inode.serialize())

        # Write back superblock
        self.disk.seek(0)
        self.disk.write(self.superblock.serialize())

        # Close disk file
        self.disk.close()
        self.mounted = False
        self.current_user = None
        print("Disk unmounted successfully.")
        return True

    def superblock_size(self):
        inode_list_size = 4 * self.superblock.total_inodes
        block_list_size = 4 * (self.superblock.total_blocks - self.superblock.total_inodes)
        return 4 * 2 + inode_list_size + block_list_size + 4 * 2

    def read_inode_data(self, inode_number):
        inode_size = self.inode_size()
        offset = self.superblock_size() + (inode_number - 1) * inode_size
        self.disk.seek(offset)
        return self.disk.read(inode_size)

    def write_inode_data(self, inode_number, data):
        inode_size = self.inode_size()
        offset = self.superblock_size() + (inode_number - 1) * inode_size
        self.disk.seek(offset)
        self.disk.write(data)

    def inode_size(self):
        size = 4 + 4 + 4 + 16 + 8 * 3 + 4 * 10 + 4 * 2
        return size

    def allocate_block(self):
        if not self.superblock.free_blocks:
            print("No free data blocks available.")
            return None
        block_number = self.superblock.free_blocks.pop(0)
        return block_number

    def free_block(self, block_number):
        self.superblock.free_blocks.append(block_number)

    def allocate_inode(self):
        if not self.superblock.free_inodes:
            print("No free inodes available.")
            return None
        inode_number = self.superblock.free_inodes.pop(0)
        return inode_number

    def free_inode(self, inode_number):
        self.superblock.free_inodes.append(inode_number)
