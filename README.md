# Strategic Procurement Optimization System (SPOS)

This system utilizes an application of game theory called Bayesian Fuzzy Games to optimize supplier negotiations when purchasing. This game theory model implements a Bayesian Mixed strategy game that considers external factors on negotiations. Currently external factors are not considered in this version, and the mixed strategy game theory determines the counteroffer price. The bayesian network will be updated to count external factors in the negotiation. 

This system integrates with email, and can send emails. It currently cannot read emails as this will be added at a later date. <br>

# Dash App (Frontend)
The frontend data visualization dashboard
The web application: <br>
<img src="./images/Dashboard_Final.png" alt="dashboard"/> <br>

Here on the home screen you can see the external factors that influence negotiations through the Bayesian Networks on our two plots on the top. Note that the weights will be added in a future version once the bayesian network nodes are complete. These network graphs will show the values of each external factors as they are added to our system. Below that is a table that tracks the status of each game, and gives information on the games. <br>

On the left hand side of the screen there are three forms that allow you to update game, launch a new negotiation game, and add sellers to the database. 
- Add seller allows the user to add a seller to the database. 
- Update game allows the user to enter the counteroffer price from a seller for a specific game, and it will tell the user the recommended counteroffer price to send the seller. The game ID is located in the subject line of all emails from the system. 
- The launch new negotiation game form allows the user to enter a requirement, and when they hit request quotes the system will email all sellers in the database requesting quotes for the new need. 

# How to Run
Ensure docker is installed on your computer. There will be two docker containers. One for the database, and one for the dash webpage. The application runs on 8001. The database is on port 5432. To run locally go to the data_service.py folder and change the url_engine in the dataservice__init__ from 172.17.0.2 to localhost. Then you simply run the app.py file if you download the environment requirements. To run on docker (preferred) enter the command line and enter:

### How to setup the docker database
1. docker run --name spos_postgres -p 5432:5432 -e POSTGRES_PASSWORD=spos123 -d postgres
2. docker exec -it spos_postgres bash
3. su - postgres
4. psql -U postgres
5. CREATE DATABASE default_company;
6. \c default_company
7. Run rest of SQL from database/create_spos_database.sql file


### How to setup the docker application
Navigate to the app folder in the command line. Run:
1. docker build -t spos_app .
2. docker run -p 8001:8001 spos_app

Now go to a web browser and go to http://localhost:8001/


### (optional) To get pgAdmin4 to run
If you want to use pgAdmin4 to manage and view the database enter the following commands:
1. docker run -p 5050:80 -e "PGADMIN_DEFAULT_EMAIL=(your email)@gmail.com" -e "PGADMIN_DEFAULT_PASSWORD=admin" -d dpage/pgadmin4
2. Connect the containers with:
3. name: spos_postgres
host: host.docker.internal
database: postgres
user: postgres
password: spos123



# Backend
##  Game Logic 
Contains the bayesian fuzzy game logic, and contains the following classes:
### Negotiation Game <br>
This is a two player mixed strategy negotiation game. This is a game under incomplete information since we do not know the opponents reservation price or deadline. To make up for this lack of information we can predict their strategy using our game theory model. In this class we calculate the sellers utility from the following payoff matrix: <br>
<img src="./images/Payoff_Matrix.png" alt="dashboard" width="400"/> <br>
Source: See [2] Below


All games start with mixed strategy probabilities $p=0.5$ and $q=0.5$. In this class $\lambda$ is the utility and  represents the strategy, and is used in the calculate. Please see the pdf file titles SPOS mathematics for an in depth explanation of the game theory mathematics used in this web application. 


When testing please note that the non-external factor game matrix returns a strategy that is very conservative at the start of negotiations. Please create a negotiation game that has a closer due date for a more significant shift in the counteroffer price. This is to show how the strategy values impact the game:

<img src="./images/Strategy_Trend_Analysis.png" alt="network" width="400"/> <br>
Source: See [2] Below <br>

Once we determine the sellers strategy $\lambda_s$ with our mixed strategy bayesian game, we use this strategy to send our counteroffer price: <br>
$OP_t = IP + -1^{\alpha} (\frac{t}{\tau})^{\lambda_s} |RP_b - IP|$ <br>
Where $\lambda_s$ is the seller strategy, $\alpha$ is 1 for buyer and 0 for seller, $t$ is current negotiation time in days, and $\tau$ is total days of the negotiation until the buyers deadline

### Bayesian Network: <br>
Still being built due to network complexity. Contains the Bayesian Network logic following this DAG: <br>
<img src="./images/Networks.png" alt="network" width="600"/> <br>
Source: See [2] Below <br>

This network is used to calculate the influence of external factors on negotiation. This class returns a probability with 1 being external factors have no influence on the negotiators negotiation power, and 0.1 meaning external factors have a large influence on the negotiators negotiation power. 


## Data Service
Controls access to the database and uses SQLAlchemy ORM to interact with the database. The models.py contains the object relational mapping from the database to python objects. The data service python file has all functions for creating, reading, updating, or deleting (CRUD) in the data_service.py file. This ensures the frontend does not interact directly with the database, and that there is a data service layer of the business logic.  

##  Email Service
Controls the sending and receiving of emails. Would be switched with an email service in productions, but for now uses python and a gmail account, but could be substituted for any email service. 

# Database
## Daily Data Collection
The daily database updating DAG has not yet been implemented, and will be implemented to allow for daily updating of the influence of external factors on a negotiation. 

# References
[1] Gwak, J. and Sim, K. M. (2011). “Bayesian learning based negotiation
agents for supporting negotiation with incomplete information.” The
International MultiConference of Engineerings and Computer
Scientist, IMECS, HongKong, IEEE, pp. 163-168.


[2] Leu, S.-S., Hong Son, P. V., & Hong Nhung, P. T. (2014). Optimize negotiation price in
construction procurement using Bayesian Fuzzy Game Model. KSCE Journal of Civil
Engineering, 19(6), 1566–1572. https://doi.org/10.1007/s12205-014-0522-2
 