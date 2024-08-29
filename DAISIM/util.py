from scipy.stats import truncnorm
from datetime import datetime
from dataclasses import dataclass
import numpy as np
from gbm import gen_paths

############################################################################################################
@dataclass
class SimState:
    num_investors: int
    belief_factor: int
    lambdas: np.ndarray
    agent_type: str # Initialize agents with normal distribution over assets
    days_per_config: int  # Simulate two weeks of data
    runs: int
    eth_price_per_day: list
    cdp_rate : float
    tx_fee: float
    rho: float

def parse_config():
    return 

def set_defaults(sample=10,days=14):
    num_investors=sample # NOTE: 10 is more overhead, maybe use some combinatorial amount which accounts for parameters λ, Β?
    belief_factor=20
    risk_lambdas=np.ones(num_investors)*.005
    agent_type="normal"  # Initialize agents with normal distribution over assets
    days_per_config=days   # Simulate two weeks of data (default of 14)
    runs=1
    apath=gen_paths(100. , r=.005, sigma=.02, M=24*days, T=days, I=runs)
    print(apath.shape)
    eth_price_per_day=list(apath.squeeze())[::24][0:days]
    init_cdp_rate=.06
    init_tx_fee=.02
    init_rho=2.5 # TODO : generalize to a list of params (distribution over users)

    return SimState(
        num_investors,
        belief_factor,
        risk_lambdas,
        agent_type,
        days_per_config,
        runs,
        eth_price_per_day,
        init_cdp_rate,
        init_tx_fee,
        init_rho
    )

### Manually Set the Parameters From Config 
"""
    print("Input Parameters for Test")
    print("--investors", args.investors)
    print("--days_per_config", args.days_per_config)
    print("--type", args.type)
    print("--runs", args.runs)
    print("--log", args.log)
    print("--logidr", args.logdir)
    print("--config", args.config)
"""

### NOTE: ############################################################################################################


def printAssets(x, eth_price, dai_price, rho):
    print("========= Assets ============")
    print("USD         : %.2f" % x[0])
    print("ETH         : %.8f" % x[1])
    print("DAI         : %.8f" % x[2])
    print("Col ETH     : %.8f" % x[3])
    print("DAI Minted  : %.8f" % (x[3] * eth_price / dai_price / rho))
    # print("What is x[4]?: %.8f" % x[4])
    print("=============================")


def printSummary(x, eth_price, dai_price, rho, risk_param):
    print("============= Summary ==============")
    print("Risk Averseness : %.4f" % risk_param)
    print("Holdings in USD : %.4f" % (x[0] + x[1] * eth_price + x[2] * dai_price + x[3] * eth_price))
    print("Debt in USD     : %.4f" % (x[3] * eth_price / dai_price / rho))
    print("====================================")


def printColAssets(x_old, x, eth_price, dai_price, rho, risk_param):
    print("========= Assets Change ============")
    print("Risk Param  : %.4f" % risk_param)
    print("USD         : %.4f => %.4f" % (x_old[0], x[0]))
    print("ETH         : %.4f => %.4f" % (x_old[1], x[1]))
    print("DAI         : %.4f => %.4f" % (x_old[2], x[2]))
    print("Col ETH     : %.4f => %.4f" % (x_old[3], x[3]))
    print(
        "DAI Minted  : %.4f => %.4f" % ((x_old[3] * eth_price / dai_price / rho), (x[3] * eth_price / dai_price / rho)))
    print("====================================")


def printAssetsModified(x):
    print("========= Assets ============")
    print("USD         : %.2f" % x[0])
    print("ETH         : %.2f" % x[1])
    print("DAI Bought  : %.2f" % x[2])
    print("Col ETH     : %.2f" % x[3])
    print("DAI Borrowed: %.2f" % x[4])
    print("=============================")


def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


def log(string, filename, flag=False):
    if flag:
        f = open(filename, "a+")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f.write(current_time + " " + string + "\n")
        f.close()


def getAssetLogString(assets):
    return str(round(assets[0], 4)) + " $, " + str(round(assets[1], 4)) + " ETH, " + str(
        round(assets[2], 4)) + " DAI, " + str(round(assets[3], 4)) + " cETH"


def printArr(x):
    x = [round(i, 4) for i in x]
    print(x)


def getWorth(assets, eth_price, dai_price):
    print("$", assets[0] + assets[1] * eth_price + assets[2] * dai_price + assets[3] * eth_price)


class User:
    USD = 0
    ETH = 0
    DAI = 0
    cETH = 0
    rho = 0

    def __init__(self, assets, rho):
        self.USD = assets[0]
        self.ETH = assets[1]
        self.DAI = assets[2]
        self.cETH = assets[3]
        self.rho = rho

    def getAssets(self):
        return [self.USD, self.ETH, self.DAI, self.cETH]

    def setAssets(self, assets):
        self.USD = assets[0]
        self.ETH = assets[1]
        self.DAI = assets[2]
        self.cETH = assets[3]

    def getDebt(self, eth_price, dai_price):
        return self.cETH * eth_price / dai_price / self.rho
