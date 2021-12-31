# coding: utf-8

from flask import Flask, request, jsonify

from auth import AuthHandler
from agreements import AgreementsHandler

app = Flask(__name__)
AgreementsHandler = AgreementsHandler()


@app.route('/')
def index():
    return 'It\'s PCL REST API Mock Server.'


@app.route('/authentication/client-access-tokens', methods=('GET', 'POST'))
def get_client_access_token():
    token = 'No token'
    if request.method == 'GET':
        return token
    elif request.method == 'POST':
        auth_handler = AuthHandler()
        token_info = auth_handler.get_client_access_token(request.headers, request.values)
        res = jsonify(token_info)
        return res


@app.route('/agreements/', methods=('GET',))
def get_agreements():
    res = AgreementsHandler.get_agreements(request.headers, request.values)
    return jsonify(res)


if __name__ == '__main__':
    app.run()
