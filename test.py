import os

def list_files_with_full_path(directory):
    files_with_paths = [
        os.path.join(directory, filename) 
        for filename in os.listdir(directory) 
        if os.path.isfile(os.path.join(directory, filename))
    ]
    return files_with_paths

# Example usage
directory = "./pdfs"
files = list_files_with_full_path(directory)
print(files)

