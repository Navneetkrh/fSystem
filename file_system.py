# file_system.py

import datetime
from inode import Inode
from virtual_disk import BLOCK_SIZE

class FileSystem:
    def __init__(self, disk):
        self.disk = disk
        self.fd_table = {}
        self.fd_count = 0

    def create_file(self, filename):
        if not self.disk.mounted:
            print("Disk is not mounted.")
            return False

        # Allocate inode
        inode_number = self.disk.allocate_inode()
        if not inode_number:
            return False

        # Initialize inode
        inode = Inode()
        inode.file_size = 0
        inode.file_type = 'file'
        inode.owner = self.disk.current_user

        # Update inode table
        self.disk.inode_table[inode_number] = inode

        # Simulate adding file to root directory (not implemented)
        print(f"File '{filename}' created with inode {inode_number}.")
        return True

    def open_file(self, filename, mode):
        if not self.disk.mounted:
            print("Disk is not mounted.")
            return None
 
        # Find inode number by filename (simplified, assuming filename is inode number) ggh
        try:
            inode_number = int(filename)
            inode = self.disk.inode_table[inode_number]
        except (ValueError, KeyError):
            print("File not found.")
            return None

        # Assign file descriptor
        fd = self.fd_count
        self.fd_table[fd] = {
            'inode_number': inode_number,
            'mode': mode,
            'offset': 0
        }
        self.fd_count += 1

        print(f"File '{filename}' opened with file descriptor {fd}.")
        return fd

    def close_file(self, fd):
        if fd in self.fd_table:
            del self.fd_table[fd]
            print(f"File descriptor {fd} closed.")
            return True
        else:
            print("Invalid file descriptor.")
            return False

    def write_file(self, fd, data):
        if fd not in self.fd_table:
            print("Invalid file descriptor.")
            return False

        file_info = self.fd_table[fd]
        inode_number = file_info['inode_number']
        inode = self.disk.inode_table[inode_number]

        # Allocate data block if necessary
        block_number = self.disk.allocate_block()
        if not block_number:
            return False

        # Write data
        block_offset = self.calculate_block_offset(block_number)
        self.disk.disk.seek(block_offset)
        self.disk.disk.write(data.encode('utf-8').ljust(BLOCK_SIZE, b'\x00'))

        # Update inode
        inode.direct_pointers[0] = block_number
        inode.file_size = len(data)
        inode.timestamps['modified'] = datetime.datetime.now()

        print(f"Wrote data to file descriptor {fd}.")
        return True

    def read_file(self, fd):
        if fd not in self.fd_table:
            print("Invalid file descriptor.")
            return None

        file_info = self.fd_table[fd]
        inode_number = file_info['inode_number']
        inode = self.disk.inode_table[inode_number]

        # Read data from data blocks
        data = b''
        for ptr in inode.direct_pointers:
            if ptr:
                block_offset = self.calculate_block_offset(ptr)
                self.disk.disk.seek(block_offset)
                block_data = self.disk.disk.read(BLOCK_SIZE)
                data += block_data

        # Update access time
        inode.timestamps['accessed'] = datetime.datetime.now()

        print(f"Read data from file descriptor {fd}.")
        return data[:inode.file_size].decode('utf-8')

    def delete_file(self, filename):
        if not self.disk.mounted:
            print("Disk is not mounted.")
            return False

        # Find inode number by filename (simplified)
        try:
            inode_number = int(filename)
            inode = self.disk.inode_table[inode_number]
        except (ValueError, KeyError):
            print("File not found.")
            return False

        # Free data blocks
        for ptr in inode.direct_pointers:
            if ptr:
                self.disk.free_block(ptr)

        # Free inode
        self.disk.free_inode(inode_number)
        del self.disk.inode_table[inode_number]

        # Simulate removing file from root directory (not implemented)
        print(f"File '{filename}' deleted.")
        return True

    def calculate_block_offset(self, block_number):
        # Calculate the byte offset of a data block in the disk file
        offset = self.disk.superblock_size() + self.disk.inode_size() * self.disk.superblock.total_inodes
        offset += (block_number - self.disk.superblock.data_block_start) * BLOCK_SIZE
        return offset
