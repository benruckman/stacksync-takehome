## Safe Python Script Execution service
This took me ~2.5 hours.

Run with Docker:
docker build -t flask-nsjail-app .
docker run -p 8080:8080 flask-nsjail-app

Run in terminal (without nsjail):
python app.py

Run tests in terminal:
python test_app.py

Deployed:
https://stacksync-takehome-139953530506.us-west1.run.app
Post @ https://stacksync-takehome-139953530506.us-west1.run.app/execute with a valid body!

Notes:
It outputs a ton of text from stdout from the imports of builtins, pandas, and numpy. I didn't have time to fix this. 
