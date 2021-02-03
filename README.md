# Demo event handler

This script is intended to run in the customer cloud and forward webhook
events from one of their internal services to your company cloud.
The events can be anonymized, aggregated, filtered etc.

It's based on tornado and handles the events asynchronously.
1) `/events` endpoint that receives events from internal webhook
2) Process the events
3) Upload events to company cloud

# Installation
```
python3.8
pip install -r requirements.txt
```

# Tests
```
python3.8
pip install -r requirements-dev.txt
py.test test
```

# Start
```
# This will start the demo service and the API will start listening on localhost:3000
python run.py

# Afterwards you can upload some example events
python run_example_posts.py
```

# Docker
```
docker build . -t demo
docker run -p 3000:3000 -t demo python run.py
docker run --net container:<containerid> -t demo run_example_posts.py
```