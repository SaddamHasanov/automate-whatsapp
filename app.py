import flask
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def reply2():
    text = request.form.get('Body')
    response = MessagingResponse()

    text1 = str(text).lower()

    if 'salam' in text1:
        response.message('Salam necəsən?')
        return flask.Response(str(response), mimetype="application/xml")
    else:
        response.message('nə deyirsən aye')
        return flask.Response(str(response), mimetype="application/xml")


if __name__ != "__main__":
    pass
else:
    app.run()
