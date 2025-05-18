import os
from collections import Counter


def get_project_dependencies(source_directory, target_language):

    dependency_file = {
        "py": "requirements.txt",
        "js": "package.json",
        "c": "Makefile",             # C projects typically use Makefile or CMakeLists.txt
        "rs": "Cargo.toml",   
    }

    most_common_extention = detect_language(source_directory=source_directory)

    dependency_file_name = dependency_file.get(most_common_extention, None)

    print(dependency_file_name)
    
    
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
        
                