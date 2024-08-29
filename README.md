## Original DAISIM 

With a few tweaks to get it working.

cd into DAISIM and then run the following commands: 

 - `python3 sim.py --config configs/sample.config --logdir sim-logs --days_per_config 1` : Running this generates a file `sim-summary.pickle` inside the log directory
    which is used to generate useful plots.

 - `python3 plot_gen.py --data sim-logs/sim-summary.pickle` : Running this generates several useful plots for the simulation. All generated plots would show up in a `plots`
    directory under the log directory.

Will need to have: 

`cvxpy, pickle, numpy, scipy, matplotlib,` 

installed

## This Branch
- Got tons of notes and TODO's right now scattered about in 
      - simulation_util.py
      - feedback_sim.py

- Usage
   - Ensure required libraries are installed, then run:
       `python3 feedback_sim.py`

- Summary of Goals:
   - [ ] Connect PID controller to DAISIM as a bencmarking system for RAI
   - [ ] Connect Bilevel Controller ( either through julia interface (and pycall) or through pyomo directly recreating PATH)
   - [ ] Eventual Possible Inverse or System ID Approaches
         - [ ] Simple Linear Layers or shallow MLP, can it distill a multi-agent simulation ?
         - [ ] Embedded/ Parameterized Agent into the Current Bilevel Framework using iNverse Game Structure (David's paper)
               - I believe this algorithm lends itself to Nash equilibrium specifcially ( not sure about with a leader agent if it fits)
               - Also, could the market interaction be thought of as a Nash Game (although this seems like a separate question and am I just stretching that framework to make it fit ?)
               - https://arxiv.org/pdf/2302.01999
               - brainstorm notes: https://docs.google.com/document/d/1YVklxqTxyuaHRjj0dHEdUn-3P1WDJtHGSNxE4emgBQI/edit
         - [ ] Embedded Least Squares Minimization
            - In this case the upper level agent simply has a least squares objective appended to its optimization problem
            - So it tries to learn parameters jointly with control
            - i.e. we just add something like  Σ_{t-T:t} ( y - ŷ )^2 to the objective
            - Another approach I found in GEKKO tutorials is self-tuning PID (which is not too different than bilevel I think)
         - [ ] Offline Data Driven Methods
            - One approach is generative time series modeling ( David Suggests using with Scenario Based Optimizaiton )
            - more classical approach is VAR or state space modeling


- Diagram of System: (Add later)