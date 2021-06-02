"""Byte pair encoding utilities"""
import os
from pytorch_pretrained_bert import BertTokenizer


class Encoder:
    def __init__(self, filename):
        self.vocab_file = "./gpt2/vocab.txt"
        self.tokenizer = self.bert_tokenizer()
    
    def bert_tokenizer(self):
        tokenizer = BertTokenizer.from_pretrained(self.vocab_file, do_lower_case=False)
        return tokenizer
    def encode(self, text):
        print(text)
        print(self.tokenizer.tokenize(text))
        
        return self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(text))

    def decode(self, tokens):
        return " ".join(self.tokenizer.convert_ids_to_tokens(tokens.tolist())).replace(' ##','')

def get_encoder(model_name):
    return Encoder(os.path.join('models', model_name, 'sp.model'))
