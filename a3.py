# Jaziel Herrera
# jazielh@uci.edu

# a3.py

from ui import (
    create_profile, load_profile, edit_profile, print_profile_data, 
    delete_file, read_file, parse_command, send_message_online, post_journal_entry, update_bio
)

def main():
    profile = None
    while True:
        print("\nWelcome! Choose an option:")
        print("C - Create Profile Online")
        print("O - Load Profile")
        print("E - Edit Profile")
        print("P - Print Profile Data")
        print("R - Read Profile File")
        print("D - Delete Profile File")
        print("S - Send Message to Server")
        print("J - Post Journal Entry Online")
        print("B - Update Bio Online")
        print("Q - Quit")
        print("Admin - Admin Mode")
        
        mode = input().strip().lower()
        if mode == 'admin':
            while True:
                command = input().strip()
                if command.lower() == 'q':
                    break
                parse_command(command)
        else:
            command = mode.upper()
            if command == 'Q':
                break
            elif command == 'C':
                directory = input("Enter directory: ").strip()
                options = {'-n': input("Enter filename (without extension): ").strip()}
                profile = create_profile(directory, options)
            elif command == 'O':
                file_path = input("Enter file name:(with the .dsu):").strip()
                profile = load_profile(file_path)
            elif command == 'E':
                file_path = input("Enter file name:(with the .dsu):").strip()
                options = {}
                while True:
                    option = input("Enter option (-usr, -pwd, -bio, -addpost, -delpost) or 'done' to finish: ").strip()
                    if option == 'done':
                        break
                    value = input(f"Enter value for {option}: ").strip()
                    options[option] = value
                profile = load_profile(file_path)
                if profile:
                    edit_profile(profile, options)
            elif command == 'P':
                file_path = input("Enter file name: (with the .dsu) ").strip()
                profile = load_profile(file_path)
                if profile:
                    options = input("Enter options to print (-usr, -pwd, -bio, -posts, -all): ").strip().split()
                    print_profile_data(profile, options)
            elif command == 'R':
                file_path = input("Enter file name: (with the .dsu)").strip()
                read_file(file_path)
            elif command == 'D':
                file_path = input("Enter file name: (with the .dsu)").strip()
                delete_file(file_path)
            elif command == 'S':
                send_message_online()
            elif command == 'J' and profile:
                post_journal_entry(profile)
            elif command == 'B' and profile:
                update_bio(profile)
            else:
                print("Invalid command or no profile loaded.")

if __name__ == "__main__":
    main()
