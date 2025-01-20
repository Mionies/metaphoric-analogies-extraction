# Exraction of Metaphoric Analogies from Literary Texts

Extracting metaphors and analogies from free text requires high-level reasoning abilities such as abstraction and language understanding. Our study focuses on the extraction of the concepts forming metaphoric analogies in literary texts. To this end, we construct a novel dataset in this domain with the help of domain experts. We compare the out-of-the-box ability of recent large language models (LLMs) to structure metaphoric mappings from fragments of texts containing rather explicit proportional analogies. The models are further evaluated on the generation of implicit elements of the analogy, which are indirectly suggested in the texts and inferred by human readers. The competitive results obtained by LLMs in our experiments are encouraging and open up new avenues such as automatically extracting analogies and metaphors from text instead of investing resources in domain experts to manually label data.

  
### Paper reference 
___

Joanne Boisson, Zara Siddique, Hsuvas Borkakoty, Dimosthenis Antypas, Luis Espinosa-Anke, Jose Camacho-Collados. 2025. *[Automatic Extraction of Metaphoric Analogies from Literary Texts: Task Formulation, Dataset Construction, and Evaluation.](https://arxiv.org/abs/2412.15375)* *Proceedings of the 31th international conference on computational
linguistics (COLING), Abu Dhabi, UAE*. Association for Computational Linguistics.


### What are 4-term metaphoric analogies?
___

  <img width="600" src="img/metaphoric-analogies.png" /> 

We release a dataset of 204 short texts containing a 4-term analogy, where explicit terms are tagged and implicit terms are suggested by annotators.

The data and inter-annotator-agreement test can be found [here](./data).
### Task & Experiments
___

We test the ability of Large Language Models to extract explicit terms of a metaphoric analogy, and generate relevant implicit terms.

**Input** : 
- a short text
- a term T1, T2, S1 or S2

**Instructions**:
- Extract the other explicit terms forming
the 4-terms metaphor
- Generate eventual missing implicit
terms

**Output** :
The structured metaphoric analogy :
values of the 4 frames **T1, T2, S1 and S2**.


- **Prompt used in the experiments**:
  
<p align="center"> 
  <img width="295" src="img/prompt1.png" />
  <img width="275" src="img/prompt2.png" /> 
</p>   

The scripts and output of our experiments with openAI and open source models can be found [here](./experiments).

### Evaluation
___

- [**Explicit terms**](./evaluation/explicit_terms-evaluation) : we evaluate the correctness of the extracted explicit terms using an automatic metric of lemmatized head noun match between the gold standard and the model output.

<p align="center">
    <img width="450" src="img/explicit-terms.png" />
</p>
  
- [**Implicit terms**](./evaluation/implicit_terms-evaluation): the relevance of the generated implicit terms is manually rated.

<p align="center">
  <img align="center" width="550" src="img/implicit-terms.png" /> 
</p>

___

<p align="center">
  <img width="80" src="img/Cardiff_University_(logo).svg" /> 
  <img width="80"  src="img/cardiff-nlp-logo.png" />
</p>

### License
___

CC BY 4.0 [![License: CC BY 4.0](https://licensebuttons.net/l/by/4.0/80x15.png)](https://creativecommons.org/licenses/by/4.0/)

