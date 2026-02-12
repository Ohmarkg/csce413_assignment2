# Assignment 2 
This my implementation of the port scanner ( I only completed part I)

## How to run
Navigate into the project directory `cd` into `port_scanner` and start the containers using  
```bash
docker compose up
```
Copy the main.py into the container
```bash
docker cp main.py 2_network_webapp:/app/main.py
```
Once start then move into the container environment  

```bash
docker exec -it 2_network_webapp /bin/bash
```

Now you are able to scan IPs of your choice using the required arguments `-target` and `-ports`. `-target` takes the target ip e.g `172.20.0.20` and `-ports` takes a start and end points to define the range of ports to scan.

### Example usage
```python
python3 main.py -target 172.20.0.20 -ports 1 30000
```
The program will show any ports that were opened and related banner info if it is available

## Additional features
I just added multi threaded search using threading 