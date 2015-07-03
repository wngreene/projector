# projector
A convenience tool for creating projects and metaprojects.

The `init` subcommand will create a template project for you using
the RRG's agreed upon best practices.

The `init -m` subcommand will do the same for metaprojects.

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

The installation step (to a directory that lies on your `PYTHONPATH`)
allows you to call `projector.py` from any directory.

### Usage
```
# Initialize a project.
projector.py init my_project

# Initialize a metaproject.
projector.py init -m my_meta_project

# Add a submodule to a project.
projector.py add <git_url> <path> -d <dependencies>
```
