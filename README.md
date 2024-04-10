# Strategic Procurement Optimization System (SPOS)

This system utilizes an application of game theory called Bayesian Fuzzy Games to optimize supplier negotiations when purchasing. This system works via email. It will calculate the optimal counter offer price, and then email the counter offer to the supplier. 

## How to Run
Pending (build in progress)


##  Game Logic 
Contains the bayesian fuzzy game logic, and contains the following classes:
### Negotiation Game <br>
This is a two player zero-sum mixed strategy game. If we can estimate the opponents (suppliers) reservation price (lowest price they will accept) and deadline (how long before they need to make the deal) exactly, then our buyer agent can find an optimal strategy. We only need to correctly estimate one of these two to be able to find the other.  


### Bayesian Network: <br>
Contains the Bayesian Network logic following this DAG: <br>
<img src="Networks.png" alt="network" width="600"/> <br>
Source: See [2] Below


## Daily Data Collection
Collects data every day, and updates values in the database. 

## Data Access
Allows access to the database, and is how the game logic and flask app can access data from the database. 

##  Email Service
Contains bayesian fuzzy games and business logic. 

## Flask App 
Handles API endpoints. 

## Dash App
The frontend data visualization dashboard

## References
[1] Gwak, J. and Sim, K. M. (2011). “Bayesian learning based negotiation
agents for supporting negotiation with incomplete information.” The
International MultiConference of Engineerings and Computer
Scientist, IMECS, HongKong, IEEE, pp. 163-168.


[2] Leu, S.-S., Hong Son, P. V., & Hong Nhung, P. T. (2014). Optimize negotiation price in
construction procurement using Bayesian Fuzzy Game Model. KSCE Journal of Civil
Engineering, 19(6), 1566–1572. https://doi.org/10.1007/s12205-014-0522-2
 