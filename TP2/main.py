from flask import Flask, request, render_template

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
    if request.method == 'POST':
        text = request.form.get('textarea')
        print(text)

    return render_template('logger.html', text=text)

if __name__ == "__main__":
    app.run()
