# Project example

This is an example project. Copy and rename it to make new projects.

# Basic instructions

To fork:
Create a new, empty project repository on github.mit.edu. Let's call it \<project name\>. Then,
```bash
git clone git@github.mit.edu:rrg/project_example.git <project name>
cd <project name>
<Set up the project>
git remote set-url origin git@github.mit.edu:rrg/<project name>.git
```

To download a project with submodules:
```
git clone --recursive git@github.mit.edu:rrg/project_example.git
```

To make a project:
```
 mkdir build
 cd build
 cmake ..
 make
```

To update a project with submodules:
```
git fetch                               # grab any changes
git rebase -p                           # apply them
git submodule sync --recursive          # ensure submodule urls are in sync
git submodule update --init --recursive # update or initialize submodules
make -C build
```
