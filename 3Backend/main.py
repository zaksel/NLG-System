from flask import Flask, request, redirect, Response, jsonify
from generate_samples import Model

app = Flask(__name__)

@app.route('/')
def output():
    result = "NLG-System Backend is running"
    return result


@app.route('/input', methods=['POST'])
def input():
    global model
    data = request.get_json(force=True)
    print("Got Message from Word Add-In", data)

    #call generation of text
    output = model.generate(data['text'])

    res = {"text": output}
    return jsonify(res)


@app.route('/settings', methods=['POST'])
def settings():
    global model
    data = request.get_json(force=True)
    print("Got Settings from Word Add-In", data)

    #start new model with given params
    model.stop()
    del model
    model = Model(model_name=data['model'],
                  seed=int(data['seed']) if int(data['seed']) else None,
                  length=int(data['len']),
                  temperature=float(data['temp']),
                  top_p=float(data['top_p']),
                  lang_target=data['language'])

    res = jsonify(success=True)
    return res


#add response headers into our response
@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == '__main__':
    model = Model()
    app.run(host='127.0.0.1', port=5000)
