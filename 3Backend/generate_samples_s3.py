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
    def __init__(self, **kwargs):
        model_name = kwargs['model']
        seed = kwargs['seed']
        self.length = kwargs['len']
        top_k = kwargs['top_k']
        self.lang_target = kwargs['language']

        self.enc = encoder.get_encoder(model_name)
        self.translator = googletrans.Translator()
        hparams = model.default_hparams()
        with open(os.path.join('./data/models', model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))
        self.lang_model = hparams.n_lang    #get the language of the model from Hyperparameter

        # start session
        self.sess = tf.Session()
        self.context = tf.placeholder(tf.int32, [1, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        self.output = sample.sample_sequence(
            hparams=hparams, length=self.length,
            context=self.context,
            batch_size=1,
            temperature=1,
            top_k=top_k, top_p=0
        )

        # restore transformer model from last checkpoint
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('./data/models', model_name))
        saver.restore(self.sess, ckpt)

    def generate(self, input):
        if self.lang_target: input = self.transl(input, True, self.lang_target, self.lang_model)

        start_token = self.enc.encode(input.pop(0))
        out = self.sess.run(self.output, feed_dict={self.context: [start_token]})
        for support in input:
            context_tokens = self.enc.encode(self.enc.decode(out[0]) + " " + support)
            out = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})

        # add runs at the end to finish sentence
        while True:
            context_tokens = out[0]
            out = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})
            if 13 in out[0][-self.length:]:
                break
        output = self.enc.decode(out[0])
        output = ".".join(output.split(".")[:-1]) + "."  # take only full sentences

        if self.lang_target: output = self.transl(output, False, self.lang_model, self.lang_target)
        return output

    def transl(self, input, array, lang_in, lang_out):
        if array:
            translation = []
            for ele in input:
                translation.append(self.translator.translate(ele, src=lang_in, dest=lang_out).text)
        else:
            translation = self.translator.translate(input, src=lang_in, dest=lang_out).text
        return translation

