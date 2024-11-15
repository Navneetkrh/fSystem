# main.py

import sys
from virtual_disk import VirtualDisk
from file_system import FileSystem
import cli_commands

def main():
    disk = VirtualDisk()
    fs = FileSystem(disk)

    commands = {
        'create_disk': lambda: cli_commands.cli_create_disk(disk),
        'mount_disk': lambda: cli_commands.cli_mount_disk(disk),
        'unmount_disk': lambda: cli_commands.cli_unmount_disk(disk),
        'create_file': lambda: cli_commands.cli_create_file(fs),
        'open_file': lambda: cli_commands.cli_open_file(fs),
        'close_file': lambda: cli_commands.cli_close_file(fs),
        'write_file': lambda: cli_commands.cli_write_file(fs),
        'read_file': lambda: cli_commands.cli_read_file(fs),
        'delete_file': lambda: cli_commands.cli_delete_file(fs),
        'exit': sys.exit
    }

    while True:
        print("\nCommands: create_disk, mount_disk, unmount_disk, create_file, open_file, close_file, write_file, read_file, delete_file, exit")
        cmd = input("Enter command: ")
        if cmd in commands:
            commands[cmd]()
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
