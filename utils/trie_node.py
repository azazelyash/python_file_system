from typing import List

from utils.colors import Colors

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