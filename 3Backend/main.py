from flask import Flask, request, redirect, Response, jsonify
from interactive_conditional_samples import Model

app = Flask(__name__)

@app.route('/')
def output():
    result = "NLG-System Backend is running"
    return result


@app.route('/input', methods=['POST'])
def input():
    data = request.get_json(force=True)
    print("Got Message from Word Add-In", data)

    #call generation of text
    output = model.generate(data['text'])

    res = {"text": output}
    return jsonify(res)


@app.route('/settings', methods=['POST'])
def settings():
    data = request.get_json(force=True)
    print("Got Settings from Word Add-In", data)


#add response headers into our response
@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    model = Model()
    app.run(host='127.0.0.1', port=5000)
