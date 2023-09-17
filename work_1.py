import sys
from fs.tarfs import TarFS
s = ''

with TarFS(sys.argv[1]) as file:
    path = "/"
    while (s != "exit"):
        s = input('% ')
        if (s == "ls"):
            print(*file.listdir(path))
        elif (s[:3] == "cat"):
            if (file.isfile(path + '/' + s[4:])):
                print(file.readtext(path + '/' + s[4:]), end="")
            else:
                print("bad path")
        elif (s == "pwd"):
            print(path)
        elif (s[:2] == "cd"):
            if (s[3:] == "."):
                pass
            elif (s[3:] == ".."):
                tmp = path.split("/")
                path = "/".join(tmp[:-1])
                if (path == ""):
                    path = "/"
            elif (file.isdir(s[3:])):
                path += s[3:]
            else:
                print("bad command")
        elif (s != "exit"):
            print("bad command")
