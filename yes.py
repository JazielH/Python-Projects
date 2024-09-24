# Jaziel Herrera
# jazielh@uci.edu
#a4.py

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from Profile import Profile, DirectMessage
import ds_messenger
import time

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        selected_item = self.posts_tree.selection()
        if selected_item:
            index = int(selected_item[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)

    def insert_contact(self, contact: str):
        if contact not in self._contacts:
            self._contacts.append(contact)
            id = len(self._contacts) - 1
            self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            contact = contact[:24] + "..."
        self.posts_tree.insert('', 'end', id, text=contact)

    def insert_user_message(self, message: str):
        self.entry_editor.insert(tk.END, f"You: {message}\n", 'entry-right')

    def insert_contact_message(self, sender: str, message: str):
        self.entry_editor.insert(tk.END, f"{sender}: {message}\n", 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        self.message_editor.delete('1.0', tk.END)
        self.message_editor.insert('1.0', text)

    def clear(self):
        self._contacts = []
        self.posts_tree.delete(*self.posts_tree.get_children())
        self.entry_editor.delete('1.0', tk.END)
        self.message_editor.delete('1.0', tk.END)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="green")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="green", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="green")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root, bg='green')
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def set_status(self, text: str):
        self.footer_label.config(text=text)

    def _draw(self):
        send_button = tk.Button(master=self, text="Send", width=20, command=self.send_click, bg='light green')
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.", bg='green')
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server if server else ""
        self.user = user if user else ""
        self.pwd = pwd if pwd else ""
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, bg='light green')
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.profile = Profile()
        self.direct_messenger = None
        self._draw()

    def _initialize_messenger(self):
        if self.username and self.password and self.server:
            self.direct_messenger = ds_messenger.DirectMessenger(self.server, self.username, self.password)
            self.profile.direct_messenger = self.direct_messenger
            print(f"Messenger initialized with user: {self.username}, server: {self.server}")

    def send_message(self):
        message = self.body.get_text_entry()
        if self.recipient and message:
            print(f"Sending message to {self.recipient}: {message}")
            self.direct_messenger.send(message, self.recipient)
            self.profile.add_message(DirectMessage(self.username, self.recipient, message, time.time()))
            self.body.insert_user_message(message)
            self.body.set_text_entry("")
            self.profile.save_profile("profile.dsu")
            print("Message sent and profile saved.")

    def add_contact(self):
        new_contact = simpledialog.askstring("Add Contact", "Enter the username of the new contact:")
        if new_contact:
            print(f"Adding new contact: {new_contact}")
            self.profile.add_friend(new_contact)
            self.body.insert_contact(new_contact)
            self.profile.save_profile("profile.dsu")
            print("Contact added and profile saved.")

    def recipient_selected(self, recipient):
        self.recipient = recipient
        print(f"Recipient selected: {recipient}")
        self.footer.set_status(recipient)
        self.body.entry_editor.delete('1.0', tk.END)
        for msg in self.profile.messages:
            if msg.recipient == recipient:
                self.body.insert_user_message(msg.message)
            elif msg.sender == recipient:
                self.body.insert_contact_message(recipient, msg.message)

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account", self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        if self.username and self.password and self.server:
            self.direct_messenger = ds_messenger.DirectMessenger(self.server, self.username, self.password)
            self.profile.direct_messenger = self.direct_messenger
            self.profile.username = self.username
            self.profile.password = self.password
            self.profile.dsuserver = self.server
            self.profile.save_profile("profile.dsu")
            print(f"Server configured with user: {self.username}, server: {self.server}")

    def open_profile(self):
        file_path = filedialog.askopenfilename(filetypes=[("DSU Files", "*.dsu")])
        if file_path:
            try:
                self.profile.load_profile(file_path)
                self.username = self.profile.username
                self.password = self.profile.password
                self.server = self.profile.dsuserver
                self._initialize_messenger()
                self._load_ui_from_profile()
                print(f"Profile loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load profile: {e}")

    def save_profile(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".dsu", filetypes=[("DSU Files", "*.dsu")])
        if file_path:
            try:
                self.profile.save_profile(file_path)
                print(f"Profile saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save profile: {e}")

    def _load_ui_from_profile(self):
        self.body.clear()
        for friend in self.profile.friends:
            self.body.insert_contact(friend)
        for msg in self.profile.messages:
            if msg.recipient == self.username:
                self.body.insert_contact_message(msg.sender, msg.message)
            elif msg.sender == self.username:
                self.body.insert_user_message(msg.message)

    def check_new(self):
        if self.direct_messenger:
            print("Checking for new messages...")
            try:
                new_messages = self.direct_messenger.retrieve_new()
                for msg in new_messages:
                    if isinstance(msg, ds_messenger.DirectMessage):
                        new_message = DirectMessage(
                            sender=msg.sender,
                            recipient=self.username,
                            message=str(msg.message),
                            timestamp=msg.timestamp
                        )
                        self.profile.add_message(new_message)
                        print(f"New message from {new_message.sender}: {new_message.message}")
                        if new_message.sender == self.username:
                            self.body.insert_user_message(new_message.message)
                        else:
                            self.body.insert_contact_message(new_message.sender, new_message.message)
                            self.body.insert_contact(new_message.sender)
                    else:
                        print("Unexpected message format: ", msg)
                self.profile.save_profile("profile.dsu")
            except Exception:
                self.footer.set_status("No Wifi")
        self.root.after(5000, self.check_new)

    def _draw(self):
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Save', command=self.save_profile)
        menu_file.add_command(label='Close', command=self.root.quit)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact', command=self.add_contact)
        settings_file.add_command(label='Configure DS Server', command=self.configure_server)

        self.body = Body(self.root, recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.after(2000, app.check_new)
    main.mainloop()
