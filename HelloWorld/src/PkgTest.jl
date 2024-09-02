using Random, Distributions,CSV, DataFrames, Plots, StatsPlots
using Base.Filesystem, Pkg, PyCall

function checkDependencies()
    println("Available packages in the project include:")
    println()
    Pkg.status()
    println("Compare this list to HelloWorld/Project.toml for sanity check.")
    println()
end

function makeRandFrame(;samples=10, sample_size=30)
    d = Normal()
    array=rand(d,(samples,sample_size))
    df = DataFrame(array, :auto)
    CSV.write("output.csv", df)
end

function readSomeData(data::Vector{Vector{Float64}})
    # "Strictly Typed"
end

function readSomeData(data::Any) # "Cheat Code for Max Flexibility?"
    println("\nOn the Julia side...")
    # Cast PyObject into Julia Type with PyCall -- Do We Need This ?
    # julia_array = PyArray{Float64}(data)  # Cast to a Julia Float64 array
    julia_array=[data[row,:] for row in 1:size(data)[1]] # vector of vectors
    # println("What Type is It? " , typeof(data)) 
    println("First column:  ", data[:,1] )
end

function plotSomeData(data::Any)

    julia_array=[data[row,:] for row in 1:size(data)[1]] 
    p1 = plot(julia_array[1], label="Series Sample 1")
    time=[i for i in 1:length(julia_array[1])]
    for row in 1:length(julia_array)
        plot!(time, julia_array[row], label="Series $row", legend=false)
    end
    # Create the histogram in the second panel
    p2 = histogram(vec(data), bins=30, title="Histogram of Combined Data", xlabel="Value", ylabel="Frequency")
    # Display both plots in a 2x1 grid
    p=plot(p1, p2, layout=(2,1))
    # display(p)
    savefig("my_plot.png")
end

