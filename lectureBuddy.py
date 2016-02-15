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
    
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)
