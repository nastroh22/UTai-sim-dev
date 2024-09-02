using Pkg
println("Including the activator script. This is to test dependency management")
Pkg.instantiate()
Pkg.precompile()
println("Success! You should now be able to use HelloWorld from Python")