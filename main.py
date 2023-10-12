from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# CONSTANTS
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


# SEARCH OPERATION
def search_for_it():
    search = website_input.get()
    empty_data = {
        search: {
            "email": "",
            "password": ""
        }
    }

    try:
        with open("saved_data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open("saved_data.json", "w") as file:
            json.dump(empty_data, file)
        search_for_it()
    else:
        if search in data:
            email = data[search]["email"]
            password = data[search]["password"]
            if len(email) == 0 or len(password) == 0:
                messagebox.showwarning(title="No Info", message=f"{search} website doesn't contain any information.")
            else:
                messagebox.showinfo(title=search, message=f"Email/Username: {email} \nPassword: {password}")
            website_input.delete(0, END)
        else:
            messagebox.showwarning(title="Info Error", message=f"{search} website doesn't exist.")


# PASSWORD GENERATOR

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
           'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
           'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
           'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_list = []
    [password_list.append(random.choice(letters)) for k in range(random.randint(8, 10))]
    [password_list.append(random.choice(symbols)) for j in range(random.randint(2, 4))]
    [password_list.append(random.choice(symbols)) for i in range(random.randint(2, 4))]

    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    password_input.delete(0, END)
    password_input.insert(0, password)
    messagebox.showinfo(title="Saved It", message="Your Password is saved in your clipboard.")


# SAVE PASSWORD
def save_password():
    website = website_input.get()
    email = email_username_input.get()
    password = password_input.get()
    data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered: \nEmail: {email} \nPassword :{password} \nDo you want to save it?")
        if is_ok:
            try:
                with open("saved_data.json", 'r') as file:
                    load_data = json.load(file)
                    load_data.update(data)
            except (json.decoder.JSONDecodeError, FileNotFoundError):
                with open("saved_data.json", 'w') as file:
                    json.dump(data, file, indent=4)
            else:
                with open("saved_data.json", 'w') as file:
                    json.dump(load_data, file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# UI SETUP
window = Tk()
window.config(padx=30, pady=30, bg=YELLOW)
window.title("PASSWORD MANAGER")

canvas = Canvas(width=200, height=200, bg=YELLOW, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=0, columnspan=4)

website_label = Label(text="Website: ", fg=RED, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
website_label.grid(row=1, column=0)

website_input = Entry(width=35, font=FONT_NAME)
website_input.grid(row=1, column=1, columnspan=2)
website_input.focus()

email_username_label = Label(text="Email/Username: ", fg=PINK, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
email_username_label.grid(row=2, column=0)

email_username_input = Entry(width=35, font=FONT_NAME)
email_username_input.grid(row=2, column=1, columnspan=2)
email_username_input.insert(0, "dummy@gmail.com")

password_label = Label(text="Password: ", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
password_label.grid(row=3, column=0)

password_input = Entry(width=35, font=FONT_NAME)
password_input.grid(row=3, column=1, columnspan=2)

password_button = Button(text="Generate Password", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 9, "bold"),
                         command=generate_password, width=17)
password_button.grid(row=3, column=3)

add_button = Button(text="ADD", fg=RED, bg=YELLOW, font=(FONT_NAME, 11, "bold"), width=37, command=save_password)
add_button.grid(row=4, column=1, columnspan=3)

search_button = Button(text="SEARCH", fg=RED, bg=YELLOW, font=(FONT_NAME, 9, "bold"), command=search_for_it, width=10)
search_button.grid(row=1, column=3)
window.mainloop()
