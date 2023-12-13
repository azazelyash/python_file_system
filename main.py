from utils.colors import Colors
from utils.file_systems import FileSystem


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
