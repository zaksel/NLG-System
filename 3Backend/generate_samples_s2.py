# Strategie 2 Search until fit
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
                 model_name='117M',
                 seed=1,
                 length=5,
                 temperature=1,
                 top_k=40, top_p=0,
                 lang_target='de'):

        self.enc = encoder.get_encoder(model_name)
        self.translator = googletrans.Translator()
        hparams = model.default_hparams()
        with open(os.path.join('./data/models', model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))
        self.lang_model = hparams.n_lang
        self.lang_target = lang_target

        self.sess = tf.Session()

        self.context = tf.placeholder(tf.int32, [1, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        self.output = sample.sample_sequence(
            hparams=hparams, length=length,
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
        context_tokens = self.enc.encode(input.pop(0))
        supp_tokens = []
        for supp in input:
            supp_tokens.extend(self.enc.encode(supp))
        while len(supp_tokens) > 0 and (time.time()-start < 600):
            sample = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})
            if supp_tokens[0] in sample[0]:
                print("used token: ", supp_tokens[0])
                print(self.enc.decode(sample[0]))
                context_tokens.extend(sample[0])
                supp_tokens.pop(0)
        text = self.enc.decode(context_tokens)
        return text

if __name__ == '__main__':
    model = Model()
    start = time.time()
    print(model.generate(["Push the button", "right", "activate", "camera", "pictures", "family", "animals."]))    #a
    #print(model.generate(["The C625AF camera", "five flash modes", "red-eye", "lens", "protected", "UV Filter.", "auto focus", "programmed shutter", "camera case"]))   #b
    #print(model.generate(["If the viewfinder", "not sharp", "check", "eyepiece diopter adjustment", "knob", "near to the eyepiece.", "On-Off control", "button", "handgrip on the right", "thumb", "one press", "recording", "second", "stop."]))  #c
    print(time.time()-start)
