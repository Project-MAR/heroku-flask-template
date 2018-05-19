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

@app.route('/secure_check', methods=['GET'])
@auth.login_required
def check():

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
    return json.dumps(payload)

@app.route('/callback', methods=['POST'])
def callback():

    return 'HELLO' + request.data

if __name__ == "__main__":
    app.run()
