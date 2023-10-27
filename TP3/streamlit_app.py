import streamlit as st
import requests

st.title("Google Analytics Viewer")

# User input for the Google Analytics URL
google_analytics_url = st.text_input("Enter Google Analytics URL:", "https://analytics.google.com/analytics/web/?utm_source=marketingplatform.google.com&utm_medium=et&utm_campaign=marketingplatform.google.com%2Fabout%2Fanalytics%2F#/p407503755/reports/intelligenthome?params=_u..nav%3Dmaui")

if google_analytics_url:
    # Construct the URL for the Flask route
    flask_url = f"http://localhost:5000/perform-google-request/{google_analytics_url}"

    # Make a request to the Flask application to fetch the Google Analytics content
    req = requests.get(flask_url)

    # Display the status code and content
    st.text(f"Status Code: {req.status_code}")
    st.markdown(req.text)
