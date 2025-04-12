### Introduction
#### Trading Strategy Playground
A web-based platform for systematic evaluation of trading strategies.

Users can define parameter ranges to perform combinatorial testing of strategy variations on 
historical stock time series data. The platform automates backtesting across all parameter 
combinations and surfaces performance metrics for comparative analysis.

### Tech Stack
1. PostgresSQL database (Running in Docker on local/cloud server)
2. Python backend codebase (FastAPI app, runs with Uvicorn, running in Docker on local/cloud server)
3. Redis (Caching/temp data for Python backend, running in Docker on local/cloud server)
4. React frontend (Vite + TypeScript, served as static files by Nginx on local/cloud server)
5. Nginx for SSL and routing (Runs directly on the local/cloud server)


### Developer Setup Instructions
#### Backend

1.	Create a local keys.list file with environment variables, and configure your Python run settings to use it.
2.	Install dependencies from requirements.txt.
3.	Clone the Git repository and create a development branch based on main.
4.	Push changes to the development branch and open a merge request to merge into main upon review.


#### Frontend

1. Save index.html to the local/cloud server


#### Docker setup instructions

Restart:
```
docker-compose up -d
```

If you make changes to images/compose file and want to rebuild and start all:
```
docker-compose down -v
docker-compose up --build -d
```


Transfer compose to the server
```
scp docker-compose.yml dimitri@192.168.1.67:~/kafka/docker-compose.yml
scp -P 2634 docker-compose.yml dimitri@75.155.166.60:~/kafka/docker-compose.yml
```

Start Kafka environment
```
docker compose up --build -d
```

Transfer the project to the server
```
rsync -av --exclude='.venv' TradingStrategy/ dimitri@192.168.1.67:~/services/TradingStrategy/
rsync -av --exclude='.venv' -e 'ssh -p 2634' TradingStrategy/ dimitri@75.155.166.60:~/kafka/TradingStrategy/
```

Copy service file to systemd dir
```
cd services/TradingStrategy

sudo cp kafka-stream.service /etc/systemd/system/
```

Start the systemd service
```
sudo systemctl daemon-reload
sudo systemctl enable kafka-stream.service
sudo systemctl restart kafka-stream.service
systemctl status kafka-stream.service
journalctl -u kafka-stream.service -f

sudo systemctl disable kafka-stream.service 
sudo systemctl stop kafka-stream.service
```

Save logs
```
journalctl -u kafka-stream.service \
  --since "2025-04-12 03:43:57.547" \
  --output=cat \
  --no-pager > .monitoring/kafka-stream.log
  
scp dimitri@192.168.1.67:/home/dimitri/services/TradingStrategy/.monitoring/kafka-stream.log .
```

Start watcher service to email on error or warning, save files (in .monitoring/) to new location for systemctl
``` 
sudo cp .monitoring/kafka-log-watcher.service /etc/systemd/system/
nano /etc/systemd/system/kafka-log-watcher.service

nano ~/services/TradingStrategy/.monitoring/log_alert.sh

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable kafka-log-watcher.service
sudo systemctl start kafka-log-watcher.service

journalctl -u kafka-log-watcher.service -f
```