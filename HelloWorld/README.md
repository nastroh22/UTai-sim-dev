## Guide

## Getting Started
- Create a [new julia package](https://pkgdocs.julialang.org/v1/creating-packages/) local to your python project

- [Install pyjulia](https://pyjulia.readthedocs.io/en/latest/installation.html)

- Move to project home directory and try the following code to see that the basic setup is working

## Adding Dependencies
As the project gets more complex, we likely are going to start having many dependencies pile up both in julia and python. This is really the key problem we want to solve. Here's a simple test to check that the tools we have in place are up for the task:

### Method 1 : Add From Julia RePL
- navigate back to HelloWorld
    `cd HelloWorld'

### Setup Script
- alternatively, we can take care of it all automatically (almost) just abstracting it away into a setup script which we can run in python or julia. I'm choosing python here. 

In setup.py, add these lines
- 
`
  from julia import Main
  Main.include("path/to/script.jl")
`

In script.jl, instantiate and activate the package
`  
    using Pkg
    Pkg.instantiate()
    Pkg.precompile()
`

### Run Your Projecct
In the python file that drives the project, make sure to add your package. Then you should be good to go.
` 
    Pkg.activate("/path/to/MyJuliaProject") 
`
