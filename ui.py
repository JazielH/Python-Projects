# Jaziel Herrera
# jazielh@uci.edu
# 78328456
# ui.py

from pathlib import Path
import shlex
from Profile import Profile, Post, DsuFileError, DsuProfileError

def create_profile(directory, options):
    filename = options.get('-n')
    if not filename:
        filename = input("Enter filename: ")
    if not filename:
        print("ERROR: Please provide a filename.")
        return

    file_path = Path(directory) / (filename + '.dsu')
    if file_path.exists():
        print("File already exists. Loading existing profile.")
        profile = load_profile(file_path)
    else:
        file_path.touch()
        profile = Profile(dsuserver='default')
        profile.username = input("Enter username: ")
        profile.password = input("Enter password: ")
        profile.bio = input("Enter bio: ")
        profile.file_path = str(file_path)
        profile.save_profile(profile.file_path)
        print("Profile created successfully.")
    return profile

def load_profile(file_path):
    try:
        profile = Profile()
        profile.load_profile(str(file_path))
        print("Successfully done.")
        profile.file_path = str(file_path)
        return profile
    except (DsuFileError, DsuProfileError) as e:
        print(f"Failed to load profile from {file_path}: {e}")
        raise DsuFileError()

def edit_profile(profile, options):
    if '-usr' in options:
        profile.username = options['-usr']
    if '-pwd' in options:
        profile.password = options['-pwd']
    if '-bio' in options:
        profile.bio = options['-bio']
    if '-addpost' in options:
        post_content = options['-addpost']
        post = Post(post_content)
        profile.add_post(post)
    if '-delpost' in options:
        post_id = int(options['-delpost'])
        profile.del_post(post_id)
    profile.save_profile(profile.file_path)

def print_profile_data(profile, options):
    for option in options:
        if option == '-usr':
            print(f"Username: {profile.username}")
        elif option == '-pwd':
            print(f"Password: {profile.password}")
        elif option == '-bio':
            print(f"Bio: {profile.bio}")
        elif option == '-posts':
            posts = profile.get_posts()
            print("Posts:")
            for i, post in enumerate(posts):
                print(f"ID: {i}, Entry: {post.entry}")
        elif option.startswith('-post'):
            index = int(option.split()[1])
            posts = profile.get_posts()
            if 0 <= index < len(posts):
                print(f"Post ID {index}: {posts[index].entry}")
            else:
                print(f"Invalid post ID: {index}")
        elif option == '-all':
            print("All Profile Data:")
            print(f"Username: {profile.username}")
            print(f"Password: {profile.password}")
            print(f"Bio: {profile.bio}")
            posts = profile.get_posts()
            print("Posts:")
            for i, post in enumerate(posts):
                print(f"ID: {i}, Entry: {post.entry}")

def delete_file(file_path):
    file_path = Path(file_path)
    if file_path.suffix == '.dsu' and file_path.exists():
        file_path.unlink()
        print(file_path, "DELETED")
    else:
        print("ERROR")

def read_file(file_path):
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
    path = ' '.join(parse[1:])
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]

    options = {}
    if ' -n ' in path:
        path, option = path.split(' -n ')
        options['-n'] = option

    if choice == 'C':
        create_profile(path, options)
    elif choice == 'D':
        delete_file(path)
    elif choice == 'R':
        read_file(path)
    elif choice == 'O':
        return load_profile(path)
    elif choice == 'E':
        parts = path.split(' ')
        path = parts[0]
        options_str = ' '.join(parts[1:])
        options = {}
        current_option = None
        for part in shlex.split(options_str):
            if part.startswith('-'):
                current_option = part
                options[current_option] = ''
            elif current_option:
                options[current_option] = part
                current_option = None
        profile = load_profile(path)
        if profile:
            edit_profile(profile, options)
    elif choice == 'P':
        parts = path.split(' ')
        path = parts[0]
        options = parts[1:]
        profile = load_profile(path)
        if profile:
            print_profile_data(profile, options)
    else:
        print("ERROR")

