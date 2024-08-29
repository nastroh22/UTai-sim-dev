import pyomo.environ as pyo
from pyomo.mpec import *
import pyomo.mpec.plugins.pathampl as path
from pyomo.mpec.plugins.pathampl import *
print(dir(path))

# NOTE: Another thing to try is to use with JUlia
# https://medium.com/@bkamins/julia-and-python-better-together-a60676081008#:~:text=There%20are%20two%20Julia%20packages,Python%20from%20the%20Julia%20language.

#NOTE: Ok yeah I still don't really get how I could just embed my problem naturally
# Check here maybe
# https://github.com/Pyomo/pyomo/blob/main/examples/mpec/linear1_run.mod
# https://ftp.cs.wisc.edu/math-prog/solvers/path/ampl/
# https://gist.github.com/anthonydouc/3d90c9e10674b6e05a9c998a8493d412

model = pyo.ConcreteModel()
solver =  pyo.SolverFactory("pathampl",executable='pathampl')

model.x = pyo.Var(initialize=5.0, bounds=(1,None))
model.y = pyo.Var(initialize=5.0)

def obj_rule(m):
    return (m.x-1.01)**2 + m.y**2
model.obj = pyo.Objective(rule=obj_rule)

def con_rule(m):
    return m.y == pyo.sqrt(m.x - 1.0)
model.con = pyo.Constraint(rule=con_rule)

solver.options['halt_on_ampl_error'] = 'yes'
solver.solve(model, tee=True)

print(pyo.value(model.x))
print(pyo.value(model.y))

## PROBLEM 2


