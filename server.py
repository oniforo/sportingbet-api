from flask import Flask, request
from main import return_content

app = Flask(__name__)

@app.route("/")
def home():
    subdir = request.args.get("subdir")
    return return_content(subdir)

if __name__ == "__main__":
    app.run(debug=True)