import flask
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pymongo
from datetime import datetime

cluster = pymongo.MongoClient("mongodb+srv://Saddam:Matrixgame213@wpbotdatabase.giznbjw.mongodb.net/botDB?retryWrites=true&w=majority")

db = cluster.botDB
users = db.users
orders = db.orders

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def reply():

    # fetching
    text = request.form.get('Body')
    number = request.form.get('From')

    # changing
    text = str(text).lower()
    # number = number.replace("whatsapp:", "")[:-2]

    # reply to messages
    response = MessagingResponse()
    user = users.find_one({"number": number})
    if (bool(user) is False) or ('salam' in text):
        users.insert_one({"number": number, "status": "main", "messages": []})
        users.update_one({"number": number}, {"$set": {"status": "main"}})
        response.message("Salam, dəyərli müştərimiz, *Handex komandası* olaraq\nbütün "
                         "suallarınıza cavab verməyə və sizə dəstək olmağa hazırıq: \n\n"
                         "1️⃣ Kurslar haqqında məlumat\n2️⃣ Bizimlə əlaqə\n3️⃣ FAQ\n4️⃣ "
                         "Təlimlərimizin sillabusları\n")
        return flask.Response(str(response), mimetype="application/xml")
    elif user["status"] == "main":
        try:
            option = int(text)
        except ValueError:
            response.message("Məlumat ala bilmək üçün zəhmət olmasa 1, 2, 3, 4\nrəqəmlərindən birini daxil edin")
            return flask.Response(str(response), mimetype="application/xml")

        if option == 1:
            response.message("0️⃣ Geri qayıtmaq\n"
                             "1️⃣ Excel\n"
                             "2️⃣ MOSE\n"
                             "3️⃣ Power BI (PL-300)\n"
                             "4️⃣ SQL (1Z0-071)\n"
                             "5️⃣ Data Analitika")
            users.update_one({"number": number}, {"$set": {"status": "kurslar"}})
            return flask.Response(str(response), mimetype="application/xml")
        elif option == 2:
            response.message("Əlaqə nömrəsi: 050-369-60-88\n"
                             "Email: seddamhasanov213@yandex.com")
            return flask.Response(str(response), mimetype="application/xml")
        elif option == 3:
            response.message("3 seçildi")
            return flask.Response(str(response), mimetype="application/xml")
        elif option == 4:
            response.message("4 seçildi")
            return flask.Response(str(response), mimetype="application/xml")
        elif option == 5:
            return
        else:
            response.message("Məlumat ala bilmək üçün zəhmət olmasa 1, 2, 3, 4\nrəqəmlərindən birini daxil edin")
            return flask.Response(str(response), mimetype="application/xml")
    elif user["status"] == "kurslar":
        try:
            option = int(text)
        except ValueError:
            response.message("Məlumat ala bilmək üçün zəhmət olmasa 0, 1, 2, 3, 4, 5\nrəqəmlərindən birini daxil edin")
            return flask.Response(str(response), mimetype="application/xml")
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            response.message("1️⃣ Kurslar haqqında məlumat\n"
                             "2️⃣ Bizimlə əlaqə\n"
                             "3️⃣ FAQ\n"
                             "4️⃣ Təlimlərimizin sillabusları\n")
            return flask.Response(str(response), mimetype="application/xml")
        elif 1 <= option <= 5:
            kurslar = ["Excel", "MOSE", "PowerBI (PL-300)", "SQL (1Z0-071)", "Data Analitika"]
            qiymetler = [175, 169, 449, 400, 849]
            mellimler = ['Orxan Niftullayev', 'Rəşad Qurbanov', 'Şahmurad Məmmədov',
                         'Ceyhun Qazıxanov', 'Rəşad Qurbanov\n'
                         'Ceyhun Qazıxanov\n'
                         'Kamal Mustafayev\n'
                         'Tuncay Məcnunlu\n'
                         'Tural Əhmədov']
            vaxt = ['II gün - saat 20:00-22:00\nVI gün - saat 11:00-13:00',
                    'II gün - saat 20:00-22:00\nVI gün - saat 11:00-13:00',
                    'I gün - saat 19:00-21:00 (Power BI tədrisi + Praktika)\n'
                    'IV gün - saat 19:00-21:00 (Power BI tədrisi + Praktika)\n'
                    'VI gün – saat 11:00-13:00 (PL-300 hazırlıq)',
                    'II gün - saat 20:00-22:00\nVI gün - saat 11:00-13:00',
                    'I gün - saat 19:00-21:00\n'
                    'IV gün - saat 19:00-21:00\n'
                    'VI gün – saat 11:00-13:00']
            selected = kurslar[option-1]
            users.update_one({"number": number}, {"$set": {"item": selected}})
            response.message(f'0️⃣ Əsas səhifəyə qayıtmaq üçün\n'
                             f'{selected} kursumuz:\n'
                             f'Qiymət: {qiymetler[option-1]} AZN\n'
                             f'Təlimçimiz: {mellimler[option-1]}\n'
                             f'Təlim vaxtları: {vaxt[option-1]}')
            orders.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now()})
            return flask.Response(str(response), mimetype="application/xml")
        else:
            response.message("Məlumat ala bilmək üçün zəhmət olmasa 0, 1, 2, 3, 4, 5\nrəqəmlərindən birini daxil edin")
            return flask.Response(str(response), mimetype="application/xml")

    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})


if __name__ != "__main__":
    pass
else:
    app.run()
