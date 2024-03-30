# MuTaGENe-Replication-Package

This project is the replication package for the paper entitled *Experimenting with MuTaGENe: a custom GPT model to create
domain-aware model mutations* submitted to MODELS2024. 

## Setting up

Unfortunately, the OpenAI’s policy prevents us from publishing MuTaGENe in the GPT store anonymously. We will make MuTaGENe available in case of acceptance. However, this repository provides all the materials available in the knowledge and the instruction set provided in the corresponding `Instruction.md` file. It is worth mentioning that repeating the same instruction set can lead to different results/outcomes due to the generative nature of the GPTBuilder tool. Nevertheless, we report the entire conversation used in the file. 


## Project structure
We describe the content of this repository in the following



### GPT_KB
The `GPT_KB` directory is designated for knowledge base files that are specifically formatted or structured for use with the custom GPT. In particular, the knowledge is composed of the following files:

#### Wodel artifacts


- Sample projects: They are loaded in the KB as .zip files and cover three different application domains, i.e., generic UML models (UMLDiagrams.zip), business process (BPEL.zip), and finite automata (DFAsample.zip). We elicit those projects since they include a larger number of examples. We used the remaining ones as testing while we excluded WodelEdu and LogicCircuits projects since the structure is different compared to standard Wodel projects 
 
- Github parsed documentation: For each project (including the testing ones) we devise a set of scripts (see `parse_documentation.py`) to parse the documentation available on the corresponding {GitHub website} [https://gomezabajo.github.io/Wodel/samples.html]





#### Helpers 
- grammar_utils.py: This file contains a set of tailored functions
employed to parse the Wodel grammar syntax  devoted to the extraction of the DSL;
- parse_documentation.py: This function is used to analyze
the parsed GitHub documentation depicted in Figure 5, thus
helping MuTaGENe during the reasoning phase.
- mapping_models.py: This file contains a dedicated set of
functions that exploits the PyEcore library to parse the
modeling artifacts, i.e., the metamodel and the seed model
expressed in .ecore and .xmi format, respectively

### RQ1
This folder contains all the materials used to answer the first research question (RQ1) outlined in our project. For each project, we include the output of the Wodel program, the generated files by MuTaGENe, the metamodel and the corresponding seed model. 

### RQ2
Similar to the `RQ1`, this folder contains the data used to answer the second research question (RQ2). We adopt the same structure as described for `RQ1` folder. 



### RQ3
This folder holds the data to replicate the experiment discussed in the third research question (RQ3). In particular, each subfolder represents a *mutation scenario* described in the paper. Each subfolder contains the seed model, the generated mutants, and the `pe-string.txt` file that contains the query prompt. 



