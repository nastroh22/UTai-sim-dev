import sympy

def supply_const(S,Δ):
    return S + Δ

# [lamb.diff(x) for x in ]
from sympy import symbols, diff

# Define the variables
x1, x2, x3 = symbols('x1 x2 x3')
variables=[x1,x2,x3]

# Define the expression
expression = x1 + x2 + x3**2

# Compute the gradient (partial derivatives)
gradient_x1 = diff(expression, x1)
gradient_x2 = diff(expression, x2)
gradient_x3 = diff(expression, x3)
gradient = [diff(expression, var) for var in variables]

# Print the gradients
print(f'd/dx1: {gradient_x1}')  # Should print: 1
print(f'd/dx2: {gradient_x2}')  # Should print: 1
print(f'd/dx3: {gradient_x3}')  # Should print: 2*x3

from pyomo.environ import ConcreteModel, Var, Objective, Constraint, SolverFactory

model=ConcreteModel()
# Define the variables
model.x1 = Var()
model.x2 = Var()
model.x3 = Var()

varmap=values = {x1: model.x1, x2: model.x2, x3: model.x3}

# NOTE:
# Cool ! this actually seems to work ok 
# Start with symbolic gradient in python -- 
# use the sympy package as an intermediary similar to "Symbolics.jl"
# Pass it into these *arg funcs to dynamicallty assigning vars
# Then you can get a pyomo expression out on the other end

# TODO:
# Testing derived experssion versus hard-coded ( this )
# Write "variable interface / variable Map"
# might also be nice to convert it to a usable package (supporting second-order ?)

# Define the expression and its gradient
def expression_rule(model):
    return model.x1 + model.x2 + model.x3**2
# print(expression_rule(mod))

import sympy as sp

# def template_test():
def lambidfy(func,vars=(x1,x2,x3)):
    return sp.lambdify(vars, func, 'numpy')
    # return func
symgrad=list(map(lambidfy,gradient))

testfunc = sp.lambdify((x1, x2, x3), gradient_x3, 'numpy')
print(testfunc(x1, x2, x3))

def substitute(func,*args):
    # print([arg for arg in args])
    return func(*args)
pyomograd=[substitute(func,model.x1, model.x2, model.x3) for func in symgrad]
# print(substitute(gradient_x3,model.x1.value, model.x2.value, model.x3.value))

print(pyomograd[2])

def expression_function(x1_val, x2_val, x3_val):
    return testfunc(x1_val, x2_val, x3_val)

def pyomo_expression_rule(model):
    return expression_function(model.x1, model.x2, model.x3)

print("target")
print(pyomo_expression_rule(model))