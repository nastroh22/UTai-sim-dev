## Chat GPT generated "switching calls" examples

from julia import Julia
jl = Julia(compiled_modules=False)
from julia import Main

# If you need to use specific Julia packages, you can do so by importing them
# from julia import YourJuliaModule  # Replace with your actual module #NOTE Bilevel Module ??

# Define your Python function
def python_function(input_from_julia):
    # Perform some operation
    output_to_julia = input_from_julia * 2  # Example operation
    return output_to_julia

# Define the initial input
input_to_julia = 1.0  # Example initial value

# Load Julia function
Main.include("julia_function.jl")  # Replace with your Julia script name

# Loop 10 times, passing data between Python and Julia
for i in range(10):
    # Call Julia function with input from Python
    output_from_julia = Main.julia_function(input_to_julia)

    # Process Julia output in Python
    input_to_julia = python_function(output_from_julia)

    print(f"Iteration {i+1}: Julia output = {output_from_julia}, Python output = {input_to_julia}")
