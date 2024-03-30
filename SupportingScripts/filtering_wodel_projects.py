import os, re
import zipfile
from pathlib import Path
import shutil
from GPT_KB.grammar_utils import parse_mutator_file, prompt_generator

ROOT_WODEL= 'Wodel_sample/'
ROOT = "C:/Users/claud/OneDrive/Desktop/GPT_KB/Project_samples/"
ROOT_RQ1= "C:/Users/claud/OneDrive/Desktop/paperTo Submit/Repos/ModelMutator-Replication-Package/RQ1/"
ROOT_RQ2 = "C:/Users/claud/OneDrive/Desktop/paperTo Submit/Repos/ModelMutator-Replication-Package/RQ2/"

def unzip_folders():
    """
    Unzip all .zip files found in the specified folders within the root path.

    Parameters:
    - root_path: The root directory containing the folders.
    - folder_list: A list of folder names (str) to look for .zip files to unzip.

    Returns:
    - A list of tuples with the format (zip_path, extraction_status) where extraction_status
      is a boolean indicating whether the extraction was successful.
    """
    for folder_path in os.listdir(ROOT):


        zip_path = os.path.join(ROOT, folder_path)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract all the contents into the same folder
                zip_ref.extractall(zip_path + '_extracted')

        except zipfile.BadZipFile:
            print(f"Bad zip file: {zip_path}")
            #àextraction_results.append((folder_path, False))
        except Exception as e:
            print(f"Error extracting {zip_path}: {e}")
            #extraction_results.append((folder_path, False))

    return


def extract_and_consolidate(root_path, output_folder):
    """
    Navigate a project structure from `root_path` to find and consolidate
    files from folders named 'model' and 'src' into `output_folder`.

    Parameters:
    - root_path: The starting directory to search for 'model' and 'src' folders.
    - output_folder: The directory where all files will be consolidated.

    Note: If there are filename conflicts, files will be renamed to avoid overwriting.
    """
    # Define the folders to look for
    target_folders = ['model', 'src']
    # Ensure the output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(root_path):
        # Check if the current folder is one of the targets
        if os.path.basename(root) in target_folders:
            for file in files:
                # Construct the source file path
                src_path = os.path.join(root, file)
                # Construct the target file path
                dest_path = os.path.join(output_folder, file)

                # Check for filename conflicts
                if os.path.exists(dest_path):
                    # Generate a new file name to avoid overwriting
                    unique_id = 1
                    new_file_name = f"{Path(file).stem}_{unique_id}{Path(file).suffix}"
                    dest_path = os.path.join(output_folder, new_file_name)
                    # Increment the unique_id until a new, non-conflicting name is found
                    while os.path.exists(dest_path):
                        unique_id += 1
                        new_file_name = f"{Path(file).stem}_{unique_id}{Path(file).suffix}"
                        dest_path = os.path.join(output_folder, new_file_name)

                # Copy the file to the output folder
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")
            else:
                print('not mapped')

    print("Consolidation complete.")


#unzip_folders()

def extract_gpt_kb():



    for parent in os.listdir(ROOT_WODEL):
        for child in os.listdir(ROOT_WODEL + parent):
            for wodel_proj in os.listdir(ROOT_WODEL + parent + '/' + child):
                in_path = ROOT_WODEL + '/' + parent + '/' +child + '/' + wodel_proj
                extract_and_consolidate(in_path, 'GPT_KB/'+parent+'/'+ wodel_proj)





def count_folders_and_file_types(root_path):
    """
    Count the number of folders inside the root_path and for each folder,
    print the number of .model and .mutator files.

    Parameters:
    - root_path: The root directory to start the search.
    """
    folder_count = 0
    for root, dirs, files in os.walk(root_path, topdown=True):
        # Only proceed if we're directly inside the root folder
        if root == root_path:
            folder_count = len(dirs)  # Count folders directly under root
            print(f"Total folders inside root: {folder_count}")
            break  # Exit after processing the root directory
    tot_mut = 0
    tot_model = 0

    for dir_name in dirs:
        folder_path = os.path.join(root_path, dir_name)
        count_mutator = 0
        count_model = 0

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.mutator'):
                    count_mutator += 1
                elif file.endswith('.model'):
                    count_model += 1

        print(f"Folder '{dir_name}' has {count_mutator} .mutator files and {count_model} .model files")
        tot_mut += count_mutator
        tot_model += count_model

    print(tot_mut, tot_model)


root_project = ROOT + 'DFASamples.zip_extracted/'
MM_SRC = root_project +"SecurityPolicy.ecore"
MD_SRC = root_project + "LibraryRBAC.model"
MU_SRC = root_project + "SecurityPoliciesExample.mutator"

print(prompt_generator(root_project +'Security_rtt',MM_SRC, MD_SRC, MU_SRC))

count_folders_and_file_types(root_project)

