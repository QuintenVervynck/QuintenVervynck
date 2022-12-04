#!/usr/bin/python3

import os

ignore_list = {".DS_Store", ".git", ".gitkeep"}
ignore_extensions = { ".png", ".jpg", ".svg"}
def ignore(name):
    return name not in ignore_list and name.split(".")[-1] not in ignore_extensions

# prefix components:
space =  ' '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '

"""
def tree(dir_path: Path, prefix: str=''):
    #A recursive generator, given a directory Path object
    #will yield a visual tree structure line by line
    #with each line prefixed by the same characters

    contents = list(sorted(filter(ignore, dir_path.iterdir())))
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        name = path.name[:-3] if path.name[-3:] == ".md" else str(path.name)
        if 
        yield f"[`{prefix}{pointer}{name}`]({str(path).replace(' ' , '%20')})"
        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension)


prevline = Path().absolute().name  # get the current dir name
for line in tree(Path()):
    print(prevline + "\\")
    prevline = line
print(prevline)
"""

def create_index():
    with open("index.md", "w") as f:
        f.write("## Roadmap\n")
        years = sorted(os.listdir("roadmap"), reverse=True)
        for i, year in enumerate(years):
            if i == len(years) - 1:
                f.write(f"`└───` `{year}` \\\n")
            else:
                f.write(f"`├───` `{year}` \\\n")
            dirs = sorted(filter(ignore, os.listdir(f"roadmap/{year}")), reverse=True)
            for j, dir in enumerate(dirs):
                # if at the last dir
                if j == len(dirs) - 1:
                    prefix = f"{space}`└─`"
                    suffix = "\\\n"
                else: # if not
                    prefix = f"{space}`├─`"
                    suffix = "\\\n"
                # if the dir is a post (has a README.md)
                if os.path.exists(f"roadmap/{year}/{dir}/README.md"):
                    f.write(f"{prefix} [`{dir[3:]}`]({f'roadmap/{year}/{dir}/README.md'.replace(' ' , '%20')}){suffix}")
                else:  # the dir is a mention (don't want a link to it)
                    f.write(f"{prefix} `{dir[3:]}`{suffix}")
        f.write(space)

if __name__ == "__main__":
    create_index()

