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

