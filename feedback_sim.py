from pid import PID
import daisim
from daisim.sim import *
import matplotlib.pyplot as plt
from daisim.util import set_defaults, SimState
import numpy as np
from dataclasses import dataclass, fields
import seaborn as sns

init_price=1.0
SAMPLE=5
DAYS=20
rai=PID(initial_market_price=1.0, KP=.1) # TODO: Tune PID with Ziegler Method (Rudra?)
params=set_defaults(SAMPLE,DAYS) #NOTE read  CDPRates, TXFs from config, sample = num agents ( as many as necessary to decently capture info )

#NOTE: a particular hard-coded distribution where more risk-tolerant investors exist and risk-averse
# tolerant=[max((.005)-(.002)*i,.0001) for i in range(1,4)] #NOTE: must not be non-negative
# averse=[(.005)+(.002)*i for i in range(1,4)]
# averse.reverse()
params.lambdas=abs(np.random.normal(.005,.01,size=SAMPLE))

# NOTE: Add Risk Bias Factor
bias = 0.005
params.lambdas = [lam+bias for lam in params.lambdas]

#NOTE: uncomment to see starter settings
# print("check starting values\n\n")
# for field in fields(params):
#         value = getattr(params, field.name)
#         print(f'{field.name}: {value}')

#NOTE: uncomment to see risk_distribution
#plt.plot(params.risk_lamdas)
#plt.title("Agent Risk Settings")
#plt.pause(.5)

ASSETS=get_assets(params.num_investors)
RISK = params.lambdas

# NOTE: Refactor the sim.py file into a "closed-loop" system with PID.py 
def run_step( params : SimState , logdir = "sim-logs", logger=False, runs=1, display=False, fig_suffix="", figdir="", 
    controller=PID(initial_market_price=1.0, KP=.1)
):
    assets_runs,risk_params=generate_assets_and_risk(params.num_investors,"normal",runs)
    asset_history=[]
    dai_price_history=[1.0]
    market_dai_history=[]
    cdp_rate_history=[params.cdp_rate]
    rai_price_history=[]

    cur_assets=assets_runs # size should be (1, n, 4)  --> 1 run, n users, 4 assets 
    cur_dai_price = 1

    for day in range(0, DAYS):
        #--------------- MARKET SIM BLOCK -----------------------------------
        s = Simulator(
            belief_factor=params.belief_factor, rho=params.rho, cdpRate=params.cdp_rate, 
            txf=params.tx_fee, run_index=0, eth_price=params.eth_price_per_day[day],
            sample_size=params.num_investors, 
            initial_distribution=cur_assets, risk_params=params.lambdas,
            logdir=logdir, logger=False
        )
        s.dai_price = cur_dai_price
        dai_price, market_dai = s.run_simulation()
        dai_price=dai_price+np.random.normal(loc=0.0,scale=.005)
        print("Check Market Change: ", market_dai)
    
        # Definition of USER
        #  users = [User(self.initial_distribution[i], self.rho) for i in range(len(self.initial_distribution))]

        # get asset state
        cur_assets = s.final_distribution
        cur_dai_price = dai_price
        # NOTE : also this is about 3 to 5 seconds per cycle -- 50 steps might be about 4 minutes , 100 ~ 8 minutes
        # NOTE : coupled with our solver + overhead. 100 step simulation who knows? 16-20 minutes on my laptop?
       
        # --------------- RESPONSE BLOCK -------------------------
        # TODO: Ensure Information Passing is Correct
        # TODO: probably check on the convert price to rate function too
        controller.compute_error(dai_price)
        controller.compute_new_redemption_price() 
        p_redeem=controller.read_redemption_price()
        params.cdp_rate = convert_price_to_rate(p_redeem, dai_price)
        
        if day % 5 == 0:
            print("day :", day)

        if (display):
            print("Step: {}, Check Updates:")
            print("------------------------")
            print("Net burn/mint : ", np.sum(np.array(s.final_distribution)[:,3])) #TODO: this is wrong, the 3rd asset is cETH -- correct formula takes diff and price to convert
            print("Dai Price: ", dai_price)
            print("New Redemption Price: ", p_redeem)
            print("New CDP Rate: ", params.cdp_rate)
            print("\n Check Rai Controller State")
            print("Rai redeem price:" , controller.pr)
            print("Rai Error", controller.errors)
            print(controller.kp)
            print(controller.target)
            print(controller.mode)
            print("-----------------------\n")

        # NOTE Save Data   -- store asset_history and dump into a separate pickle file
        asset_history.append(cur_assets[:])
        cdp_rate_history.append(params.cdp_rate)
        dai_price_history.append(dai_price)
        market_dai_history.append(market_dai)
        rai_price_history.append(controller.pr)
    
    from collections import Counter
    count_d=Counter(params.lambdas)
    import pandas as pd
    df=pd.DataFrame(params.lambdas,columns=["lambdas"])
    fig,ax=plt.subplots(2,2)
    # ax[0,0].stem(list(count_d.keys()), list(count_d.values()))
    ax[0,0].set_title("Agent Risk Profile")
    sns.kdeplot(df, x="lambdas", common_norm=False, ax=ax[0,0])
    ax[0,1].plot(cdp_rate_history)
    ax[0,1].set_title("CDP Redemption Rates")
    ax[1,0].plot(dai_price_history, label="Market Price ()")
    ax[1,0].plot(rai_price_history, label="Redemption Price")
    ax[1,0].set_title("Prices")
    ax[1,1].plot(market_dai_history, label="Token Supply")
    ax[1,1].set_title("Token Supply")
    ax2 = ax[1,1].twinx()
    ax[1,1].set_ylabel('Token Supply')
    ax2.plot(params.eth_price_per_day,color="firebrick",label="Eth Price Path")
    ax2.set_ylabel('Eth Prices')
    ax[1,0].legend()
    fig.tight_layout()
    plt.savefig(f"{figdir}run_summary{fig_suffix}.png")

    # NOTE: no longer needed
    # plt.figure()
    # plt.plot(params.eth_price_per_day)
    # plt.title("Eth Price Path")
    # plt.savefig(f"{figdir}sim_eth_path{fig_suffix}.png")
    # plt.show()

def convert_price_to_rate(p_redeem, p_dai=1):
    return -(1 - (p_redeem/p_dai))

def generate_assets_and_risk(sample_size, test_type, runs):
    # if ASSETS was populated from config, return. Else generate a random ASSETS
    if ASSETS is not None:
        return ASSETS, RISK

    assets_runs = [get_assets(sample_size, test_type) for k in range(runs)]
    risk_params = get_risk_params(sample_size)

    return assets_runs, risk_params

def run_pid_testing():
    for KP in [0.1,0.25,0.5,0.75,1.0]:
        rai=PID(initial_market_price=1.0, KP=KP) # TODO: Tune PID with Ziegler Method (Rudra?)
        params=set_defaults(SAMPLE,DAYS) #NOTE read  CDPRates, TXFs from config, sample = num agents ( as many as necessary to decently capture info )
        run_step(params,fig_suffix=f"_KP_{KP}",figdir="figs/")

def make_test_pids():
    rais=[]
    for KP in [0.1,0.25,0.5,0.75,1.0]:
        rais.append(PID(initial_market_price=1.0, KP=KP)) # TODO: Tune PID with Ziegler Method (Rudra?)
    return rais


if __name__ == "__main__":
    
    rais=make_test_pids() #  run_pid_testing()
    for rai in rais:
        run_step(params,controller=rai,fig_suffix=f"_KP_{rai.kp}",figdir="figs/")



