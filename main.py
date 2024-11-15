# main.py

from rich.console import Console
from rich.table import Table
from virtual_disk import VirtualDisk
from file_system import FileSystem
import cli_commands

console = Console()

def display_commands():
    table = Table(title="Available Commands", show_header=True, header_style="bold magenta")
    table.add_column("Command", style="bold cyan")
    table.add_column("Description", style="bold green")

    commands = {
        "create_disk": "Create a new virtual disk",
        "mount_disk": "Mount the virtual disk",
        "unmount_disk": "Unmount the virtual disk",
        "create_file": "Create a new file",
        "open_file": "Open an existing file",
        "close_file": "Close an open file descriptor",
        "write_file": "Write data to an open file",
        "read_file": "Read data from an open file",
        "delete_file": "Delete a file",
        "exit": "Exit the program",
    }

    for cmd, desc in commands.items():
        table.add_row(cmd, desc)

    console.print(table)

def main():
    disk = VirtualDisk()
    fs = FileSystem(disk)

    while True:
        display_commands()
        cmd = console.input("[bold magenta]Enter command: [/]")
        try:
            if cmd == "create_disk":
                cli_commands.cli_create_disk(disk)
            elif cmd == "mount_disk":
                cli_commands.cli_mount_disk(disk)
            elif cmd == "unmount_disk":
                cli_commands.cli_unmount_disk(disk)
            elif cmd == "create_file":
                cli_commands.cli_create_file(fs)
            elif cmd == "open_file":
                cli_commands.cli_open_file(fs)
            elif cmd == "close_file":
                cli_commands.cli_close_file(fs)
            elif cmd == "write_file":
                cli_commands.cli_write_file(fs)
            elif cmd == "read_file":
                cli_commands.cli_read_file(fs)
            elif cmd == "delete_file":
                cli_commands.cli_delete_file(fs)
            elif cmd == "exit":
                console.print("[bold cyan]Exiting the program. Goodbye![/]")
                break
            else:
                console.print("[bold red]Invalid command! Please try again.[/]")
        except Exception as e:
            console.print(f"[bold red]An error occurred: {e}[/]")

if __name__ == "__main__":
    main()
