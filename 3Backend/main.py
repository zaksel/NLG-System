from flask import Flask, request, redirect, Response, jsonify
import tensorflow as tf
import generate_samples_s1a as s1a
import generate_samples_s1b as s1b
import generate_samples_s2 as s2
import generate_samples_s3 as s3
import generate_samples_s4 as s4

app = Flask(__name__)

@app.route('/')
def output():
    result = "NLG-System Backend is running"
    return result


@app.route('/input', methods=['POST'])
def input():
    data = request.get_json(force=True)
    print("Got Message from Word Add-In", data)

    #start model
    model = eval(data['settings']['strategy']).Model(
                                                model_name=data['settings']['model'],
                                                seed=data['settings']['seed'],
                                                length=data['settings']['len'],
                                                top_k=data['settings']['top_k'],
                                                lang_target=data['settings']['language'],
                                                beam_width=data['settings']['beam_width'],
                                                beam_depth=data['settings']['beam_depth'],
                                                scope=data['settings']['scope'],
                                                timeout=data['settings']['timeout'])

    #call generation of text
    output = model.generate(data['text'])
    #del model
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
