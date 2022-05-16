from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def genearte_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    # for char in range(nr_letters):
    #     password_list.append(random.choice(letters))
    password_list = [random.choice(letters) for _ in range(nr_letters)]

    # for char in range(nr_symbols):
    #     password_list += random.choice(symbols)

    password_list += [random.choice(symbols) for _ in range(nr_symbols)]

    # for char in range(nr_numbers):
    #     password_list += random.choice(numbers)

    password_list +=[random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    #password = ""
    # for char in password_list:
    #     password += char

    password = "".join(password_list)

    passwd = pass_input.get()
    if len(passwd)!=0:
        pass_input.delete(0,END)
        pass_input.insert(0,f"{password}")
        pyperclip.copy(password)
    else:
        pass_input.insert(0, f"{password}")
        pyperclip.copy(password)
    #print(f"Your password is: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = pass_input.get()
    new_data = {
        website:{
            "email": email,
            "password": password
        }
    }
    if len(website)==0 or len(password)==0:
        messagebox.showinfo(title="Oops", message=f"Please don't leave any fields empty")
    else:
        #messagebox.showinfo(title="Title", message="Message")
        #messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}\n "
        #                                              f"Password: {password}\n Is It Ok To Save?")

        try:
            with open("data.json", "r") as file:
                #Reading old data
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(new_data, file, indent=4)

        else:
            #update old data with new data
            data.update(new_data)

            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            website_input.delete(0,END)
            pass_input.delete(0,END)
            website_input.focus()

#----------------------------Search Password ---------------------------#

def search_password():
    website = website_input.get()
    is_ok=False
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            messagebox.showinfo(title=f"{website}", message=f"Email: {tuple(data[website].values())[0]}\n "
                                                            f"Password: {tuple(data[website].values())[1]}")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No Data File Found")
    except KeyError:
        messagebox.showinfo(title=f"{website}", message="No Data Found")


# ---------------------------- UI SETUP ------------------------------- #

windows = Tk()
windows.title("Password Manager")
windows.config(padx=20, pady=20)

canvas = Canvas(height=200, width=200)
#image
photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(column=1, row=0)

#label
website_label = Label(text="website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

#Entry
website_input = Entry(width=29)
website_input.grid(column=1, row=1, pady=10, padx=10)
website_input.focus()

email_input = Entry(width=55)
email_input.grid(column=1, row=2, columnspan=2, pady=10)
email_input.insert(0, "ajinkya@gmail.com")

pass_input = Entry(width=29)
pass_input.grid(column=1, row=3, pady=10)

#button
search_button = Button(text="Search", width=18, command=search_password)
search_button.grid(column=2, row=1, padx=10, pady=10)

pass_button = Button(text="Generate Password", width=18, command=genearte_password)
pass_button.grid(column=2, row=3, padx=10, pady=10)

add_button = Button(text="Add", width=47, command=save)
add_button.grid(column=1, row=4, columnspan=2)




windows.mainloop()
