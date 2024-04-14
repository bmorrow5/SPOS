# Strategic Procurement Optimization System (SPOS)

This system utilizes an application of game theory called Bayesian Fuzzy Games to optimize supplier negotiations when purchasing. This system works via email. It will calculate the optimal counter offer price, and then email the counter offer to the supplier. 

## How to Run
Pending (build in progress)
There will be two docker containers. One for the database, and one for the API. The frontend is seperated as well. To run on docker enter the command line and enter:

### How to setup the database
1. docker run --name spos_postgres -p 5432:5432 -e POSTGRES_PASSWORD=spos123 -d postgres
2. docker exec -it spos_postgres bash
3. su - postgres
4. psql
5. CREATE DATABASE default_company;
6. \c default_company
7. Run rest of SQL

### To get pgAdmin4 to run
1. docker run -p 5050:80 -e "PGADMIN_DEFAULT_EMAIL=brandonmorrow09@gmail.com" -e "PGADMIN_DEFAULT_PASSWORD=admin" -d dpage/pgadmin4
2. Connect the containers with:
3. name: spos_postgres
host: host.docker.internal
database: postgres
user: postgres
password: spos123

### Logging in
Username: spos6045@gmail.com
password: 1234abcd!#



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

## Data Service
Controls access to the database and uses SQLAlchemy ORM to interact with the database. Has all functions for creating, reading, updating, or deleting (CRUD) in the data_service.py file. The models.py contains the object relational mapping from the database to pythong objects. 

##  Email Service
Controls the sending and receiving of emails. Would be switched with an email service in productions, but for now uses python and a gmail account.
https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python

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
 