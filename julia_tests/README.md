## Use ROS to Handle Message Passing

- Student in David's lab was working on this (Christian ?)
- Also found this : https://jdlangs.github.io/RobotOS.jl/stable/#full-example

## Purpose

- Use Julia for the solver and Use Python to run the simulation
- In Loop, so:
    - Run Julia Solver (could be up to a few seconds per step form prior experiments)
    - Pass stability rate parameter to Python, run a step of python sim
    - Pass DAI price, ETH price (and forecasts), burn/mint action (net?) back to julia (new state info)
 might be more efficient than th back and forth method listed here in the example directory

https://medium.com/@bkamins/julia-and-python-better-together-a60676081008#:~:text=There%20are%20two%20Julia%20packages,Python%20from%20the%20Julia%20language.