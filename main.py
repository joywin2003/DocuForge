# from google.adk.agents import LlmAgent, BaseAgent
import os
import shutil
import re
from git import Repo
from pydantic import BaseModel


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


    # most_common_extention = detect_language(clone_dir)

    
    return {"root_folder" : f"{folder_name}"}


if __name__ == "__main__":
    repo = RepoLink(repo_url="https://github.com/joywin2003/gameApp-dotnet.git", srclang="en", destlang="hi")
    clone_github_repo(repo)