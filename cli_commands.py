# cli_commands.py

def cli_create_disk(disk):
    disk.create_disk()

def cli_mount_disk(disk):
    username = input("Enter username: ")
    disk.mount_disk(username)

def cli_unmount_disk(disk):
    disk.unmount_disk()

def cli_create_file(fs):
    filename = input("Enter filename (use numbers for simplicity): ")
    fs.create_file(filename)

def cli_open_file(fs):
    filename = input("Enter filename (inode number): ")
    mode = input("Enter mode ('r' for read, 'w' for write): ")
    fd = fs.open_file(filename, mode)
    if fd is not None:
        print(f"File descriptor: {fd}")

def cli_close_file(fs):
    fd = int(input("Enter file descriptor: "))
    fs.close_file(fd)

def cli_write_file(fs):
    fd = int(input("Enter file descriptor: "))
    data = input("Enter data to write: ")
    fs.write_file(fd, data)

def cli_read_file(fs):
    fd = int(input("Enter file descriptor: "))
    data = fs.read_file(fd)
    if data is not None:
        print(f"Data read:\n{data}")

def cli_delete_file(fs):
    filename = input("Enter filename (inode number): ")
    fs.delete_file(filename)
