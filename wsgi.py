from backend.app import app

"""
A wrapper to easily run using gunicorn server - example to run at port 5000:

gunicorn --bind 127.0.0.1:5000 wsgi:app -t 1200 --config gunicorn_config.py &

NOTE ON IP ADDRESS USED

127.0.0.1 will only allow local conections - i.e it will *not* allow connections from your laptop if the app is running on a GCP instance
That is A GOOD THING because in general you should not open up the http port to the world which is the risk you run if you allow
non-local connections. If you need to run your app in a hosted instance continue to use 127.0.0.1 as the ip address and
put nginx in front of your app to use https connections.

"""

if __name__ == "__main__":
    app.run()
