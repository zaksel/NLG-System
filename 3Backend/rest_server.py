import sys

from flask import Flask, render_template, request, redirect, Response, jsonify
import random, json

app = Flask(__name__)

@app.route('/')
def output():
    result = "NLG-System Backend is running"
    return result


@app.route('/input', methods=['POST'])
def input():
    data = request.get_json(force=True)
    print("Got Message from Word Add-In", data)
    input_word = data['word']

    #call generation of text
    output = "Verarbeitet " + input_word

    res = {"text": output}
    return jsonify(res)

#add response headers into our response
@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
