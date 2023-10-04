from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/logger")
def logger():
    # Print a log message to the Python console
    print("Logging message in Python console.")

    # Get the user agent from the request headers
    user_agent = request.headers.get('User-Agent')
    
    # Print a log message to the browser
    return f"<p>Logging message on the browser. User Agent: {user_agent}</p>"

if __name__ == "__main__":
    app.run()
