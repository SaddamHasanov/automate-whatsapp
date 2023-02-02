import flask
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pymongo

cluster = pymongo.MongoClient("mongodb+srv://Saddam:Matrixgame213@wpbotdatabase.giznbjw.mongodb.net/botDB?ssl=true&ssl_cert_reqs=CERT_NONEretryWrites=true&w=majority")

db = cluster.botDB
users = db.users
orders = db.orders

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def reply2():
    text = request.form.get('Body')
    number = request.form.get('From')
    response = MessagingResponse()
    user = users.find_one({"number": number)

    text1 = str(text).lower()

    if (bool(user) is False) or ('salam' in text1):
        response.message('Salam necəsən?')
        # users.insert_one({"number": number, "status": "main", "messages": []})
        return flask.Response(str(response), mimetype="application/xml")
    else:
        response.message('nə deyirsən aye')
        return flask.Response(str(response), mimetype="application/xml")


if __name__ != "__main__":
    pass
else:
    app.run()
