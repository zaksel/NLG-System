import json

input_enc = "./data/embedding/encoder.txt"
output_enc = "./data/embedding/encoder.json"
input_voc = "./data/embedding/vocab.txt"
output_voc = "./data/embedding/vocab.bpe"

def format_vocab(input_file, encoder, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        vocab_lines = f.readlines()
    with open(encoder, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(output_file, "w+", encoding="utf-8") as f:
        for line in vocab_lines:
            line = line.replace("</w>","")
            line = line.replace("\n","")
            frags = line.split(" ")

            if frags[0] in data and frags[1] in data and frags[0]+frags[1] in data:
                f.write(line+"\n")
            else:
                f.write("\u0120" + line + "\n")


#numerate and save dict to json
def format_encoder(input_file,output_file):
    dict={}
    tokens=[]
    count=0
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.split("\n")
    for line in lines:
        token = line.split(" ")[0]
        token = token.replace("\\u0120","\u0120") #Be careful hack
        if "\u0120" in token:
            token = token.split("\u0120")
            token = "\u0120"+token[0]
        tokens.append(token)
    tokens.sort()
    for token in tokens:
        dict[token] = count
        count += 1
    json_dict = json.dumps(dict)

    with open(output_file, "w+") as f:
        f.write(json_dict)

if __name__ == '__main__':
    format_encoder(input_enc, output_enc)
    format_vocab(input_voc, output_enc, output_voc)
