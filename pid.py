## Basic PID ---------------------------------------------------
# https://www.youtube.com/watch?v=ZMI_kpNUgJM
# Ziegler Nichols Method
# I think the same method is recommended her by THOR Labs : https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=9013#:~:text=To%20tune%20your%20PID%20controller,to%20roughly%20half%20this%20value.

#------------------------------------------------------------------
# Might be Able to Use GEKKO for simple real-time tuning idea ??
# also nice will take away a lot of the coding effort and the model
# can be more focused on fitting observations
# https://gekko.readthedocs.io/en/latest/imode.html
# https://www.youtube.com/watch?v=0LiNb_MEXmQ

import numpy as np

class PID(object):

    def __init__(self,
            KP=1.0,
            KI=0.0,
            KD=0.0,
            initial_market_price=1.0,
            initial_redemption_price=1.0,
            target=1.0,
            mode="floating",
        ):
        TS=.001
        self.kp=KP
        self.ki=KI
        self.kd=KD
        self.pm=initial_market_price
        self.pr=initial_redemption_price
        self.target=target
        self.oracle=PriceOracle(initial_market_price) # potentially set forecaster vars here
        self.error=initial_market_price - self.target
        self.integral_error=0  #(sample time for continuos time) * TS
        self.derivative_error=0
        self.mode=mode
        self.errors=[]

    def read_redemption_price(self):
        return self.pr

    def read_error(self):
        return self.error
    
    def read_rate(self):
        return self.rate

    def compute_error(self,observed_price):
        if self.mode=="floating":
            # self.target=self.oracle.compute_estimate(observed_price)
            self.target=observed_price

        temp=self.target-self.pr
        self.integral_error+=temp
        self.derivative_error = temp-self.error #(sample time for continuos time) * TS
        self.error=temp
        # self.errors.append(self.error)
    
    def compute_new_redemption_price(self):
        self.rate = self.kp*self.error + self.ki*self.integral_error + self.kd*self.derivative_error
        self.pr += self.rate

    def set_mode(self,mode):
        assert (mode in ["constant", "floating"])
        self.mode=mode
         

import numpy as np

class PriceOracle():

    def __init__(self,init_price,n=10,gamma=0.8):
        self.history=np.random.normal(init_price,scale=.005,size=10)
        self.history[-1]=init_price
        self.weights=self.normalize(np.array([gamma**(n-i-1) for i in range(n)]))
        self.currprice=init_price#most recent observation
    
    def update(self,obs):
        self.history[0:-2]=self.history[1:-1]
        self.history[-1]=obs
        self.currprice=np.dot(self.history,self.weights)
        return 
    
    def read_price(self):
        print(self.history)
        # print(np.sum(self.weights))
        return self.currprice
    
    def normalize(self,x):
        return x/(np.sum(x))


oracle=PriceOracle(1.05)
init=oracle.read_price()
curr=init
rai=PID(KP=1.5,initial_market_price=init)
redeems=[]
errors=[]
markets=[]


if __name__ == "__main__":
    # print("Redemptions ", redeems)
    # print("Errors ", errors)
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(2,2)
    KP=.05 # arbitrage rate
    for(n,K) in enumerate([0.1, 0.5, 1, 1.5]):
        i,j = n%2, n//2
        init=1.05
        da=0
        curr=init
        last=curr
        rai=PID(KP=K,initial_market_price=init)
        redeems=[1.0]
        errors=[]
        markets=[]
        for __ in range(200):
            # prices
            # Unresponsive market:

            curr=last+np.random.normal(scale=.05)
            curr= curr+KP*(init-curr) #+np.random.normal(scale=.01)
            
            # np.random.normal(loc=da,scale=.001)
            
            # Oracle Test
            # new=(init-curr) + np.random.normal(scale=.01) + init
            # print("Market Obs: " , new)
            # oracle.update(new)
            # curr=oracle.read_price()
            # print("Oracle Weighted: ", curr)

            # PID Test
            rai.compute_error(curr)
            rai.compute_new_redemption_price()
            pr=rai.read_redemption_price()
            err=rai.read_error()
            da=rai.read_rate()

            errors.append(err)
            markets.append(curr)
            redeems.append(pr)

            ax[i,j].plot(markets,label="market_price")
            ax[i,j].plot(redeems,label="rai_price", alpha=.8, linestyle="--")
            # ax[i,j].plot(errors, label="input error")
            ax[i,j].legend()
            ax[i,j].set_ylim([.5,1.5])
            ax[i,j].set_title(f"RAI Kp Value: {K}",)
            fig.tight_layout()
            fig.suptitle("Redemption v. Market Price Comparison \n (Without Feedback)")

        plt.show()






