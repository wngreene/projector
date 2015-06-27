# module_example

This repository is an example module (package) that will

1. Build, install, and configure a library (rrt).
2. Build and install an executble (rrt_gui).
3. Build unit tests (test_rrt).

It should be used as a reference for how to build software using CMake as well
as a template for starting new modules (packages).

The code itself implements the Rapidly-exploring Random Tree (RRT) algorithm [LaValle 99].

## Maintainer
- Will Vega-Brown (wrvb@csail.mit.edu)

## Dependencies
- OpenCV 2.4.9
- Eigen 3.2
- Doxygen 1.8.6

## Compilation
First, ensure that the dependencies are met and installed to a location where CMake can
find them. The rest of the build process follows the standard convention for CMake projects:
```
cd module_example
mkdir build
cd build
cmake ..
make 
make install
```

## Usage
```
rrt_gui <image> [scale]
```
where `<image>` is a grayscale image representing an occupancy map and `[scale]`
is an optional positive real number representing how much to scale the image.
