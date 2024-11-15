import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QGridLayout, QMessageBox, QWidget
)
from virtual_disk import VirtualDisk
from file_system import FileSystem


class VirtualFileSystemApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize Virtual Disk and File System
        self.disk = VirtualDisk()
        self.fs = FileSystem(self.disk)

        # Set up the main window
        self.setWindowTitle("Virtual File System")
        self.setGeometry(300, 100, 400, 300)

        # Main Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Add Buttons
        self.status_label = QLabel("Status: Ready", self)
        layout.addWidget(self.status_label)

        layout.addWidget(QPushButton("Create Disk", self, clicked=self.create_disk))
        layout.addWidget(QPushButton("Mount Disk", self, clicked=self.mount_disk))
        layout.addWidget(QPushButton("Unmount Disk", self, clicked=self.unmount_disk))
        layout.addWidget(QPushButton("Create File", self, clicked=self.create_file))
        layout.addWidget(QPushButton("Open File", self, clicked=self.open_file))
        layout.addWidget(QPushButton("Write to File", self, clicked=self.write_file))
        layout.addWidget(QPushButton("Read File", self, clicked=self.read_file))
        layout.addWidget(QPushButton("Delete File", self, clicked=self.delete_file))
        layout.addWidget(QPushButton("Exit", self, clicked=self.close))

    def create_disk(self):
        if self.disk.create_disk():
            self.show_message("Success", "Disk created successfully!")
        else:
            self.show_message("Error", "Disk already exists!")

    def mount_disk(self):
        username, ok = self.simple_input_dialog("Mount Disk", "Enter username:")
        if ok and username:
            if self.disk.mount_disk(username):
                self.show_message("Success", "Disk mounted successfully!")
            else:
                self.show_message("Error", "Failed to mount disk!")

    def unmount_disk(self):
        if self.disk.unmount_disk():
            self.show_message("Success", "Disk unmounted successfully!")
        else:
            self.show_message("Error", "No disk is currently mounted!")

    def create_file(self):
        filename, ok = self.simple_input_dialog("Create File", "Enter filename:")
        if ok and filename:
            if self.fs.create_file(filename):
                self.show_message("Success", f"File '{filename}' created successfully!")
            else:
                self.show_message("Error", "Failed to create file!")

    def open_file(self):
        filename, ok = self.simple_input_dialog("Open File", "Enter filename:")
        if ok and filename:
            mode, ok_mode = self.simple_input_dialog("Open File", "Enter mode ('r' for read, 'w' for write):")
            if ok_mode and mode:
                fd = self.fs.open_file(filename, mode)
                if fd is not None:
                    self.show_message("Success", f"File '{filename}' opened with file descriptor {fd}!")
                else:
                    self.show_message("Error", "Failed to open file!")

    def write_file(self):
        fd, ok = self.simple_input_dialog("Write to File", "Enter file descriptor:")
        if ok and fd:
            data, ok_data = self.simple_input_dialog("Write to File", "Enter data to write:")
            if ok_data and data:
                if self.fs.write_file(int(fd), data):
                    self.show_message("Success", "Data written successfully!")
                else:
                    self.show_message("Error", "Failed to write to file!")

    def read_file(self):
        fd, ok = self.simple_input_dialog("Read File", "Enter file descriptor:")
        if ok and fd:
            data = self.fs.read_file(int(fd))
            if data:
                self.show_message("File Content", data)
            else:
                self.show_message("Error", "Failed to read file!")

    def delete_file(self):
        filename, ok = self.simple_input_dialog("Delete File", "Enter filename:")
        if ok and filename:
            if self.fs.delete_file(filename):
                self.show_message("Success", f"File '{filename}' deleted successfully!")
            else:
                self.show_message("Error", "Failed to delete file!")

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def simple_input_dialog(self, title, label):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)

        layout = QGridLayout(dialog)
        layout.addWidget(QLabel(label), 0, 0)
        input_field = QLineEdit(dialog)
        layout.addWidget(input_field, 0, 1)

        buttons = QDialog().add_buttons()
        layout.addWidget(buttons, 1, 0, 1, 2)

        ok = dialog.exec_()
        return input_field.text(), ok


# Main Application Entry Point
def main():
    app = QApplication(sys.argv)
    window = VirtualFileSystemApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
