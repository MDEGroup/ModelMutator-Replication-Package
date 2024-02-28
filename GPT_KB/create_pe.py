from bs4 import BeautifulSoup
import re
import zipfile
import os
def parse_html(filename='Home.html'):
    dizionario = []
    with open(filename, 'r') as page:
        soup = BeautifulSoup(page.read(), 'html.parser')
        codes = soup.find_all('code')
        for code in codes:
            dizionario.append((code.parent.previous_sibling.previous_sibling.text,code.text))
    return dizionario

def unzip(filename, output_folder='Wodel/zip/automata/'):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
def get_single_project_info(filename):
    mutator = ''
    mutator_folder = os.path.join(filename, "src")
    for file in os.listdir(mutator_folder):
        if file.endswith('.mutator'):
            with open(os.path.join(filename, "src", file)) as reader: mutator = reader.read()
    ecore = ''
    seeds = {}
    model_folder = os.path.join(filename, "data", "model")
    for file in os.listdir(model_folder):
        if file.endswith('ecore'):
            with open(os.path.join(filename, "data", "model", file)) as reader: ecore = reader.read()
        else:
            with open(os.path.join(filename, "data", "model", file)) as reader: seeds[file.replace(".model", "")] = (reader.read())
    outputs = {} 
    model_folder = os.path.join(filename, "data", "out")
    for sub_folder in os.listdir(model_folder):
        #check file is a folder
        if os.path.isdir(os.path.join(model_folder, sub_folder)):
            count = 0
            for name in os.listdir(os.path.join(model_folder, sub_folder)):
                if name.endswith('.model'):
                    with open(os.path.join(model_folder, sub_folder, name)) as reader: outputs[sub_folder + '___' +str(count)] = (reader.read())
    return mutator, ecore, seeds, outputs

def get_info(folder):
    list_of_files = []
    for file in os.listdir(folder):
        if file.endswith('.zip'):
            unzip(folder + "/" + file, folder)
            list_of_files.append(get_single_project_info(folder + '/' + file.replace('.zip', '')))
    return list_of_files
    



def get_ecore(filename=''):
    ecore_link = '' 
    with open('Wodel/' + filename, 'r') as page:
        soup = BeautifulSoup(page.read(), 'html.parser')
        codes = soup.find_all('a')
        for code in codes:
            if code['href'].endswith('ecore'):
                ecore_link = code['href'].replace('https://gomezabajo.github.io/','')
    ecore = ''
    with open(ecore_link, 'r') as reader: ecore = reader.read()
    return ecore
    
    

def get_tutorials(x):
    pe_string = ''
    dis = parse_html(filename='Wodel/' + x)
    for (c,v) in dis:
        pe_string = pe_string + "USER: To " + c + "use the following mutator operator: " + v + "\n"
    return pe_string
def get_static_text(): 
    init = "SYSTEM: You are a AI modeling assistant. You should provide model mutation in XMI format.\n"

    wodel_description = "USER: Wodel is a language to generate mutants for models. \
    It is based on the concept of mutation operators and constraints.\
    The wodel programs are defined among an ecore model notation \n"

    wodel_get_starting = "USER: Wodel provides different facilities to perform model mutations:\
    # SELECTION STRATEGIES: a set of selection strategies fulfilling a conditional clause:\
    * all: a list with all the elements that satisfy the conditional clause.\
    * one: a random element that satisfies the conditional clause.\
    * typed: an element that is of this given type.\
    * closure: the closure of elements of the given reference.\
    * other: a different element to the current element at the given reference.\
    * [variable name]: you can just place the name of a variable in order to apply to it any mutation operator.\
    # Conditional: In order to provide a conditional criterion for the different selection strategies described above, \
    the Wodel DSL provides the keyword 'where' along with the following possibilities:\
    * self: it refers to the object(s) currently taken by the mutation operator.\
    * [feature] = [value]: the given feature has the given value.\
    * [feature] <> [value]: the given feature has a different value from the one given.\
    * [feature] in [list]: the given feature is in the given list.\
    * [feature] is typed [type]: the given feature is of the given type.\
    * [feature] not typed [type]: the given feature is of a different type from the one given.\
    # Operations to modify the object's features: Wodel provides the functionality to modify the different features \
    of the given object(s) with the keyword 'with' along with the following possibilities:\
    * [feature] = [value]: sets the feature to the given value.\
    * [feature] += [value]: adds the given value to the list referenced by the feature.\
    * [feature] -= [value]: removes the given value from the list referenced by the feature.\
    * reverse([boolean feature]): reverses the boolean value of the feature.\
    * swap([feature1, feature2]): swaps the values of the given features.\
    * unset([feature]): unsets the given feature.\
    # Blocks of mutation operators: We can classify the mutation operators in 'blocks' of mutation operators. \
    This way, Wodel will apply each of the declared blocks independently, as independent mutation operators. \
    This is the easiest way to distinguish each mutation operator. To achieve this functionality,\
    we must include the keyword 'blocks' at the beginning of the mutation operators section in the Wodel program. \
    The following example declares the two mutation operators 'rtt' and 'rer' for the Security Policies meta-model.\n"


examples = ['asple.html', 'automata.html', 'bpel.html', 'bpmn.html', 'lc.html','pfsm.html', 'secpol.html','umlcd.html']
for x in examples:

    with open(x + 'txt', 'w') as f:
        tutorial = get_tutorials(x)
        f.write('#TUTORIAL\n\n')
        f.write(tutorial + "\n\n")
        
        # ecore = get_ecore(x)
        # print(ecore)
        # print("=====================================")
        
        results = get_info('Wodel/zip/' + x.replace('.html', ''))
        f.write('#ECORE\n\n')
        f.write(ecore + "\n\n")
        for mutator, ecore, seeds, outputs in results:
            for k, v in outputs.items():
                f.write('#MUTATOR\n\n')
                f.write(mutator + "\n\n")
                f.write('#SEED\n\n')
                f.write(seeds[k.split('___')[0]] + "\n\n")
                f.write('#GENERATED\n\n')
                f.write(v + "\n\n")
#get_info()