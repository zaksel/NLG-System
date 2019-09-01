#Strategie 4 Bert-GPT-2 Hybrid
import json
import os
import numpy as np
import tensorflow as tf
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM
import googletrans
import time

import sys
sys.path.insert(0, '.\src')
import model, sample, encoder

from tensorflow.python import debug as tf_debug


class Model(object):
    """
    Start session
    :model_name=117M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to reproduce
     results
    :nsamples=1 : Number of samples to return total
    :batch_size=1 : Number of batches (only affects speed/memory).  Must divide nsamples.
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
     considered for each step (token), resulting in deterministic completions,
     while 40 means 40 words are considered at each step. 0 (default) is a
     special setting meaning no restrictions. 40 generally is a good value.
    :top_p=0.0 : Float value controlling diversity. Implements nucleus sampling,
     overriding top_k if set to a value > 0. A good setting is 0.9.
    """
    def __init__(self,
                 model_name='ISW_Model',
                 seed=0,
                 length=3,
                 temperature=1,
                 top_k=20, top_p=0,
                 lang_target='de'):

        self.enc = encoder.get_encoder(model_name)
        self.translator = googletrans.Translator()
        hparams = model.default_hparams()
        with open(os.path.join('./data/models', model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))
        self.lang_model = hparams.n_lang
        self.lang_target = lang_target
        self.length = length

        self.sess = tf.Session()

        self.context = tf.placeholder(tf.int32, [1, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        self.output = sample.sample_sequence(
            hparams=hparams, length=self.length,
            context=self.context,
            batch_size=1,
            temperature=temperature,
            top_k=top_k, top_p=top_p
        )

        # restore transformer model from last checkpoint
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('./data/models', model_name))
        saver.restore(self.sess, ckpt)

        # Load pre-trained model (weights)
        self.model = BertForMaskedLM.from_pretrained('bert-base-german-cased')
        self.model.eval()
        # Load pre-trained model tokenizer (vocabulary)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-german-cased', do_lower_case=False)

    def generate(self, input):

        def bert(text):
            print(text)
            tokenized_text = self.tokenizer.tokenize(text)
            for i in range(len(tokenized_text)):
                if tokenized_text[i] == "[MASK]":
                    # Convert token to vocabulary indices
                    indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
                    # Convert inputs to PyTorch tensors
                    tokens_tensor = torch.LongTensor([indexed_tokens])

                    # Predict tokens
                    with torch.no_grad():
                        predictions = self.model(tokens_tensor)

                    predicted_index = torch.argmax(predictions[0,i]).item()
                    predicted_token = self.tokenizer.convert_ids_to_tokens([predicted_index])

                    # fill in prediction
                    tokenized_text[i] = predicted_token[0]

            text = ' '.join(tokenized_text)
            text = text.replace(' ##', '').replace(' ,', ',').replace(' . ', ' ')
            print(text)
            return text

        context_tokens = self.enc.encode(input.pop(0))
        out = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})

        for support in input:
            text = self.enc.decode(out[0]) + " [MASK] " + support
            text_bridge = bert(text)
            context_tokens = self.enc.encode(text_bridge)
            #context_tokens = self.enc.encode(self.enc.decode(out[0]) + " " + support)
            out = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})


        #add runs at the end to finish sentence
        while True:
            context_tokens = out[0]
            out = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})
            if 13 in out[0][-self.length:]:
                break
        output = self.enc.decode(out[0])
        output = ".".join(output.split(".")[:-1]) + "."  # take only full sentences


        #output = ". ".join(output.split(".")[:-1])+"." #take only full sentences
        return output

if __name__ == '__main__':
    model = Model()
    start = time.time()
    #print(model.generate(["Push the button", "right", "activate", "camera", "pictures", "family", "animals."]))    #a
    #print(model.generate(["The C625AF camera", "five flash modes", "red-eye", "lens", "protected", "UV Filter.", "auto focus", "programmed shutter", "camera case"]))   #b
    #print(model.generate(["If the viewfinder", "not sharp", "check", "eyepiece diopter adjustment", "knob", "near to the eyepiece.", "On-Off control", "button", "handgrip on the right", "thumb", "one press", "recording", "second", "stop."]))  #c
    print(model.generate(["Im Jahre 1953", "MIT", "numerisch gesteuerte Werkzeugmaschine", "NC-Steuerungen", "Koordinatenbewegungen", "Produktionsmaschinen", "alphanumerische Informationen", "automatisch", "Informationen", "digitaler Form", "früher", "Lochstreifen", "heute", "Rechnerspeichermedien", "Server", "Nc-Steuerung", "decodiert", "Verfahrbewegungen", "Interpolation", "feine Schritte", "Sollwertsignale", "Bewegung der Achsen"]))

    print(time.time()-start)
