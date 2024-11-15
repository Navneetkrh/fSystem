# inode.py

import struct
import datetime

class Inode:
    def __init__(self):
        self.file_size = 0
        self.file_type = 'file'  # 'file' or 'directory'
        self.permissions = 0o755
        self.owner = ''
        self.timestamps = {
            'created': datetime.datetime.now(),
            'modified': datetime.datetime.now(),
            'accessed': datetime.datetime.now()
        }
        self.direct_pointers = [None] * 10
        self.single_indirect = None
        self.double_indirect = None

    def serialize(self):
        data = struct.pack('I', self.file_size)
        data += struct.pack('I', 1 if self.file_type == 'file' else 2)
        data += struct.pack('I', self.permissions)
        data += struct.pack('16s', self.owner.encode('utf-8'))
        data += struct.pack('d', self.timestamps['created'].timestamp())
        data += struct.pack('d', self.timestamps['modified'].timestamp())
        data += struct.pack('d', self.timestamps['accessed'].timestamp())
        for ptr in self.direct_pointers:
            data += struct.pack('I', ptr if ptr else 0)
        data += struct.pack('I', self.single_indirect if self.single_indirect else 0)
        data += struct.pack('I', self.double_indirect if self.double_indirect else 0)
        return data

    @staticmethod
    def deserialize(data):
        inode = Inode()
        offset = 0
        inode.file_size = struct.unpack_from('I', data, offset)[0]
        offset += 4
        file_type_code = struct.unpack_from('I', data, offset)[0]
        inode.file_type = 'file' if file_type_code == 1 else 'directory'
        offset += 4
        inode.permissions = struct.unpack_from('I', data, offset)[0]
        offset += 4
        inode.owner = struct.unpack_from('16s', data, offset)[0].decode('utf-8').rstrip('\x00')
        offset += 16
        inode.timestamps['created'] = datetime.datetime.fromtimestamp(struct.unpack_from('d', data, offset)[0])
        offset += 8
        inode.timestamps['modified'] = datetime.datetime.fromtimestamp(struct.unpack_from('d', data, offset)[0])
        offset += 8
        inode.timestamps['accessed'] = datetime.datetime.fromtimestamp(struct.unpack_from('d', data, offset)[0])
        offset += 8
        inode.direct_pointers = []
        for _ in range(10):
            ptr = struct.unpack_from('I', data, offset)[0]
            inode.direct_pointers.append(ptr if ptr != 0 else None)
            offset += 4
        inode.single_indirect = struct.unpack_from('I', data, offset)[0]
        inode.single_indirect = inode.single_indirect if inode.single_indirect != 0 else None
        offset += 4
        inode.double_indirect = struct.unpack_from('I', data, offset)[0]
        inode.double_indirect = inode.double_indirect if inode.double_indirect != 0 else None
        return inode
