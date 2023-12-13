import json
import os
from typing import List

from utils.colors import Colors
from utils.trie_node import TrieNode


class FileSystem:
    def __init__(self):
        self.root = TrieNode()
        self.path = '/'
        
    def get_desktop_path(self):
        # Get the path to the desktop folder
        return os.path.join(os.path.expanduser("~"), "Desktop")

    def save_state(self, filename='filesystem_state.json'):
        # Save the current state of the file system to a JSON file on the desktop
        desktop_path = self.get_desktop_path()
        file_path = os.path.join(desktop_path, filename)

        with open(file_path, 'w') as file:
            json.dump(self.root.to_dict(), file)

    def load_state(self, filename='filesystem_state.json'):
        # Load the file system state from a JSON file on the desktop
        desktop_path = self.get_desktop_path()
        file_path = os.path.join(desktop_path, filename)

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.root.from_dict(data)
        except FileNotFoundError:
            Colors.print_red(f"Error: File system state file not found on the desktop. ({file_path})")


    # Create a directory at the given path
    def mkdir(self, new_path: str):
        node = self.root.insert((self.path + new_path) if self.path == '/' else (self.path + '/' + new_path), False)

    # List directory or file
    def ls(self) -> List[str]:
        node = self.root.search(self.path)

        if node is None:
            return []
        if node.isFile:
            return [node.name]
        return sorted(node.children.keys())

    # Display the content of a file
    def cat(self, file):
        node = self.root.search((self.path + file) if self.path == '/' else (self.path + '/' + file))
        if node is None or not node.isFile:
            raise FileNotFoundError(f"File not found: {self.path + '/' + file}")
        return node.content

    # Create a new file at the given path
    def touch(self, file):
        self.root.insert((self.path + file) if self.path == '/' else (self.path + '/' + file), True)

    # Write a string to a file
    def echo(self, file, text):
        node = self.root.search((self.path + file) if self.path == '/' else (self.path + '/' + file))

        if node is None or not node.isFile:
            raise FileNotFoundError(f"File not found: {self.path + '/' + file}")

        node.content += ' '.join(text) + ' '

    def mv(self, src, dst):
        # Move a file or directory to a new destination
        src_node = self.root.search((self.path + src) if self.path == '/' else (self.path + '/' + src))
        dst_node = self.root.search((self.path + dst) if self.path == '/' else (self.path + '/' + dst))

        if src_node is None or dst_node is None:
            print("Invalid source or destination path.")
            return

        src_node.move(src_node, dst_node)

    def cp(self, src, dst):
        # Copy a file or directory to a new destination
        src_node = self.root.search((src) if src.startswith('/') else (self.path + '/' + src))
        dst_node = self.root.search((dst) if dst.startswith('/') else (self.path + '/' + dst))

        if src_node is None or dst_node is None:
            print("Invalid source or destination path.")
            return

        src_node.copy(src_node, dst_node)

    def rm(self, new_path):
        # Remove a file or directory
        node = self.root.search((self.path + new_path) if self.path == '/' else (self.path + '/' + new_path))

        if node is None:
            print("Invalid path.")
            return

        # If the node is a file, remove it directly
        if node.isFile:
            node.parent.remove(node.name)
        else:
            # If the node is a directory, check if it's empty before removing
            if not node.children:
                node.parent.remove(node.name)
            else:
                Colors.print_red(f"Directory not empty: {new_path}")

    def grep(self, file_path, pattern):
        # Search for a pattern in a file
        node = self.root.search((self.path + file_path) if self.path == '/' else (self.path + '/' + file_path))

        if node is None or not node.isFile:
            print("Invalid path.")
            return

        node.grep(pattern)

    def cd(self, new_path):
        if not new_path or new_path == '.':
            # No change in the current directory
            return
        elif new_path == '..':
            # Move to the parent directory
            if self.path != '/':
                parts = self.path.split('/')
                self.path = '/'.join(parts[:-1]) or '/'
        elif new_path == '/':
            # Move to the root directory
            self.path = '/'
        elif new_path.startswith('/'):
            # Navigate to the specified absolute path
            node = self.root.search(new_path)
            if node and node.isFile:
                print(f"{new_path} is a file. Cannot navigate to it.")
            elif node:
                self.path = new_path
            else:
                print(f"Directory not found: {new_path}")
        else:
            # Navigate relative to the current path
            new_path = (self.path + '/' + new_path).replace('//', '/')
            node = self.root.search(new_path)
            if node and node.isFile:
                print(f"{new_path} is a file. Cannot navigate to it.")
            elif node:
                self.path = new_path
            else:
                Colors.print_red(f"Directory not found: {new_path}")

        Colors.print_yellow(f"Current directory: {self.path}\n")
