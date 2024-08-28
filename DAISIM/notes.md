## Notes 

(DAISIM Paper)[https://drops.dagstuhl.de/storage/01oasics/oasics-vol092-fab2021/OASIcs.FAB.2021.3/OASIcs.FAB.2021.3.pdf]

## D^{OV} : Order Value

- There is some demand based on every agent's portfolio
- cdp rate is directly put into the agent cost function
- rho is fixed in DAISIM -- but there is no reason why we couldn't vary this as an input

## D^{cdp} : Burn Mint Demand

- Updates to Dai Price ar actually done at the agent level
- They aggregate the dispairty between CDP need and Order value Demand D_ov - D_cdp
- So for example, if D_ov < 0 but D_cdp  > 0 this means an agent would like to reallocate out of DAI but also has to mint DAI this is going to result in a lot of extra supply. On the other hand, extra demand will spike price

- These values might balance. For instance, if D_ov=D_cdp then the amount minted matches the amount the agent wants to buy from the market and they contribute net 0 to price dynamics. Intuitively they mint new dai tokens and also `buy' them -- so they just effectively "hold" those tokesn
 ( not sure where D_cdp "goes" exactly though in terms of how the market is simulated)

 TODO: investigate this question ^^

 ## Arbitrage

 - We should also note that I think the belief factor is likely contributing to arbitrage
 - for example, if 

## Resources
- Bash setup:
https://rowannicholls.github.io/bash/intro/myscript.html
- cvxpy:
https://www.cvxpy.org/index.html
- Daisim
https://github.com/ANRGUSC/DAISIM/blob/main/input_generator.py