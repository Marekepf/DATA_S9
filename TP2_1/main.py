from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def root():
    prefix_google = """
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-6JDE6HH266"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-6JDE6HH266');

        </script>
        """
    return prefix_google + "Hello from Space! 🚀"

@app.route("/logger")
def logger():
    # Print a log message to the Python console
    print("Logging message in Python console.")

    # Get the user agent from the request headers
    user_agent = request.headers.get('User-Agent')
    
    # JavaScript code to log to the browser's console and display in a textbox
    log_to_browser = """
        <script>
        console.log('Logging message on the browser. User Agent:', '%s');
        document.getElementById('logTextbox').value = 'Logging message on the browser. User Agent: %s';
        </script>
        """ % (user_agent, user_agent)
    
    # HTML response with a textbox
    response = """
        <p>Logging message on the browser. User Agent: {user_agent}</p>
        <textarea id="logTextbox" rows="5" cols="50" readonly></textarea>
        """.format(user_agent=user_agent)
    
    return response + log_to_browser

if __name__ == "__main__":
    app.run()
