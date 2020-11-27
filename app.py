from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instructions = instructions)

@app.route('/questions/<int:id>')
def questions(id):
    num_questions = len(satisfaction_survey.questions)
    if id is None:
        return redirect('/')
    elif len(responses) == num_questions:
        return redirect('/thank')
    elif id >= num_questions or id != len(responses):
        flash('Invalid question ID, please finish the current answer first', 'ID Error')
        return redirect(f'/questions/{len(responses)}')
    return render_template('questions.html', question = satisfaction_survey.questions[id], id = id)

@app.route('/answer', methods=["POST"])
def handle_answer():
    choice = request.form.get('answer')
    text = request.form.get('text','')
    if choice == None:
        flash('Please enter your choice', 'Choice Missing')
        return redirect(f'/questions/{len(responses)}')
    responses.append(choice)
    if (len(responses) >= len(satisfaction_survey.questions)):
        return redirect('/thank')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thank')
def thank_page():
    return render_template('thank.html')
