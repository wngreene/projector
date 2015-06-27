# projector
A convenience tool for creating projects and metaprojects.

### Maintainer
- W. Nicholas Greene (wng@csail.mit.edu)

### Dependencies
- python
- git
- gitpython

### Installation
```
cd projector
python ./setup.py install --prefix=${INSTALL_PATH}
```
where `INSTALL_PATH` must be on your `PYTHONPATH`.

### Usage
```
# Initialize a project.
projector init my_project

# Initialize a metaproject.
projector init -m my_meta_project

# Add a submodule to a project.
projector add <git_url> <path> -d <dependencies>
```
