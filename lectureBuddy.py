from lecturebuddy import *

@app.route('/')
def mainIndex():
    return render_template('welcome.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
    
@app.route('/emailInvite')
def emailInvite():
    return render_template('emailInvite.html')
    
@app.route('/getQuestionBank', methods=['POST'])
def getQuestionBank():
    questionID = request.values.get('questionID')
    questionInstance = request.values.get('questionInstance')
    return render_template('questionInstance.html', questionID=questionID, questionInstance=questionInstance)
    
if __name__ == '__main__':
    #app.debug=True
    app.run(host='0.0.0.0', port=8080)
