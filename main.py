import json
import os
from typing import List

class Colors:
    @staticmethod
    def print_yellow(text):
        print("\033[93m" + text + "\033[0m")  # ANSI escape code for yellow

    @staticmethod
    def print_red(text):
        print("\033[91m" + text + "\033[0m")  # ANSI escape code for red

class TrieNode:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.isFile = False
        self.content = ""
        
    def to_dict(self):
        # Convert TrieNode and its children to a dictionary
        return {
            "name": self.name,
            "isFile": self.isFile,
            "content": self.content,
            "children": {name: child.to_dict() for name, child in self.children.items()}
        }

    def from_dict(self, data, parent=None):
        # Recreate TrieNode and its children from a dictionary
        self.name = data["name"]
        self.isFile = data["isFile"]
        self.content = data["content"]
        self.parent = parent
        self.children = {name: TrieNode().from_dict(child_data, parent=self) for name, child_data in data["children"].items()}
        return self

    def insert(self, path: str, is_file: bool) -> 'TrieNode':
        # Insert a path into the Trie and return the final node
        node = self
        parts = path.split('/')
        for part in parts[1:]:
            if part not in node.children:
                node.children[part] = TrieNode(name=part, parent=node)
            node = node.children[part]

        node.isFile = is_file

        if is_file:
            node.name = parts[-1]

        return node

    def search(self, path: str) -> 'TrieNode':
        # Search for a node given a path in the Trie
        node = self

        if path == '/':
            return node

        parts = path.split('/')

        for part in parts[1:]:
            if part not in node.children:
                return None
            node = node.children[part]

        return node

    def move(self, src: 'TrieNode', dst: 'TrieNode'):
        # Move a file to a new directory
        if not src or not dst:
            return

        # Remove the node from the source parent
        del src.parent.children[src.name]

        # Update the parent reference for the moved node
        src.parent = dst

        # Add the node to the destination parent
        dst.children[src.name] = src


    def copy(self, src: 'TrieNode', dst: 'TrieNode'):
        # Copy a file to a new directory
        if not src or not dst:
            Colors.print_red("Error: Invalid source or destination path.")
            return

        # Create a new node for the destination
        dst.children[src.name] = TrieNode(name=src.name, parent=dst)

        # Copy content and properties
        dst.children[src.name].content = src.content
        dst.children[src.name].isFile = src.isFile
        dst.children[src.name].children = src.children.copy()


    def remove(self, name: str):
        # Remove a file or directory
        if not name or name not in self.children:
            return

        del self.children[name]

    def grep(self, pattern: str):
        # Find a string in a file
        if not pattern or not self.isFile:
            return

        if pattern in self.content:
            Colors.print_yellow(f"Pattern '{pattern}' found in {self.name}")
            
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
        src_node = self.root.search(src)
        dst_node = self.root.search(dst)

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


def main():
    print("|--------------Welcome to the In-Memory File System--------------|")
    print("List of Commands: mkdir, ls, cd, cat, touch, echo, mv, cp, rm, grep")
    print("Type 'exit' to exit the program\n")

    fs = FileSystem()
    
    fs.load_state()
    
    Colors.print_yellow(f"Current directory: {fs.path}\n")

    while True:
        cmd = input().split()

        if not cmd:
            print("Please enter a command")
            continue

        if cmd[0] == 'exit':
            break

        if cmd[0] == 'mkdir':
            fs.mkdir(cmd[1])

        elif cmd[0] == 'ls':
            children = fs.ls()
            print(children)

        elif cmd[0] == 'cd':
            fs.cd(cmd[1])

        elif cmd[0] == 'cat':
            content = fs.cat(cmd[1])
            print(content)

        elif cmd[0] == 'touch':
            fs.touch(cmd[1])

        elif cmd[0] == 'echo':
            fs.echo(cmd[1], cmd[2:])

        elif cmd[0] == 'mv':
            fs.mv(cmd[1], cmd[2])

        elif cmd[0] == 'cp':
            fs.cp(cmd[1], cmd[2])

        elif cmd[0] == 'rm':
            fs.rm(cmd[1])

        elif cmd[0] == 'grep':
            fs.grep(cmd[1], cmd[2])

        else:
            print("Invalid command")
    
    fs.save_state()


main()
