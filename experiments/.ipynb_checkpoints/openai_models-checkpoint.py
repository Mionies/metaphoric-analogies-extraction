import json
import ast
import logging
import os
from time import sleep
from typing import List
import copy 
import openai

data = json.load(open("../data/signed-met-dataset-v1/signed-met-for-experiments.json"))
openai.api_key = "add-your-key-here"


def get_reply(model, text):
    while True:
        try:
            reply = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": text}],)
            break
        except Exception:
            print('Rate limit exceeded. Waiting for 10 seconds.')
            sleep(10)
    o = reply['choices'][0]['message']['content']
    print(o)
    return o


def clean_brackets(dataset):
	d = {}
	for run_id in dataset:
		d[int(run_id)]={}
		for s in dataset[run_id]:
			d[int(run_id)][s]=[]
			for x in dataset[run_id][s]:
				k = copy.deepcopy(x)
				for i,v in enumerate(k[2]):
					if "<" in v:
						#print(v)
						v = v.split(">")[0].strip("<")
						#print("\t"+v)
						k[2][i]=v
					if "/" in v:
						print(v)
						v = v.split("/")[0]
						print("\t"+v)
						k[2][i]=v
				d[int(run_id)][s].append(k)
	return d





def prompt(input_examples, test_example,c ):
	cnames = ["T1","T2","S1","S2"]
	p = ["Let T1, T2, S1 and S2 be four concepts forming a metaphor in a short text. "
	"The relation between the concepts T1 and T2 is analogous to the relation between the concepts S1 and S2. " 
	"The two concepts T1 and T2 belong to the target domain of the metaphor, they express the main topic discussed in the text. "
	"The two concepts S1 and S2 belong to the source domain of the metaphor, they express the image of the metaphor."
	"Given a short text that contains a metaphor, and one of the four concepts, "
	"your task is to find three other concepts forming a metaphor with it in the text." 
	"The provided concept and the three extracted concepts must together form an analogy."
	"Sometimes, T1, T2, S1 or S2 might be implicit in the text (the word might not appear in the text),"
	"and in this case you should infer a correct concept.\n\n"
	]
	for i,x in enumerate(input_examples):
		p+=[f"Example {i}:\nText containing a metaphor: \"{x[1]}\"\nConcept "
		f"{cnames[c]}: \"{x[2][c]}\"\nAnswer : \nT1: {x[2][0]}\nT2: {x[2][1]}\nS1: "
		f"{x[2][2]}\nS2: {x[2][3]}\n\n"]
	q= [f"\nNow it is your turn. Here is a sentence containing a metaphor: \"{test_example[1]}\""
	f"\nHere is a concept {cnames[c]}: \"{test_example[2][c]}\"\n\nAnswer:\nT1: "]
	p+=q
	return "".join(p)


dadi = clean_brackets(data)
answers = {}

for model in ["gpt-3.5-turbo","gpt-4"]:
	answers[model]={}
	for i in range(10): 
		answers[model][i]={0:[],1:[],2:[],3:[]}
		for j in dadi[i]["test"]:
			for k in range(4):
				p = prompt(dadi[i]["input"],j,k)
				print(p[-150:])
				answer =get_reply(model,p)
				answers[model][i][k].append(answer)
				print(answer)



with open('openai-answers.json', 'w', encoding='utf-8') as file:
	json.dump(answers, file, indent='\t', ensure_ascii=False)

