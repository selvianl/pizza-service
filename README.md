## Installation

* Go your home directory by typing `cd ~`.

* Create virtual enviroment by running `virtualenv --python=python3 pizza`.

* Clone the project by typing `git clone https://github.com/selvianl/pizza-service.git`.

* Go in the project directory: `cd pizza-service`.

* Activate the virtual environment by running `source ~/pizza/bin/activate `.

* If docker is not installed, install by getting help from:<br>
  https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community-1
  
 * Create container for API by typing `sudo docker build -t pizza-service .`.

* Pull container of postgres by typing ` sudo docker pull postgres:10.10 `.

* Start docker swarm by typing `sudo docker swarm init`.

* Create stack service by typing `sudo docker stack deploy -c docker-compose.yml demo`.

* Track service status by typing `sudo docker service ls`.

* Halt the service by typing `sudo docker service rm demo_pizza-sercive demo_postgres`.

* Check for log of service by typing `sudo docker servi log <service_name>`.

## API Endpoints

* **Create a customer:** http://127.0.0.1:8000/api/create_customer/

* **Create a pizza:** http://127.0.0.1:8000/api/create_pizza/

* **Create an order:** http://127.0.0.1:8000/api/create_order/ <br>
  When adding an order for a new customer you have to first add a customer, then add a pizza and then add an order selecting those objects for its fields. 
  

* **Track an Order Status:** http://127.0.0.1:8000/api/track_status_order/ (order id)/

* **Change Status of Order:** http://127.0.0.1:8000/api/update_status_order/ (order id)/

* **Edit an Order Details:** http://127.0.0.1:8000/api/update_order/ (order id)/

* **Remove an Order:** http://127.0.0.1:8000/api/remove_order/ (order id)/

* **Showing all orders:** http://127.0.0.1:8000/api/list_order/ 

* **Details of a spesific order:** http://127.0.0.1:8000/api/detail_order/ ?order_id=<VALUE>/
                                                
* **Filtering Orders:** http://127.0.0.1:8000/api/search_order/ ?customer_id=<VALUE>&delivered=<VALUE>/

## Test

To run the tests run the command `python manage.py test api` .
