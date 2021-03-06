from flask import Flask, request
import requests
import simi
import json
import configparser


app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to hack4Missions-Bot!"


@app.route("/hack")
def hack():
    return "Created for Hack4Missions Kampala"


@app.route('/api', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        # print("===========================================================================================================")
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/api', methods=['POST'])
def handle_incoming_messages():

    # data = json.dumps(request.json)
    data = request.json

    simi.xappend("mydatalog.pop", json.dumps(data))

    sender = data['entry'][0]['messaging'][0]['sender']['id']
    # {"entry": [{"id": "324222655033543", "time": 1540065931059, "messaging": [{"sender": {"id": "2004367952978507"}, "recipient": {"id": "324222655033543"}, "timestamp": 1540065930518, "message": {"mid": "iNTahh6Qr_DXgQPNxHIoK8zvSwJhOYDaOBXlXY92tOe27q2jAyRNT9Be_OIKU5Bv0ek8cx-qY-YEFr3h8NKdQw", "seq": 54745, "text": "hi"}}]}]}

    # test_users.append(sender)

    reply_msg = "H4CBot"
    # return reply_msg

    post_to_graph(sender, reply_msg)

    # simi.xdump(list(set(test_users)), "/home/bots/test_users.bot")

    return "OK", 200


def post_to_graph(user_id, reply_msg):
    reply_data = {
        "recipient": {"id": user_id},
        "message": {"text": reply_msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=reply_data)
    print(resp.content)


if __name__ == '__main__':
    # this test users obj was used to add test users' ids to the bots database; to be used for the scheduled task
    # test_users = simi.xload( "/home/bots/test_users.bot" )

    # credentials have been moved to a config file to remove them from public github visibility
    config = configparser.ConfigParser()
    config.read("/home/bots/config.ini")
    ACCESS_TOKEN = config.get('Creds', 'ACCESS_TOKEN')
    VERIFY_TOKEN = config.get('Creds', 'VERIFY_TOKEN')

    # run the flask app //start the server
    app.run()


