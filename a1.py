# Jaziel Herrera
# jazielh@uci.edu

from pathlib import Path
import shlex

def create_file(directory, options):
    filename = options.get('-n')
    if filename:
        file_path = Path(directory) / (filename + '.dsu')
        file_path.touch()  #creates file
        print(file_path)
    else:
        print("ERROR")

def delete_file(file_path):
    #delets dsu
    file_path = Path(file_path)
    if file_path.suffix == '.dsu' and file_path.exists():
        file_path.unlink()
        print(file_path, "DELETED")
    else:
        print("ERROR")

def read_file(file_path):
    #read dsu file
    file_path = Path(file_path)
    if file_path.suffix == '.dsu' and file_path.exists():
        content = file_path.read_text()
        if content:
            print(content.strip())
        else:
            print("EMPTY")
    else:
        print("ERROR")

def parse_command(command):
    parse = shlex.split(command)
    if len(parse) < 2:
        print("ERROR")
        return

    choice = parse[0]
    
    # joins so path works 
    path = ' '.join(parse[1:])
    
    # remove double quotes to accept both paths
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]

    options = {}
    if ' -n ' in path:
        path, option = path.split(' -n ')
        options['-n'] = option

    if choice == 'C':
        create_file(path, options)
    elif choice == 'D':
        delete_file(path)
    elif choice == 'R':
        read_file(path)
    else:
        print("ERROR")

def main():
    while True:
        command = input().strip()
        if command.upper() == 'Q':
            break
        parse_command(command)

if __name__ == "__main__":
    main()
