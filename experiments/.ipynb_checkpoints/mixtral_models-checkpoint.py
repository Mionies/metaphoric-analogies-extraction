import json
import ast
import logging
import os
from time import sleep
from typing import List
from datasets import load_dataset
from transformers import AutoTokenizer
import transformers
import torch
import copy 

data = json.load(open("../data/signed-met-dataset-v1/signed-met-for-experiments.json"))


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


def get_reply(text):
    sequences = pipeline(
        text,
        #do_sample=True,
        #top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        #max_length=50,
    )     
    o = sequences[0]['generated_text']
    print(o)
    return o







# for mixtral
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
		p+=[f"<s> [INST] Example {i}:\nText containing a metaphor: \"{x[1]}\"\nConcept "
		f"{cnames[c]}: \"{x[2][c]}\"[/INST]\n Answer : \nT1: {x[2][0]}\nT2: {x[2][1]}\nS1: "
		f"{x[2][2]}\nS2: {x[2][3]}\n</s>\n"]
	q= [f"\n<s> [INST] Now it is your turn.Here is a sentence containing a metaphor: \"{test_example[1]}\""
	f"\nHere is a concept {cnames[c]}: \"{test_example[2][c]}\"\n[/INST]\nAnswer:\nT1: "]
	p+=q
	return "".join(p)


        

if __name__ == '__main__':



	model_id = "Mixtral-8x22B-Instruct-v0.1"
	model_id = "Mixtral-8x22B-Instruct-v0.1"


	# set quantization configuration to load large model with less GPU memory
	# this requires the `bitsandbytes` library
	bnb_config = transformers.BitsAndBytesConfig(
	    load_in_4bit=True,
	    bnb_4bit_quant_type='nf4',
	    bnb_4bit_use_double_quant=True,
	    bnb_4bit_compute_dtype=torch.bfloat16
	)

	# begin initializing HF items, need auth token for these

	model_config = transformers.AutoConfig.from_pretrained(
	    model_id,
	)

	# initialize the model
	model = transformers.AutoModelForCausalLM.from_pretrained(
	    model_id,
	    trust_remote_code=True,
	    config=model_config,
	    quantization_config=bnb_config,
	    device_map='auto',
	)
	model.eval()

	tokenizer = transformers.AutoTokenizer.from_pretrained(
	    model_id,
	)

	pipeline = transformers.pipeline(
	    "text-generation",
	    tokenizer=tokenizer,
	    model=model,
	    torch_dtype=torch.float16,
	    device_map="auto",
	)

	tokenizer = AutoTokenizer.from_pretrained(model_id)
	dadi = clean_brackets(data)
	answers = {}
	for i in range(10): 
		print(i)
		answers[i]={0:[],1:[],2:[],3:[]}
		n = 0
		for j in dadi[i]["test"]:
			print(i,n)
			for k in range(4):
				p = prompt(dadi[i]["input"],j,k)
				print(p[-150:])
				answer =get_reply(p)
				answers[i][k].append(answer)
				#print(answer)
				n+=1
			with open("mixtral-xx-answers.json", "w") as outfile:
				json.dump(answers,outfile,indent="\t")

