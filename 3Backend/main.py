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

    """
    start session with the following Keyword Arguments(kwargs)
    strategy=[s1a,s1b,s2,s3,s4] :   Specify Strategy to connect supporting words one out of
                                    [Beam-Search, Beam-Search(Scope), Search until fit, Cut-off and insert, BERT-GPT2 Hybrid]
    model_name=[117M,ISW_Model]:    String, which model to use
    seed=None :                     Integer seed for random number generators, fix seed to reproduce results
    length=None :                   Number of tokens in generated text
    top_k=0 :                       Count of Tokens considered for each step (Probability Distribution)
    language :                      Language in which the support words are given, equal to output language
                                    set to None if no translation required
    beam_width :                    Beamwidth for strategy s1a or s1b
    beam_depth :                    Beamdepth for strategy s1a or s1b
    scope :                         Scope for s1b
    timeout :                       Set a timeout if you use strategy s1a,s1b or s2 to stop process after time
    """
    model = eval(data['settings']['strategy']).Model(**data['settings'])

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
