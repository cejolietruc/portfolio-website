from flask import Flask, render_template, request, redirect, url_for, flash
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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

        mail = Mail(
            from_email=my_email,
            to_emails=to_email,
            subject='Message from Portfolio Website!',
            html_content=f'<strong>Name : {name}</strong><br>'
                         f'<strong>Name : {email}</strong><br>'
                         f'<p>Name : {message}</p><br>'
        )
        try:
            sg = SendGridAPIClient(os.environ['SENDGRID_APIKEY'])
            # sg.set_sendgrid_data_residency("eu")
            # uncomment the above line if you are sending mail using a regional EU subuser
            response = sg.send(mail)
            flash(response.status_code)
            # flash(response.body)
            # flash(response.headers)
        except Exception as e:
            flash(f"Email error: {e}")
        except ConnectionError as msg:
            flash(f"{msg}. Try again later!")
        # else:
        #     flash("Your message has been sent!")
        #     return redirect(url_for('home'))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

