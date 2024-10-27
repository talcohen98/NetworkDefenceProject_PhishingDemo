from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
from MessageGenarator import Data2Message

app = Flask(__name__)

# Introductory page route
@app.route('/', methods=['GET', 'POST'])
def intro():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('intro.html')

# Home route to collect user input
@app.route('/form', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect data from form
        name = request.form['name']
        about = request.form['about']
        education = request.form.get('education')
        interests = request.form.get('interests')
        post1 = request.form.get('post1')
        post2 = request.form.get('post2')
        post3 = request.form.get('post3')

        # Create JSON object
        user_data = {
            "name": name,
            "about": about,
            "education": education,
            "interests": interests,
            "posts": [post1, post2, post3]
        }

        # Generate the response message
        responseMessage = Data2Message(user_data)
        print(responseMessage)
        # Redirect to display message page
        return redirect(url_for('display_message', message=responseMessage))

    return render_template('index.html')

# Route to display the created message
@app.route('/display')
def display_message():
    message = request.args.get('message', '')
    current_time = datetime.now().strftime("%I:%M %p, %A")  # Format current time
    return render_template('display.html', message=message.strip(), current_time=current_time)

# Route for the page after the generated message
@app.route('/after-message')
def after_message():
    return render_template('after_message.html')

# Final page route
@app.route('/final')
def final_page():
    return render_template('final.html')

if __name__ == '__main__':
    app.run()
