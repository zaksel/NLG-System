import json

input_enc = "./data/embedding/encoder.txt"
output_enc = "./data/embedding/encoder.json"
input_voc = "./data/embedding/vocab.txt"
output_voc = "./data/embedding/vocab.bpe"

enc_len = 50257

def format_vocab(input_file, encoder, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        vocab_lines = f.readlines()
    with open(encoder, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(output_file, "w+", encoding="utf-8", newline='') as f:
        f.write("#version: 0.2\n")
        for line in vocab_lines:
            line = line.replace("</w>","")
            line = line.replace("\n","")
            frags = line.split(" ")

            pre = frags[0]
            post = frags[1]
            full = pre + post

            #I hate myself
            if pre in data:
                if pre in data:
                    if full in data:
                        f.write(line + "\n")
                    elif "\u0120" + full in data:
                        f.write("\u0120" + line + "\n")
                elif "\u0120" + pre in data:
                    if full in data:
                        f.write("\u0120" + line + "\n")
                    elif "\u0120" + full in data:
                        f.write("\u0120" + line + "\n")
            elif "\u0120" + pre in data:
                if pre in data:
                    if full in data:
                        f.write("\u0120" + line + "\n")
                    elif "\u0120" + full in data:
                        f.write("\u0120" + line + "\n")
                elif "\u0120" + pre in data:
                    if full in data:
                        f.write("\u0120" + line + "\n")
                    elif "\u0120" + full in data:
                        f.write("\u0120" + line + "\n")
            else:
                print("Missing Fragment in encoder.json. Skipped:    " + line)


            #nicer but what if fragments are not anymore in encoder.json?
            # if frags[0] in data and frags[1] in data and frags[0]+frags[1] in data:
            #     f.write(line+"\n")
            # else:
            #     f.write("\u0120" + line + "\n")


#numerate and save dict to json
def format_encoder(input_file,output_file):
    dict={}
    tokens=[]
    count=0
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.split("\n")

    # add all unicode chars from latin and extensions (592) on the top
    for i in list(range(ord("!"), ord("~")+1))+list(range(ord("¡"), ord("¬")+1))+list(range(ord("®"), ord("ÿ")+1))+list(range(ord("Ā"), ord("Ń")+1)):
        dict[chr(i)] = count
        count += 1

    for i in range(count, enc_len-1):
        token = lines[i].split(" ")[0]
        if "\u0120" in token:
            token = token.split("\u0120")
            token = "\u0120" + token[0]
        tokens.append(token)
    tokens.sort()
    for token in tokens:
        if token not in dict:
            dict[token] = count
            count += 1

    dict["<|endoftext|>"] = enc_len-1

    json_dict = json.dumps(dict)
    with open(output_file, "w+") as f:
        f.write(json_dict)

if __name__ == '__main__':
    format_encoder(input_enc, output_enc)
    format_vocab(input_voc, output_enc, output_voc)
