# TODO: Update the read me
# (steps that might work ? )
""" 
    - install pyjulia

    - activate the environment of julia package & install
    - probabbly the steps are soemthing like:
        - Pkg.precompile(path_to_source)
        - Pkg.activate("bilevel")
        
        # By name
        Pkg.develop("Example")

        # By url
        Pkg.develop(url="https://github.com/JuliaLang/Compat.jl")

        # By path
        Pkg.develop(path="MyJuliaPackages/Package.jl")
"""
from julia import Julia
jl = Julia(compiled_modules=False)
from julia import Main, Pkg
import os
import numpy
import pandas as pd

NAME="HelloWorld"
PARENT=os.path.abspath(os.path.join(__file__,".."))
PROJECT_PATH=f"{PARENT}/{NAME}/src/{NAME}.jl" #NOTE: assumes standard naming

#NOTE: Must Add the Local Definition to LOAD_PATH if not registered remotely
# e.g. see issue 179 resolution: https://github.com/JuliaPy/pyjulia/issues/179

def add_to_path(demo=False,abspath=None):
    """NOTE:
        If the package is not registered remotely, must add the path
    to the local defintiion to julia's LOAD_PATH env variable, 
    e.g. see issue 179 resolution: https://github.com/JuliaPy/pyjulia/issues/179

        Probably preferred anyway. Slightly more flexible unless someone is 
    actively managing their project remotely while under development.
    """
    if demo:
        print("\nJulia LOAD_PATH Before:")
        Main.eval("println(LOAD_PATH)")
        print("\nAfter:")
    if (abspath):
        Main.eval(f'push!(LOAD_PATH, "{abspath}")')
    else:
        Main.eval(f'push!(LOAD_PATH, "{PROJECT_PATH}")')
    if demo:
        Main.eval("println(LOAD_PATH)")

if __name__ == "__main__":

    # first add the project to path
    add_to_path() # no arg passes default

    # Now activate the package
    print("\nLoad Test...\n---------------------")
    Pkg.activate("HelloWorld")
    from julia import HelloWorld as hello # now can import as if native to python
    hello.greet()

    print("\nDependency Test...\n---------------------")
    # NOTE: if project isn't already precompiled, you probably need this step
    # Main.include("./HellowWorld/activator.jl") 
    
    hello.checkDependencies()

    # This makes a csv random numbers "output.csv" in project home directory
    hello.makeRandFrame()

    # Then we can read, and try passing data back to julia module
    print("\nData Passing Test...\n---------------------")
    arr=pd.read_csv("output.csv").to_numpy()
    print("On the Python side, numpy array \n", arr.shape)
    print("First column: ", arr[:,0])
    hello.readSomeData(arr)
    hello.plotSomeData(arr) 

    print("\nDone. Made 'my_plot.png' & 'output.csv'\n")