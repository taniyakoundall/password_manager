from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# ALL GOOD
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    nr_letters = randint(2, 3)
    nr_symbols = randint(2, 3)
    nr_numbers = randint(2, 3)

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    print(password_list)

    # to clear password_entry
    password_entry.delete(0, END)

    gen_password = "".join(password_list)
    password_entry.insert(0, gen_password)
    pyperclip.copy(gen_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:
            {
                "email": email,
                "password": password,
            }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open("data.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode='w') as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    #   check if user's text entry matches an item in the data.json
    try:
        with open('data.json', mode='r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="ERROR", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="GOT IT!", message=f"email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="ERROR", message="No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=20)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# LABELS
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# ENTRY
website_entry = Entry(width=30)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, sticky="w")

email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
email_entry.insert(0, "abc@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="w")

# BUTTON
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="w")

gen_button = Button(text="Generate Password", command=generate_password)
gen_button.grid(row=3, column=2, sticky="w")

add_button = Button(text="Add", width=52, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="w")

window.mainloop()
