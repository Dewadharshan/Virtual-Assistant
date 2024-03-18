import nltk
from nltk.stem.porter import PorterStemmer
import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader


def tokenize(sentence):
    print("sentence",sentence,type(sentence))
    return nltk.word_tokenize(sentence['text'])

def stem(word):
    return stemmer.stem(word)

def bag_of_words(tokenized_sentence,all_words):
    bag = np.zeros(len(all_words),dtype=np.float32)
    for idx,w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag


class neuralnet(nn.Module):
    
    def __init__(self,input_size,hidden_size,num_classes):
        super(neuralnet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out



stemmer = PorterStemmer()
FILE = 'D:\\mini_project\\model_creating\\data_new.pth'
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

device = torch.device('cpu' if torch.cuda.is_available() else 'cpu')
model = neuralnet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

with open("json_dataset_new.json",'r') as file:
    intents = json.load(file)



def analyze_command(sentence):

    sentence = tokenize(sentence)

    for i,word in enumerate(sentence):
        sentence[i] = stem(word)
    print(sentence)

    X = bag_of_words(sentence, all_words)
    X = X.reshape(1,X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)

    _, predicted = torch.max(output,dim=1)
    prob_softmax = torch.softmax(output, dim=1)
    prob = prob_softmax[0][predicted.item()]
    print('final prob = ',prob.item())
    tag = tags[predicted.item()]
    
    for intent in intents['intents']:
        if tag == intent['description']:
            print(intent['description'])
            print("function",intent['functions'])
            print("function",prob.item())
            if prob.item() >= 0.95:
                
                return intent['functions']
            else:
                print("can't find command")
                return None
