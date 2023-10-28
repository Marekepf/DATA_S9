from flask import Flask, request, render_template, jsonify
import requests  
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO  
import base64  
from collections import Counter
import logging
import time
app = Flask(__name__)

# Function to generate Matplotlib plot
def generate_plot():
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=['NASA', 'SpaceX'], timeframe='2018-01-01 2019-12-31')
    data = pytrends.interest_over_time()

    # Generate a line plot to see the trends
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data['NASA'], label='NASA')
    plt.plot(data.index, data['SpaceX'], label='SpaceX')
    plt.xlabel('Date')
    plt.ylabel('Search Interest')
    plt.title('Google Trends Data')
    plt.legend()
    plt.savefig('static/plot.png')  # Save the plot as a static file

# Run the generate_plot function before the first request
generate_plot()


def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' took {execution_time:.2f} seconds to execute.")
        return result
    return wrapper

def download_shakespeare_text():
    url = "https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open("shakespeare.txt", "w", encoding="utf-8") as file:
            file.write(response.text)

def count_words_dict(text):
    word_count = {}
    words = text.split()
    for word in words:
        word = word.lower().strip(".,!?;:()[]{}")
        if word:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    return word_count

def count_words_counter(text):
    words = text.split()
    words = [word.lower().strip(".,!?;:()[]{}") for word in words if word]
    word_count = Counter(words)
    return word_count

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
        <button onclick="window.location.href='/Oauth'">Oauth Page</button>
        <button onclick="window.location.href='/get_search_interest'">Search Interest Page</button>
        <button onclick="window.location.href='/word_count_experiment'">Execution Time Page</button>
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


@app.route('/get_search_interest', methods=['GET'])
def get_search_interest():
    # Read the saved plot and encode it as base64
    with open('static/plot.png', 'rb') as plot_file:
        plot_data = base64.b64encode(plot_file.read()).decode()

    return render_template('google_trends.html', plot_data=plot_data)

@app.route('/word_count_results', methods=['GET'])
def word_count_results():
    # Download Shakespeare's text
    download_shakespeare_text()

    # Read the text from the file
    with open('shakespeare.txt', 'r', encoding='utf-8') as file:
        shakespeare_text = file.read()

    def count_words_dict():
        return count_words_with_dict(shakespeare_text)

    word_count_dict = count_words_dict()

    def count_words_counter():
        return count_words_with_counter(shakespeare_text)

    word_count_counter = count_words_counter()

    return render_template('word_count_results.html', word_count_dict=word_count_dict, word_count_counter=word_count_counter)

@app.route('/word_count_experiment', methods=['GET'])
def word_count_experiment():
    # Add the following code to set the Agg backend explicitly
    import matplotlib
    matplotlib.use('Agg')

    # Download Shakespeare's text
    download_shakespeare_text()
    shakespeare_text = open('shakespeare.txt', 'r', encoding='utf-8').read()

    # Create lists to store execution times
    execution_times_dict = []
    execution_times_counter = []

    # Repeat the experiment 100 times
    for _ in range(100):
        # Measure execution time for counting words with a dictionary
        start_time = time.time()
        count_words_dict(shakespeare_text)
        end_time = time.time()
        execution_times_dict.append(end_time - start_time)

        # Measure execution time for counting words with Counter
        start_time = time.time()
        count_words_counter(shakespeare_text)
        end_time = time.time()
        execution_times_counter.append(end_time - start_time)

    # Plot the two distributions of execution times
    plt.figure(figsize=(8, 4))
    plt.hist(execution_times_dict, bins=20, alpha=0.5, label='Dictionary')
    plt.hist(execution_times_counter, bins=20, alpha=0.5, label='Counter')
    plt.xlabel('Execution Time (seconds)')
    plt.ylabel('Frequency')
    plt.title('Execution Time Distributions')
    plt.legend()

    # Save the plot to a buffer and encode it for display in the HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()

    # Close the plot
    plt.close()

    return render_template('word_count_experiment.html', plot_data=plot_data)

if __name__ == "__main__":
    app.run()