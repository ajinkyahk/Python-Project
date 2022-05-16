##################### Extra Hard Starting Project ######################
import smtplib
import random
import datetime as dt
import pandas as pd
import re

# 1. Update the birthdays.csv
def update_bd():
    name = input("Enater Name: ")
    email = input("Enter Email: ")
    year = input("Year: ")
    month = input("Month: ")
    day = input("Day: ")
    with open("birthdays.csv","a") as f:
            f.write(f"{name},{email},{year},{month},{day}\n")

# 2. Check if today matches a birthday in the birthdays.csv
data = pd.read_csv("birthdays.csv")
now = dt.datetime.now()
y = now.year
m = now.month
d = now.day
print(now)
is_day = False
name = ""
for index,row in data.iterrows():
    if m==row.month and d==row.day:
        is_day = True
        name=row["name"]

#birth_date = dt.datetime(year=year, month=month, day=day)
#if now.date() == birth_date:
#    print("yes")
#print(birth_date)
# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

if is_day == True:
    with open(f"letter_templates/letter_{random.randint(1,3)}.txt", "r") as f:
        line = f.readline()
        letter = f.readlines()
        print(line)
        print(name)



    pattern = r"(\[\w*\])"
    new_line = re.sub(pattern, name, line)
    letter.insert(0,new_line)
    print(letter)
    birthday_wish = "".join(letter)
    print(birthday_wish)



# 4. Send the letter generated in step 3 to that person's email address.

my_email = "YOUR EMAIL"
password = "YOUR EMAIL PASSWORD"

with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)

    connection.sendmail(from_addr=my_email,
                        to_addrs="EMAIL YOU WANT TO SEND TO",
                        msg=f"Subject: Birthday Wishes !!!  \n\n"
                            f"{birthday_wish}")



