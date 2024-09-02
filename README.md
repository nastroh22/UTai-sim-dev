## Original DAISIM 

Ignore daisim stuff on this branch

## This Branch
Is about building and testing julia integration. The HelloWorld README.md has more information, but here is a basic overview of what happens so far
- We add a custom julia project locally to a python project home folder (here we're assuming the julia project has been developed previously)
- HelloWorld is our pre-developed julia package in this example
- Then we install and instantiate the julia package from a local python script "julia_setup_test.py" 
- Now the package works as if it were native to python. We can use pyjulia to simply import it like any other python package
- We run a few tests calling the julia pacakges functions "hello.greet()", "hello.makeRandFrame()", "hello.checkDependencies()", "hello.

- Finally, we test passing some data back and forth. The HelloWorld package receives soem data read in by pandas.to_csv() method and plots it using the julia-native Plots.jl package with "hello.readSomeData()" , ""hello.plotSomeData()"

## Running
- Will need an Julia Installation. Will need python and the listed python dependencies.
- Will need to precompile HelloWorld package. Either do this in the Julia REPL
```
   cd HelloWorld
   julia
   ]
   activate .
   instantiate
   precompile
```  
- Or might work by uncommenting line 67 in julia_setup_tests.py
- Then simply run 
   ` julia_setup_tests.py `

## To Do:
- Test with ParametericMPCs
- Ideally, we'd like to only precompile and setup one time in a "session" -- or at least ensure we are not precompiling every time (actually I think this might already be the case)
- For Patrick -- test this out with your ROS stuff 

- See  "new_instance_test.py"  -- the point is that sartup overhead is pretty slow -- would be nice if it were faster
