# In Memory File System

Welcome to the In-Memory File System! This project provides a simple in-memory file system implemented in Python. Users can interact with the file system using various commands to perform operations like creating directories, listing files, moving, copying, and more.

## List of Commands

- mkdir [directory_name]: Create a new directory.
- ls: List files and directories in the current directory.
- cd [path]: Change the current directory.
- cat [file_name]: Display the content of a file.
- touch [file_name]: Create a new file.
- echo [file_name] [text]: Write text to a file.
- mv [source] [destination]: Move a file or directory.
- cp ["/"source] ["/"destination]: Copy a file or directory.
- rm [file_or_directory]: Remove a file or directory.
- grep [file_name] [pattern]: Search for a pattern in a file.
- exit: Exit the file system.

## Features

- Saves the state, so that when you restart your program all the changes remain persistant
- Create, delete, and navigate directories.
- Create, read, update, and delete files.
- Move and copy files and directories.
- Search for patterns within files.

## Video Demo

<img src="InMemoryFileSytem.gif" alt="Video Demo">

## Bug Fix

If your state is not managed then check you desktop directory location and if it is different than ``` C:\Users\{USER}\Desktop ``` then in file_systems.py, on line 16 add the change before "Desktop", for example ``` some_folder_name/OneDrive/Desktop ```.
