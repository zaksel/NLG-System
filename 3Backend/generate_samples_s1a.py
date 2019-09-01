#Strategie 1a Beam-Search
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import random
import time

class Model(object):
    def __init__(self,
                 model_name='117M',
                 seed=1,
                 beam_width=20, beam_depth=5,
                 lang_target='de'):

        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

        self.beam_width = beam_width
        self.beam_depth = beam_depth
        random.seed = seed

    #gets array of words and performs beam search to connect them
    def generate(self, input):

        def get_probs(input_ids):
            outputs = self.model(input_ids, labels=input_ids) #size=(1,len_input, len_encoder.json)
            #take only logits of the prediction -> last tensor
            logits = outputs[1][0][-1:]
            #apply softmax to logits
            probabilities = torch.softmax(logits, dim=-1)
            #get top values and their id
            best_logits, best_indices = probabilities.topk(self.beam_width)

            #output
            ids = best_indices.tolist()[0]
            return ids

        def beam_search(sent_ids, supp_id):
            beams = [sent_ids]
            i = 0
            while len(beams) < (self.beam_width ** self.beam_depth - 1) / (self.beam_width - 1) and (time.time()-start < 300):
                poss_ids = get_probs(beams[i])
                for id in poss_ids:
                    # append new possible tokens to tokens along the path
                    sent_ids = torch.cat((beams[i], torch.tensor([[id]])), dim=1)
                    if id == supp_id:
                        print("Heureka")
                        #print(i)
                        return 1, sent_ids
                    beams.append(sent_ids)
                i += 1

            print("Support not found: Do random Step")
            return 0, beams[random.randrange(i)]


        sent_ids = torch.tensor(self.tokenizer.encode(input.pop(0))).unsqueeze(0)
        support = "a " + " ".join(input)
        supp_ids = self.tokenizer.encode(support)[1:]
        while (len(supp_ids) > 0) and (time.time()-start < 300):
            res, sent_ids = beam_search(sent_ids, supp_ids[0])
            if res:
                supp_ids.pop(0)

            #convert result from ids to string
            tokens = self.tokenizer.convert_ids_to_tokens(sent_ids.tolist()[0])
        return self.tokenizer.convert_tokens_to_string(tokens)


if __name__ == '__main__':
    model = Model()
    start = time.time()
    print(model.generate(["Push the button", "right", "activate", "camera", "pictures", "family", "animals."]))    #a
    #print(model.generate(["The C625AF camera", "five flash modes", "red-eye", "lens", "protected", "UV Filter.", "auto focus", "programmed shutter", "camera case"]))   #b
    #print(model.generate(["If the viewfinder", "not sharp", "check", "eyepiece diopter adjustment", "knob", "near to the eyepiece.", "On-Off control", "button", "handgrip on the right", "thumb", "one press", "recording", "second", "stop."]))  #c
    print(time.time()-start)

