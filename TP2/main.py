from flask import Flask, request, render_template, jsonify
import requests  

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

@app.route("/logger", methods=['GET', 'POST'])
def logger():
    print("Logging message in Python console...")

    text = None
    cookies = None

    if request.method == 'POST':
        text = request.form.get('textarea')
        print(text)

    # Make a request to Google Analytics to get the cookies
    req_cookies = requests.get("https://analytics.google.com/analytics/web/?utm_source=marketingplatform.google.com&utm_medium=et&utm_campaign=marketingplatform.google.com%2Fabout%2Fanalytics%2F#/p407503755/reports/intelligenthome?params=_u..nav%3Dmaui")
    
    if req_cookies.status_code == 200:
        cookies = req_cookies.cookies._cookies

    return render_template('logger.html', text=text, cookies=cookies)


@app.route('/perform-google-request', methods=['GET'])
def perform_google_request():

    req = requests.get("https://analytics.google.com/analytics/web/#/p407458242/reports/intelligenthome?params=_u..nav%3Dmaui")

    return req.text

if __name__ == "__main__":
    app.run()