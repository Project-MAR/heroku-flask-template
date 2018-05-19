from flask import Flask, request, abort, make_response
from flask_httpauth import HTTPBasicAuth

import requests, json

app = Flask(__name__)
auth = HTTPBasicAuth()

# Do not use in real world !!!
username = 'root'
password = 'root'

@auth.get_password
def get_pw(username):
    if username == username:
        return password
    return None

@auth.error_handler
def unauthorized():
    return make_response(json.dumps({'error': 'Unauthorized access'}), 401)

@app.route('/')
def index():
	return 'OK'

@app.route('/check', methods=['GET'])
def check():

    name = 'client'

    payload = {
        'to'        : name,
        'length'    : 3,
        'messages'  : [
            {
                'Id'       : 'plane text',
                'Location' : 'Bangkok',
                'Version'  : '1.0.0'
            }
        ]
    }
    return json.dumps(payload)

@app.route('/check_withlogin', methods=['GET'])
@auth.login_required
def check_withlogin():

    name = 'secure_client'

    payload = {
        'to'        : name,
        'length'    : 4,
        'messages'  : [
            {
                'Id'       : 'plane text',
                'Location' : 'Bangkok',
                'Version'  : '1.0.0',
                'Secure'   : 'True'
            }
        ]
    }

@app.route('/callback', methods=['POST'])
def callback():
    payload  = request.get_json()
    payload = json.dumps(payload)
    payload = json.loads(payload)

    return json.dumps(payload['id'] + " " + payload['name'])

if __name__ == "__main__":
    app.run()
