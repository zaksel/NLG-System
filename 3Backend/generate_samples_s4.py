#Strategie 4 Bert-GPT2 Hybrid
import json
import os
import numpy as np
import tensorflow as tf
import torch
from pytorch_pretrained_bert import BertTokenizer, BertForMaskedLM

import sys
sys.path.insert(0, '.\src')
import model, sample, encoder


class Model(object):
    def __init__(self, **kwargs):
        model_name = kwargs['model']
        seed = kwargs['seed']
        self.length = kwargs['len']
        top_k = kwargs['top_k']

        self.enc = encoder.get_encoder(model_name)
        hparams = model.default_hparams()
        with open(os.path.join('./data/models', model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))

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
            text = text.replace(' ##', '').replace(' ,', ',').replace(' . ', ' ') # TODO: decoding destroys grammar like interpunctuation
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

        return output
