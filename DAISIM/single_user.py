from builtins import abs
from cvxpy import *
import numpy as np
from numpy.ma import abs
import cvxpy as cp
import cvxpy

from util import *

# Assets are in individual units
x_base = np.array([100, 0, 0, 0])
assets = np.sum(x_base)

debug = False

def get_optimization_params():

    #NOTE:
    # These are set statically ( no dynamical update to belief)
    # This is fine for a system identifcation problem probably

    mu = np.array([.08, .22, .18, .16, 0.18])  # returns

    cor = np.array([[1, 0, 0, 0, 0], [0, 1, 0.2, 0.9, 0.2], [0, 0.2, 1, 0.1, 1], [0, 0.9, 0.1, 1, 0.1],
                    [0, 0.2, 1, 0.1, 1]])  # correlation matrix

    # Diag(std dev)
    d = np.array(
        [[0.2, 0, 0, 0, 0], [0, 0.8, 0, 0, 0], [0, 0, 0.3, 0, 0], [0, 0, 0, .5, 0],
         [0, 0, 0, 0, 0.3]])

    return mu, cor, d


def optimize(belief_factor, x_start, rho, txf, cdprate, w, eth_price, dai_price, debug=True):
    
    # print(w,cdprate," ..what")
    # print("start")
    # NOTE: The original Paper did not have a notion of belief factor
    # NOTE: Also, rho did not appear in constraints but rather the objective
    
    # Compute asset worth given ETH Price
    asset_prices = np.array([1, eth_price, dai_price, eth_price])
    assets_dollars = np.multiply(x_start, asset_prices)
    money = np.sum(assets_dollars)

    # Initial dollar worth
    xo = cp.Parameter(4, nonneg=True)
    xo.value = assets_dollars

    mu, cor, d = get_optimization_params()

    # Covariance Matrix
    cvr = (d.dot(cor)).dot(d)

    x = cp.Variable(5)
    eth = x[1]
    dai1 = x[2]
    ceth = x[3]
    dai2 = x[4]
    # x[0] is USD

    # include cost of buying ceth as well
    # modified transaction fees
    tx_fee = cvxpy.abs(x[1] - xo[1] + x[3] - xo[3]) * txf + cvxpy.abs(x[2] - xo[2]) * txf

    # objective function
    objective = cp.Maximize(mu.T @ x - w * cp.quad_form(x, cvr) - cdprate * ceth - tx_fee 
                            + belief_factor*(dai2/dai_price)*(dai_price-1) - belief_factor*(dai1/dai_price)*(dai_price-1))
    # higher belief factor I believe is encoding arbitrage -- dai2 is new burn/mint
    # x[0] is USD

    # Figure out how to use abs as a constraint for Maximize
    constraints = [x[0] + x[1] + x[2] + x[3] == money, x >= 0, x[4] == x[3] / rho, x[0] >= tx_fee]

    #NOTE DAI 2 is actually the new  DAI ? it is being constrained to mathc ceth/rho
    # That doesn't make a whole lot of sense -- is it in the paper?

    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.OSQP)

    if prob.status != "optimal":
        print("Not optimal!")
        x_temp = [i for i in x_start]
        return x_temp

    optimal_assets_in_dollars = [float(i) for i in x.value]

    # NOTE: see paper -- equation is exact match to their notation
    transaction_fees = abs(
        optimal_assets_in_dollars[1] - xo.value[1] + optimal_assets_in_dollars[3] - xo.value[3]) * txf + abs(
        optimal_assets_in_dollars[2] - xo.value[2]) * txf

    optimal_assets_in_dollars[0] -= transaction_fees

    if debug:
        print("------------------- Iteration ----------------------------")
        print("CDP Rate: " + str(cdprate) + "\nRisk Averseness: " + str(w))
        print("TxFees: $%.2f" % transaction_fees)

    assets_dollars = optimal_assets_in_dollars[:-1]

    x_temp = np.divide(assets_dollars, asset_prices).clip(min=0)

    if debug:
        printAssets(x_temp, eth_price, dai_price, rho)
        print("--------------------- Ends -------------------------------")

    return x_temp


# Pass asset distribution, ethereum price
def run_loop(eth_price):
    w = 0.001  # Risk Averseness
    rho = 2.5  # Liquidation Ratio
    belief=10

    for cdp_rate in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.34]:
        # template:
        #optimize(belief_factor, x_start, rho, txf, cdprate, w, eth_price, dai_price, debug=True):
        x = optimize(belief, x_base, rho, 0.04, cdp_rate, w, eth_price, 1, True)

        #NOTE: 
        # x_temp is just going to be the desired RESULTING portfolio (after fees are deducted from dollar var)
        # 

if __name__ == '__main__':
    # NOTE: that the eth prices are hard-coded (eth=$130)
    run_loop(130)
