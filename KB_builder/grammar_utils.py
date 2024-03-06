import re



def extract_keywords_from_xtext_file(file_path):
    # Open the file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regular expression to match keywords in the Xtext grammar
    keyword_pattern = re.compile(r"'([^']*)'")

    # Find all instances of the pattern in the content
    keywords = keyword_pattern.findall(content)

    # Remove duplicates by converting the list to a set, then back to a list
    unique_keywords = list(set(keywords))
    print(unique_keywords)
    return unique_keywords


def parse_mutator_file(grammar_file_path, input_file_path):
    # Extract keywords from the Xtext grammar file
    keywords = extract_keywords_from_xtext_file(grammar_file_path)

    # Open the input file and read its content
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # List to keep track of removed keywords
    removed_keywords = []

    # Replace each keyword in the content with an empty string and track removed ones
    for keyword in keywords:
        # Escaping keyword for regex use, in case it contains regex special characters
        escaped_keyword = re.escape(keyword)
        # Check if the keyword exists in the content
        if re.search(f"\\b{escaped_keyword}\\b", content):
            removed_keywords.append(keyword)
            content = re.sub(f"\\b{escaped_keyword}\\b", '', content)

    return content, removed_keywords


def prompt_generator(project,metamodel_file, model_file, mutator_file):
    with open(metamodel_file, 'r', encoding='utf-8') as mm:
        metamodel_content = mm.read()

    with open(model_file, 'r', encoding='utf-8') as md:
        model_content = md.read()

    with open(mutator_file, 'r', encoding='utf-8') as mu:
        rules = mu.read()

    pe_string = f"Given this #ECORE metamodel  {metamodel_content}  and this #SEED model   {model_content} , generate model" \
           f" mutants according to these #RULES <START RULES> {rules}  export the generated mutants in a zip file. Use the content of the prompt to generate the file"
    with open(f"{project}_pe.txt", 'w', encoding='utf-8', errors='ignore') as out_file:
        out_file.write(pe_string )
    return pe_string