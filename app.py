import flask
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Saddam:Matrixgame213@wpbotdatabase."
                      "giznbjw.mongodb.net/?retryWrites=true&w=majority",
                      tls=True, tlsAllowInvalidCertificates=True)

db = cluster["botDB"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def reply2():
    text = request.form.get('Body')
    number = request.form.get('From')
    response = MessagingResponse()

    text1 = str(text).lower()

    user = users.find(number)
    if (bool(user) is False) or ('salam' in text1):
        response.message('Salam necəsən?')
        return flask.Response(str(response), mimetype="application/xml")
    else:
        response.message('nə deyirsən aye')
        return flask.Response(str(response), mimetype="application/xml")


if __name__ != "__main__":
    pass
else:
    app.run()
