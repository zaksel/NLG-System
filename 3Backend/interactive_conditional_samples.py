import json
import os
import numpy as np
import tensorflow as tf

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
                 model_name='117M',
                 seed=None,
                 length=None,
                 temperature=1,
                 top_k=0, top_p=0.9):

        self.enc = encoder.get_encoder(model_name)
        hparams = model.default_hparams()
        with open(os.path.join('./data/models', model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))

        if length is None:
            length = hparams.n_ctx // 2
        elif length > hparams.n_ctx:
            raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

        self.sess = tf.Session()
        self.sess_debug = tf_debug.LocalCLIDebugWrapperSession(self.sess)

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

    def generate(self, raw_text):
        context_tokens = self.enc.encode(raw_text)

        out = self.sess.run(self.output, feed_dict={self.context: [context_tokens]})[:, len(context_tokens):]   #alternative sess_debug for TFDBG
        text = raw_text + self.enc.decode(out[0])
        return text
