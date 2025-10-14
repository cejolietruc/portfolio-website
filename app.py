from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib, os

my_email = os.environ['MY_EMAIL']
my_pass = os.environ['MY_PASS']
to_email = os.environ['TO_EMAIL']

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_KEY']


@app.route("/", methods=['POST','GET'])
def home():
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if not message:
            flash("No message has been sent!")
            return redirect(url_for('home'))

        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()  # Transport Layer Security
                connection.login(user=my_email, password=my_pass)
                connection.sendmail(from_addr=my_email,
                                    to_addrs=to_email,
                                    msg=f"Subject:Message from Portfolio Website!\n\n"
                                        f"Name : {name}\n"
                                        f"Email: {email}\n\n"
                                        f"{message}")
        except ConnectionError as msg:
            flash(f"{msg}. Try again later!")
        else:
            flash("Your message has been sent!")
            return redirect(url_for('home'))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

