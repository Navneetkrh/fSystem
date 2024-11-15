# cli_commands.py

from rich.console import Console
from rich.table import Table

console = Console()

def cli_create_disk(disk):
    console.print("[bold green]Creating disk...[/]")
    success = disk.create_disk()
    if success:
        console.print("[bold green]Disk created successfully![/]")
    else:
        console.print("[bold red]Disk already exists![/]")

def cli_mount_disk(disk):
    console.print("[bold green]Mounting disk...[/]")
    username = console.input("[bold blue]Enter username: [/]")
    success = disk.mount_disk(username)
    if success:
        console.print("[bold green]Disk mounted successfully![/]")
    else:
        console.print("[bold red]Failed to mount disk![/]")

def cli_unmount_disk(disk):
    console.print("[bold green]Unmounting disk...[/]")
    success = disk.unmount_disk()
    if success:
        console.print("[bold green]Disk unmounted successfully![/]")
    else:
        console.print("[bold red]No disk mounted![/]")

def cli_create_file(fs):
    console.print("[bold green]Creating file...[/]")
    filename = console.input("[bold blue]Enter filename (use numbers for simplicity): [/]")
    success = fs.create_file(filename)
    if success:
        console.print(f"[bold green]File '{filename}' created successfully![/]")
    else:
        console.print("[bold red]Failed to create file![/]")

def cli_open_file(fs):
    console.print("[bold green]Opening file...[/]")
    filename = console.input("[bold blue]Enter filename (inode number): [/]")
    mode = console.input("[bold blue]Enter mode ('r' for read, 'w' for write): [/]")
    fd = fs.open_file(filename, mode)
    if fd is not None:
        console.print(f"[bold green]File '{filename}' opened with file descriptor {fd}![/]")
    else:
        console.print("[bold red]Failed to open file![/]")

def cli_close_file(fs):
    console.print("[bold green]Closing file...[/]")
    fd = int(console.input("[bold blue]Enter file descriptor: [/]"))
    success = fs.close_file(fd)
    if success:
        console.print(f"[bold green]File descriptor {fd} closed successfully![/]")
    else:
        console.print("[bold red]Invalid file descriptor![/]")

def cli_write_file(fs):
    console.print("[bold green]Writing to file...[/]")
    fd = int(console.input("[bold blue]Enter file descriptor: [/]"))
    data = console.input("[bold blue]Enter data to write: [/]")
    success = fs.write_file(fd, data)
    if success:
        console.print("[bold green]Data written successfully![/]")
    else:
        console.print("[bold red]Failed to write to file![/]")

def cli_read_file(fs):
    console.print("[bold green]Reading file...[/]")
    fd = int(console.input("[bold blue]Enter file descriptor: [/]"))
    data = fs.read_file(fd)
    if data is not None:
        console.print(f"[bold green]Data read:[/]\n{data}")
    else:
        console.print("[bold red]Failed to read file![/]")

def cli_delete_file(fs):
    console.print("[bold green]Deleting file...[/]")
    filename = console.input("[bold blue]Enter filename (inode number): [/]")
    success = fs.delete_file(filename)
    if success:
        console.print(f"[bold green]File '{filename}' deleted successfully![/]")
    else:
        console.print("[bold red]Failed to delete file![/]")
