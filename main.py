from utils.colors import Colors
from utils.file_systems import FileSystem


def main():
    print("|--------------Welcome to the In-Memory File System--------------|")
    print("mkdir [directory_name]: Create a new directory.")
    print("ls: List files and directories in the current directory.")
    print("cd [path]: Change the current directory.")
    print("cat [file name]: Display the content of a file.")
    print("touch [file name]: Create a new file.")
    print("echo [file name] [text]: Write text to a file.")
    print("mv [source] [destination]: Move a file or directory.")
    print("cp [\"/\"source] [\"/\"destination]: Copy a file or directory.")
    print("rm [file_or_directory path]: Remove a file or directory.")
    print("grep [file_name] [pattern]: Search for a pattern in a file.")
    print("exit: Exit the file system.\n")

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
