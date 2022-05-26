from flask import Flask, render_template, request
import requests
import smtplib

email_one = "Your Email"
password = "Email Password"

URL = 'https://api.npoint.io/5507e502f97be25c3993'
blogs = requests.get(url=URL).json()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html', blogs=blogs)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        send_email(data['name'], data['email'], data['phone'], data['message'])
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email_one, password=password)
        connection.sendmail(from_addr=email_one,
                            to_addrs=email_one,
                            msg=email_message)


@app.route("/post/<int:num>")
def post(num):
    return render_template('post.html', blog=blogs[num - 1])


if __name__ == "__main__":
    app.run(debug=True)
