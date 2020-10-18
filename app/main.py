from flask import Flask, render_template, request


# App and model initializer
app = Flask(__name__)

title = 'Send us message'

# GET method
@app.route('/')
def home():
    return render_template('home.html', title=title)


# POST method
@app.route('/', methods=['POST'])
def result():
    data = request.form['message']
    print(data)

    return render_template('home.html', title=title, answer=f'Your message : {data}')