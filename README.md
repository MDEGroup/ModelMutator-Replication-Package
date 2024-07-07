# MuTaGENe-Replication-Package

This project is the replication package for the paper entitled *On the use of LLMs to support the development of
domain-specific modeling languages* submitted to MDE4Intelligence workshop.

## Setting up

To set up the custom GPT, users can follow the reported conversation exploiting the GPT builder services offered by OpenAI. In addition, the developed GPT, namely MuTaGENe, is publicly available [here](https://chatgpt.com/g/g-7GQpuc3wx-mutagene). 

**It is worth mentioning that repeating the same instruction set can lead to different results/outcomes due to the generative nature of the GPTBuilder tool. Nevertheless, we report the entire conversation used in the instruction file.** 


## Project structure
We describe the content of this repository in the following



### GPT_KB
The `GPT_KB` directory is designated for knowledge base files that are specifically formatted or structured for use with the custom GPT. In particular, the knowledge is composed of the following files:

#### Wodel artifacts


- Sample projects: They are loaded in the KB as .zip files and cover three different application domains, i.e., generic UML models (UMLDiagrams.zip), business process (BPEL.zip), and finite automata (DFAsample.zip). We elicit those projects since they include a larger number of examples. We used the remaining ones as testing while we excluded WodelEdu and LogicCircuits projects since the structure is different compared to standard Wodel projects 
 
- Github parsed documentation: For each project (including the testing ones) we devise a set of scripts (see `parse_documentation.py`) to parse the documentation available on the corresponding [GitHub website] (https://gomezabajo.github.io/Wodel/samples.html)





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


### SupportingScripts

This folder contains the supporting Python scripts, including functions to clean the Wodel project used in the knowledge creation phase and functions employed to produce statistics.





