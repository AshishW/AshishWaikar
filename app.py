from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/project_showcase')
def route_to_project_page():
    return render_template("projects.html")

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]
    try:
        with open("messsages.md", "a") as file:
            file.write(f"## New Submission\n")
            file.write(f"**Name:** {name}\n")
            file.write(f"**Email:** {email}\n")
            file.write(f"**Message:** {message}\n")
            file.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("\n---\n\n")
        load_dotenv()
        ntfy_topic = os.getenv("NTFY_TOPIC")
        ntfy_message = f"New message from {name} ({email}). 📩 \n check messages(md) file in portfolio"

        requests.post(f"https://ntfy.sh/{ntfy_topic}", data=ntfy_message.encode(encoding='utf-8'))
        return jsonify(success = True)
    except Exception as e:
        return jsonify(success=False, error=str(e));

if __name__ == '__main__':
    app.run(debug=True)