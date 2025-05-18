# from google.adk.agents import LlmAgent, BaseAgent
import os
import shutil
import re
from git import Repo
from pydantic import BaseModel
# from .utils.depedency import detect_language
import os
from collections import Counter

def get_directory_structure(path):
    """
    Returns the directory structure for the given path.
    
    Args:
        path (str): The starting file or directory path.
    
    Returns:
        dict: A dictionary representing the directory structure.
    """
    structure = {}
    dir_to_ignore = ['Data', 'Migrations']
    files_to_ignore = ['.db','.http', '.sln', '.gitignore']
    if os.path.isdir(path):  # Check if the path is a directory
        dir_name = os.path.basename(path)
        if dir_name in dir_to_ignore:
            return None
        structure[os.path.basename(path)] = {
            item: get_directory_structure(os.path.join(path, item))
            for item in os.listdir(path) 
            if not os.path.isfile(os.path.join(path, item)) or not os.path.splitext(item)[1] in files_to_ignore
        }
    elif os.path.isfile(path):  # If it's a file, return None to indicate a file
        ext = os.path.split(".")[-1]
        return None
    return structure


def detect_language(source_directory):
    
    file_extensions = []
    
    supported_langauges = ['cs']
    
    for _, _, filenames in os.walk(source_directory):
        for filename in filenames:           
            ext = filename.split(".")[-1]
            if ext in supported_langauges:
                file_extensions.append(ext)
                print(ext)
    extension_counts = Counter(file_extensions)
    most_common_extension, _ = extension_counts.most_common(1)[0]
    print(extension_counts.most_common())
    print(extension_counts.most_common(1))
    print(extension_counts.most_common(1)[0])
    return most_common_extension

class RepoLink(BaseModel):
    repo_url : str
    srclang:str
    destlang:str

def clone_github_repo(repo : RepoLink):
    print(repo.repo_url)
    clone_dir = "./repos"
    pattern = r"[^/]+(?=\.git$)"

    folder_name  =  re.search(pattern=pattern, string=repo.repo_url).group()
    print(folder_name)
    clone_dir += "/" + folder_name
    
    if os.path.exists(clone_dir)  and os.path.isdir(clone_dir):
        shutil.rmtree(clone_dir)
        print('folder removed')
    else:
        print('folder does not exist')

    Repo.clone_from(repo.repo_url, clone_dir)

    git_dir = os.path.join(clone_dir, '.git')
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)
        print('.git directory removed')
    else:
        print('.git directory does not exist')


    most_common_extention = detect_language(clone_dir)
    file_structure = get_directory_structure(clone_dir)
    print("1.", most_common_extention)
    print("2.", file_structure)

    
    return {"root_folder" : f"{folder_name}"}


if __name__ == "__main__":
    repo = RepoLink(repo_url="https://github.com/joywin2003/gameApp-dotnet.git", srclang="en", destlang="hi")
    clone_github_repo(repo)
    # structure = get_directory_structure("./repos")
    # print(structure)