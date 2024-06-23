from tkinter import *
from tkinter import messagebox
import secrets
import string
import pyperclip
import json

PASSWORD_LENGTH = [12, 13, 14, 15]

# Create a window object
window = Tk()
window.title("Password Manager")
# window.minsize(width=500, height=500)
window.config(padx=50, pady=50)

# Create an image
myimg = PhotoImage(file='logo.png')
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=myimg)
canvas.grid(row=0, column=1)

website = Label(text="Website:")
website.grid(row=1, column=0)
email = Label(text="Email/Username:")
email.grid(row=2, column=0)
password = Label(text="Password:")
password.grid(row=3, column=0)

website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()  # Locate the initial cursor
email_entry = Entry(width=38)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "example@gmail.com")
password_entry = Entry(width=21, show="*")
password_entry.grid(row=3, column=1)


def generate():
    characters = string.ascii_letters + string.digits + string.punctuation
    password_list = [secrets.choice(characters) for _ in range(secrets.choice(PASSWORD_LENGTH))]
    password = ''.join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def find_password():
    website_info = website_entry.get()
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error",
                               message="No data file found.")
    else:
        if website_info in data:
            messagebox.showinfo(title=website_info,
                                message=f"Email: {data[website_info]['email']}\nPassword: {data[website_info]['password']}")
        else:
            messagebox.showwarning(title=website_info,
                                   message="No details for the website found.")


def save():
    email_info = email_entry.get()
    password_info = password_entry.get()
    website_info = website_entry.get()
    new_data = {
        website_info: {
            "email": email_info,
            "password": password_info,
        }
    }

    if website_info == "" or email_info == "" or password_info == "":
        messagebox.showwarning(title="oops", message="Please don't leave any fields empty.")
    else:
        try:
            with open("data.json", mode="r") as file:
                # Read the old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", mode="w") as file:
                # Put the new data in the file
                json.dump(new_data, file, indent=4)

                password_entry.delete(0, 'end')
                website_entry.delete(0, 'end')
        else:
            data.update(new_data)

            with open("data.json", mode="w") as file:
                # Put the new data in the file
                json.dump(data, file, indent=4)
        finally:
            password_entry.delete(0, 'end')
            website_entry.delete(0, 'end')


add_password = Button(text="Add", width=36, command=save)
add_password.grid(row=4, column=1, columnspan=2)
create_password = Button(text="Generate Password", command=generate)
create_password.grid(row=3, column=2)
search_password = Button(text="Search", command=find_password, width=13)
search_password.grid(row=1, column=2)

# Set a loop in case the window closes
window.mainloop()
