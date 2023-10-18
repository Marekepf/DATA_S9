from flask import Flask, request, render_template, jsonify
import requests  
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

app = Flask(__name__)

@app.route("/")
def root():
    title = "<h1>TP1 Marek Boudeville</h1>"
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

    buttons_html = """
        <button onclick="window.location.href='/logger'">Logger Page</button>
    """

    return title + prefix_google + buttons_html  +  "Hello from Space! 🚀"


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


@app.route('/Oauth', methods=['GET'])
def fetch_google_analytics_data():

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'datasourcetp2-xxxxxxxxx.json'
    PROPERTY_ID = 'xxxxxxx'
    starting_date = "8daysAgo"
    ending_date = "yesterday"

    client = BetaAnalyticsDataClient()
    
    def get_visitor_count(client, property_id):
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": starting_date, "end_date": ending_date}],
            metrics=[{"name": "activeUsers"}]
        )

        response = client.run_report(request)
        return response
    response = get_visitor_count(client, PROPERTY_ID)

    if response and response.row_count > 0:
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = "N/A"  

    return f'Number of visitors : {metric_value}'

if __name__ == "__main__":
    app.run()