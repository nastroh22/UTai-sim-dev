from pyomo.environ import *
from pyomo.mpec import *
import pyomo.environ as pyo

agents = ['tomatoes', 'cucumbers', 'fruit']
output_prices = dict(zip(agents, [10,15,20]))
yields = dict(zip(agents, [1,1,1]))
b = dict(zip(agents, [1,1,1]))
c = dict(zip(agents, [0.1,0.1,0.1]))
wr = dict(zip(agents, [3,5,10]))
pw = dict(zip(agents, [1.192, 1.192, 1.192]))
wa = dict(zip(agents, [500, 100, 50]))
model = ConcreteModel()

model.a = Set(initialize=agents)
model.pq = Param(model.a, initialize=output_prices)
model.y = Param(model.a, initialize=yields)
model.b = Param(model.a, initialize=b) 
model.c = Param(model.a, initialize=c)
model.wr = Param(model.a, initialize=wr)
model.pw = Param(model.a, initialize=pw)
model.wa = Param(model.a, initialize=wa)
model.xt = Param(initialize=80)
model.wt = Param(initialize=500)

model.x = Var(model.a, initialize=1)
model.sl = Var()
model.sw = Var()
model.sw_a = Var(model.a)

formulation = 'market'

def foc_rule(a, formulation):
    foc =  2 * model.c[a] * model.x[a] + model.sl 
    if formulation == 'price':
        foc += model.wr[a] * model.pw[a]
    elif formulation == 'market':
        foc += model.wr[a] * model.sw
    elif formulation == 'central':
        print('foc_central')
        foc += model.wr[a] * model.sw_a[a]
    return foc >= model.pq[a] * model.y[a] - model.b[a]

def foc_comp_rule(model, a):
    return complements(foc_rule(a, formulation), model.x[a] >=0)
    
def land_con_rule():
    return model.xt - sum(model.x[a] for a in model.a) >=0

def land_sl_comp_rule(model):
    return complements(land_con_rule(), model.sl >= 0)

def water_con_rule():
    return model.wt - sum(model.wr[a] * model.x[a] for a in model.a) >= 0

def water_cona_rule(a):
    return model.wa[a] - model.wr[a] * model.x[a] >= 0
    
def water_sw_comp_rule(model):
    return complements(water_con_rule(), model.sw >= 0)

def water_swa_comp_rule(model, a):
    return complements(water_cona_rule(a), model.sw_a[a] >=0)

def objective_rule(model):
    prof = sum(model.pq[a] * model.y[a] * model.x[a] - (model.b[a] * model.x[a] + model.c[a] * model.x[a] * model.x[a]) for a in model.a)
    return prof

# model formulations... 
if formulation != 'nlp':
    model.compl_foc = Complementarity(model.a, rule = foc_comp_rule)
    model.compl_land_sl = Complementarity(rule = land_sl_comp_rule)
else:
    model.land_con = Constraint(expr=land_con_rule())
    model.water_con = Constraint(expr=water_con_rule())
    model.objective = Objective(rule=objective_rule, sense=maximize)

if formulation == 'market':
    model.compl_water_sw = Complementarity(rule = water_sw_comp_rule)
elif formulation == 'central':
    model.compl_water_swa = Complementarity(model.a, rule=water_swa_comp_rule)
  
if __name__ == '__main__':
    from pyomo.opt import SolverFactory
    import pyomo.environ
    print(formulation)
    if formulation != 'nlp':
        opt = SolverFactory("pathampl",executable='pathampl')
    else:
        opt = SolverFactory('ipopt', solver_io='nl', executable='ipopt.exe')
    # print(opt.name)
    results=opt.solve(model, tee=True)
    #sends results to stdout
    # results.write()
    print(results)
    
    print("\nDisplaying Solution\n" + '-'*60)
    
    # Access the value of the objective function
    # print(f"Objective value: {model.objective()}")

    # Access the values of variables
    for v in model.component_objects(Var, active=True):
        varobject = getattr(model, str(v))
        for index in varobject:
            print(f"{varobject[index]}: {varobject[index].value}")
    