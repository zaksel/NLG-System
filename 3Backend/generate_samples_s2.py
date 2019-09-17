# Strategie 2 Search until fit
import json
import os
import numpy as np
import tensorflow as tf
import time

import sys
sys.path.insert(0, '.\src')
import model, sample, encoder


class Model(object):
    def __init__(self, **kwargs):
        model_name = kwargs['model']
        seed = kwargs['seed']
        length = kwargs['len']
        top_k = kwargs['top_k']
        self.timeout = kwargs['timeout']

        self.enc = encoder.get_encoder(model_name)
        hparams = model.default_hparams()
        with open(os.path.join('./data/models', model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))
        self.lang_model = hparams.n_lang

        self.sess = tf.Session()

        self.context = tf.placeholder(tf.int32, [1, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        self.output = sample.sample_sequence(
            hparams=hparams, length=length,
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
        start = time.time()
        if not self.timeout:
            self.timeout = float("inf")

        context_tokens = self.enc.encode(input.pop(0))
        supp_tokens = [self.enc.encode(supp_words) for supp_words in input]

        while len(supp_tokens) > 0 and (time.time()-start < self.timeout):
            sample = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})
            sample_simp = [self.enc.encode(word) for word in self.enc.decode(sample[0]).split(" ")] #decode, split into single words and encode them back

            if supp_tokens[0] in sample_simp:    # find sub-list from supp_tokens in list of generated tokens
                print("used token: ", supp_tokens[0])
                # print(self.enc.decode(sample[0]))
                context_tokens = sample[0]
                supp_tokens.pop(0)
        text = self.enc.decode(context_tokens)
        return text
