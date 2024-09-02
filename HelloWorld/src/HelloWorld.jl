module HelloWorld

println("This text is just from including the source script.")
greet() = print(" But this is from activating the package... 
                    \n   Hello World!   \n
")

# NOTE -- or simply add them manually in Julia RepL 
# using Pkg;
# Pkg.add("Distributions");
# Pkg.add("CSV");
# Pkg.add("DataFrames");

include("PkgTest.jl")
export makeRandFrame, checkDependencies, readSomeData, plotSomeData

end # module HelloWorld
