from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from treelib import Node, Tree

class Model(object):
    def __init__(self,
                 model_name='117M',
                 seed=None,
                 beam_width=6, beam_depth=6,
                 lang_target='de'):

        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

        self.beam_width = beam_width
        self.beam_depth = beam_depth
        self.seed = seed

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
            probs = best_logits.tolist()[0]
            ids = best_indices.tolist()[0]
            words = self.tokenizer.convert_ids_to_tokens(ids)
            return ids, words, probs

        def beam_search(sent, sent_ids, supp_id):
            # start creating tree and insert root
            tree = Tree()
            tree_id = 0
            iterator = 0
            tree.create_node(tag=sent, identifier=tree_id, data=sent_ids)

            # iterate over leaves, get probs and insert them to tree
            while iterator < (self.beam_width ** self.beam_depth - 1) / (self.beam_width - 1):
                poss_ids, poss_words, probs = get_probs(tree.get_node(iterator).data)
                for id, word, prob in zip(poss_ids, poss_words, probs):
                    # append new possible tokens to tokens along the path
                    sent_ids = torch.cat((tree.get_node(iterator).data, torch.tensor([[id]])), dim=1)
                    if id == supp_id:
                        print("Heureka")
                        return 1, sent_ids
                    tree_id += 1
                    tree.create_node(tag=word + "(" + str(round(prob * 100, 2)) + ")", identifier=tree_id,
                                     data=sent_ids, parent=iterator)
                iterator += 1

            print("Support not found: Do random Step")
            return 0, tree.get_node(tree_id).data
            #tree.show()
            #print(tree.all_nodes_itr())



        sent = input[0]
        sent_ids = torch.tensor(self.tokenizer.encode(input.pop(0))).unsqueeze(0)
        support = "a " + " ".join(input)
        supp_ids = self.tokenizer.encode(support)[1:]
        while len(supp_ids) > 0:
            res, sent_ids = beam_search(sent, sent_ids, supp_ids[0])
            if res:
                supp_ids.pop(0)

            #convert result from ids to string
            tokens = self.tokenizer.convert_ids_to_tokens(sent_ids.tolist()[0])
            print(self.tokenizer.convert_tokens_to_string(tokens))



if __name__ == '__main__':
    model = Model()
    model.generate(["My Name is Harry", "Potter", "met", "Voldemort", "battle" ,"was", "strong", "Hospital"])
