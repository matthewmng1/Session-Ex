from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def start_page():
    return render_template('start_page.html', survey=survey)

@app.route('/start', methods=['POST'])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def answer():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:quesid>')
def get_question(quesid):
    responses = session.get(RESPONSES_KEY)
    if (responses == None):
        return redirect ('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect ('/complete')
    
    if (len(responses) != quesid):
        flash(f"Invalid question id: {quesid}.")
        return redirect(f"/questions/{len(responses)}") 
    
    question = survey.questions[quesid]
    return render_template(
        "question.html", question_num=quesid, question=question)

@app.route('/complete')
def complete():
    return render_template('/complete.html')