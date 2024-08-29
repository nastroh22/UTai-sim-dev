## Branches
- Ignore template and main for now
- daisim_tests to see original daisim code
- daisim_refactor is current dev branch -- integrates daisim with a pid controller

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
