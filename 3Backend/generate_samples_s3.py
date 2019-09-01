# Strategie 3 Cut-off and Insert
import json
import os
import numpy as np
import tensorflow as tf
import googletrans
import time

import sys
sys.path.insert(0, '.\src')
import model, sample, encoder

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
                 length=8,
                 temperature=1,
                 top_k=10, top_p=0,
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

    def generate(self, input):
        #input = self.transl(input, True, self.lang_target, self.lang_model)

        start_token = self.enc.encode(input.pop(0))
        out = self.sess.run(self.output, feed_dict={self.context: [start_token]})
        for support in input:
            context_tokens = self.enc.encode(self.enc.decode(out[0]) + " " + support)
            out = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})

        #add runs at the end to finish sentence
        while True:
            context_tokens = out[0]
            out = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})
            if 13 in out[0][-self.length:]:
                break
        output = self.enc.decode(out[0])
        output = ".".join(output.split(".")[:-1]) + "."  # take only full sentences

        #output = self.transl(output, False, self.lang_model, self.lang_target)
        return output

    def transl(self, input, array, lang_in, lang_out):
        if array:
            translation = []
            for ele in input:
                translation.append(self.translator.translate(ele, src=lang_in, dest=lang_out).text)
        else:
            translation = self.translator.translate(input, src=lang_in, dest=lang_out).text
        return translation

    def stop(self):
        self.sess.close()

if __name__ == '__main__':
    model = Model()
    start = time.time()
    #print(model.generate(["Push the button", "right", "activate", "camera", "pictures", "family", "animals."]))    #a
    #print(model.generate(["The C625AF camera", "five flash modes", "red-eye", "lens", "protected", "UV Filter.", "auto focus", "programmed shutter", "camera case"]))   #b
    #print(model.generate(["If the viewfinder", "not sharp", "check", "eyepiece diopter adjustment", "knob", "near to the eyepiece.", "On-Off control", "button", "handgrip on the right", "thumb", "one press", "recording", "second", "stop."]))  #c
    print(model.generate(["Im Jahr 1953", "MIT", "numerisch gesteuerte Werkzeugmaschine", "NC-Steuerungen", "Koordinatenbewegungen", "Produktionsmaschinen", "alphanumerische Informationen", "automatisch", "Informationen", "digitaler Form", "früher", "Lochstreifen", "heute", "Rechnerspeichermedien", "Server", "Nc-Steuerung", "decodiert", "Verfahrbewegungen", "Interpolation", "feine Schritte", "Sollwertsignale", "Bewegung der Achsen"]))
    print(time.time()-start)
