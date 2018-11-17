import sendgrid
import python_http_client
import requests
import sys
from sendgrid.helpers.mail import *
from threading import Timer
from time import time
from flask import Flask, render_template, request, redirect, url_for, flash
from email import utils


app = Flask(__name__)

SG_API_KEY = "YOUR API KEY"
MG_API_KEY = "YOUR API KEY"
MG_DOMAIN = "YOUR MAILGUN DOMAIN"


def use_sendgrid(sender, recipient, _subject, _content, send_after):
    # if content is left blank set it to a white space.
    if not _content:
        _content = " "

    sg = sendgrid.SendGridAPIClient(apikey=SG_API_KEY)
    data = {
        "personalizations": [{
            "to": [{
                "email": recipient
            }],
            "subject": _subject,
            "send_at": int(time())+send_after,
        }],
        "from": {
            "email": sender
        },
        "content": [{
            "type": "text/plain",
            "value": _content
        }]
    }
    response = sg.client.mail.send.post(request_body=data)
    return response.status_code


def use_mailgun(sender, recipient, _subject, _content, send_at):
    if not _content:
        _content = " "

    return requests.post("https://api.mailgun.net/v3/%s/messages" % MG_DOMAIN,
                         auth=("api", MG_API_KEY),
                         data={"from": "<%s>" % sender,
                               "to": recipient,
                               "subject": _subject,
                               "text": _content,
                               "o:deliverytime": send_at})


@app.route('/', methods=['GET', 'POST'])
def send_email():
    send_after = 0
    if request.method == 'POST':
        # if the request method is POST get the form attributes
        # and build an email service request
        try:
            # try using sendgrid service
            if (request.form['sender'] and
                    request.form['recipient'] and
                    request.form['subject']):
                if request.form['hrs']:
                    send_after += int(request.form['hrs'])*3600
                if request.form['mnts']:
                    send_after += int(request.form['mnts'])*60
                use_sendgrid(request.form['sender'], request.form['recipient'],
                             request.form['subject'],
                             request.form['content'], send_after)
                flash("Email scheduled successfully.")
            else:
                flash("Please enter sender's and recipient's emails and email subject.")
        except:
            try:
                # try using mailgun serivce if it didn't work with sendgrid.
                try:
                    # try converting unix timestamp to rfc 2822 format.
                    send_at = utils.formatdate(send_after+int(time()))
                except:
                    flash("Enter a reasonable input time for scheduling the email.")
                use_mailgun(request.form['sender'], request.form['recipient'],
                            request.form['subject'],
                            request.form['content'], send_at)
                flash("Email scheduled successfully.")
            except:
                # both services failed to deliver.
                flash("Something went wrong, try again later.")
        return redirect(url_for('send_email'))
    else:
        # The request method is GET, so load index.html
        return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=80)
