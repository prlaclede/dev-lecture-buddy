import psycopg2, psycopg2.extras, time, os, datetime, logging
from flask import (Flask, Blueprint, render_template, request, 
session, url_for, redirect, send_from_directory)
from flask.ext.iniconfig import INIConfig
from lecturebuddy.modules import *


studentAPI = Blueprint('studentAPI', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@studentAPI.route('/homeStudent', methods=['GET', 'POST'])
def homeStudent():
    if 'admin' not in session:
        return redirect(url_for('welcome'))
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    displayClasses = []
    activeClasses = []
    personClasses = []
    openQs = [] 
    
    try:
        query = "SELECT classid, classname, section FROM class"
        cur.execute(query)
        classes = cur.fetchall()
        try:
            query = "SELECT classid FROM person_class_join WHERE personid = '%s'"
            cur.execute(query % session['personid'])
            results = cur.fetchall()
            
            for item in results:
                personClasses.append(item[0])
            for item2 in classes:
                if item2[0] not in personClasses:
                    temp = "" + str(item2[1]) + " " + str(item2[2])
                    displayClasses.append(temp)
                elif item2[0] in personClasses:
                    temp = "" + str(item2[1]) + " " + str(item2[2])
                    temp2 = [item2[0], temp]
                    activeClasses.append(temp2)
        except:
            errorMessage = "Error Getting Person's Classes"
            print "Error Getting Person's Classes" 
    except:
        errorMessage = "Error Gathering All Classes"
        print "Error Gathering All Classes"
        
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (short_answer_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 't' AND t2.questiontype = 'shortAnswer') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (multiple_choice_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 't' AND t2.questiontype = 'multipleChoice') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (map_selection_q t1 INNER JOIN question_instance t2 ON (t1.questionid = t2.questionid AND t2.open = 't' AND t2.questiontype = 'map') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t1.adminowner = t4.personid)"
        cur.execute(query)
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    
    return render_template('homeStudent.html', error = errorMessage, classes = displayClasses, activeClasses = activeClasses, openQs = openQs)
    
@studentAPI.route('/joinClass', methods=['GET', 'POST'])
def joinClass():
    if 'admin' not in session:
        return redirect(url_for('welcome'))

    #Connect to the database.
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    
    if request.method == 'POST':
        className = request.form['availableClasses']
        name = className.rsplit(' ', 1)[0]
        section = className.rsplit(' ', 1)[1]
        try:
            query = "SELECT personid FROM person WHERE username = '%s'"
            cur.execute(query % session['username'])
            result = cur.fetchone()
            personid = result[0]
            try:
                query = "SELECT classid FROM class WHERE classname = %s AND section = %s"
                cur.execute(query, (name, section))
                results = cur.fetchone()
                classid = results[0]
                try:
                    query1 = "INSERT INTO person_class_join (personid, classid) VALUES (%s, %s)"
                    cur.execute(query1, (personid, classid))
                    conn.commit()
                except:
                    errorMessage = "Error Joining New Class"
                    print "Error Inserting New Class"
            except:
                errorMessage = "Error Joining New Class"
                print "Error Getting Classid"
        except:
            errorMessage = "Error Joining New Class"
            print "Error Getting Personid"
            
        return redirect(url_for('.homeStudent'))
        
    return render_template('homeStudent.html', error = errorMessage)  

@studentAPI.route('/viewInstance', methods=['GET', 'POST'])
def viewInstance():
    if 'admin' not in session:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    questionType = ""
    answerInfo = ""
    choiceInfo = []
    questionInfo = []
    errorMessage = ""
    
    if request.method == 'POST':
        instanceID = request.form['instanceID']
        try:
            query1 = "SELECT questionid, questiontype FROM question_instance WHERE instanceid = '%s'"
            cur.execute(query1 % instanceID)
            instanceInfo = cur.fetchone()
            questionID = instanceInfo[0]
            typeID = instanceInfo[1]
            if typeID == "shortAnswer":
                try:
                    questionType = "Short Answer"
                    query1 = "SELECT question, image, answer, adminowner FROM short_answer_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query5 = "SELECT username FROM person WHERE personid = '%s'"
                        cur.execute(query5 % questionInfo[3])
                        creator = cur.fetchone()[0]
                    except:
                        errorMessage = "Error Getting Question Creator"
                        print "Error Getting Question Creator"
                except:
                    errorMessage = "Error Getting Short Answer Question"
                    print "Error Getting Short Answer Question"     
                    
            if typeID == "multipleChoice":
                try:
                    questionType = "Multiple Choice"
                    query1 = "SELECT question, image, answerid, adminowner FROM multiple_choice_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query2 = "SELECT choicetext, choiceid FROM choices WHERE questionid = '%s'"
                        cur.execute(query2 % questionID)
                        choiceInfo = cur.fetchall()
                        try:
                            query3 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                            cur.execute(query3 % questionInfo[2])
                            answerInfo = cur.fetchone()[0]
                            try:
                                query5 = "SELECT username FROM person WHERE personid = '%s'"
                                cur.execute(query5 % questionInfo[3])
                                creator = cur.fetchone()[0]
                            except:
                                errorMessage = "Error Getting Question Creator"
                                print "Error Getting Question Creator"
                        except:
                            errorMessage = "Error Getting Answer"
                            print "Error Getting Answer" 
                    except:
                        errorMessage = "Error Getting Choices"
                        print "Error Getting Choices"  
                except:
                    errorMessage = "Error Getting Multiple Choice Question"
                    print "Error Getting Multiple Choice Question"  
                    
            if typeID == "map":
                try:
                    questionType = "Map"
                    query1 = "SELECT question, image, answer, adminowner FROM map_selection_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query5 = "SELECT username FROM person WHERE personid = '%s'"
                        cur.execute(query5 % questionInfo[3])
                        creator = cur.fetchone()[0]
                    except:
                        errorMessage = "Error Getting Question Creator"
                        print "Error Getting Question Creator"
                except:
                    errorMessage = "Error Getting Map Question"
                    print "Error Getting map Question"  
        except:
            errorMessage = "Error Getting QuestionId"
            print "Error Getting QuestionID"
            
    if not session['admin']:
        return render_template('questionResponse.html', question=questionInfo, creator=creator, choices=choiceInfo, answerMC=answerInfo, questionType=questionType, questionID=questionID, error=errorMessage,instanceID=instanceID)
    else:
        return render_template('viewInstance.html', question=questionInfo, creator=creator, choices=choiceInfo, answerMC=answerInfo, questionType=questionType, questionID=questionID, error=errorMessage)

@studentAPI.route('/viewQuestion', methods=['GET', 'POST'])
def viewQuestion():
    if 'admin' in session:
        if not session['admin']:
            return redirect(url_for('welcome'))
    else:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    questionType = ""
    answerInfo = ""
    choiceInfo = []
    questionInfo = []
    errorMessage = ""
    
    
    if request.method == 'POST':
        questionID = request.form['questionID'] 
        typeID = request.form['questionType']
        
        if typeID == "shortAnswer":
            try:
                questionType = "Short Answer"
                query1 = "SELECT question, image, answer FROM short_answer_q WHERE questionid = '%s'"
                cur.execute(query1 % questionID)
                questionInfo = cur.fetchone()
            except:
                errorMessage = "Error Getting Short Answer Question"
                print "Error Getting Short Answer Question"     
                
        if typeID == "multipleChoice":
            try:
                questionType = "Multiple Choice"
                query1 = "SELECT question, image, answerid FROM multiple_choice_q WHERE questionid = '%s'"
                cur.execute(query1 % questionID)
                questionInfo = cur.fetchone()
                try:
                    query2 = "SELECT choicetext FROM choices WHERE questionid = '%s'"
                    cur.execute(query2 % questionID)
                    choiceInfo = cur.fetchall()
                    try:
                        query3 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                        cur.execute(query3 % questionInfo[2])
                        answerInfo = cur.fetchone()[0]
                    except:
                        errorMessage = "Error Getting Answer"
                        print "Error Getting Answer" 
                except:
                    errorMessage = "Error Getting Choices"
                    print "Error Getting Choices"  
            except:
                errorMessage = "Error Getting Multiple Choice Question"
                print "Error Getting Multiple Choice Question"  
                
        if typeID == "map":
            try:
                questionType = "Map"
                query1 = "SELECT question, image, answer FROM map_selection_q WHERE questionid = '%s'"
                cur.execute(query1 % questionID)
                questionInfo = cur.fetchone()
            except:
                errorMessage = "Error Getting Map Question"
                print "Error Getting map Question"  
        
    return render_template('viewQuestion.html', question=questionInfo, choices=choiceInfo, answerMC=answerInfo, questionType=questionType, questionID=questionID, error=errorMessage)

@studentAPI.route('/previousQuestions')
def previousQuestions():
    if 'admin' not in session:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    errorMessage = ""
    openQs = [] 
    displayClasses = []
    personClasses = []

    try:
        query = "SELECT classid, classname, section FROM class"
        cur.execute(query)
        classes = cur.fetchall()
        try:
            query = "SELECT classid FROM person_class_join WHERE personid = '%s'"
            cur.execute(query % session['personid'])
            results = cur.fetchall()
            
            for item in results:
                personClasses.append(item[0])
            for item2 in classes:
                if item2[0] in personClasses:
                    temp = "" + str(item2[1]) + " " + str(item2[2])
                    temp2 = [item2[0], temp]
                    displayClasses.append(temp2)
        except:
            errorMessage = "Error Getting Person's Classes"
            print "Error Getting Person's Classes" 
    except:
        errorMessage = "Error Gathering All Classes"
        print "Error Gathering All Classes"
        
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (short_answer_ans t5 INNER JOIN question_instance t2 ON (t5.instanceid = t2.instanceid) INNER JOIN short_answer_q t1 ON (t1.questionid = t2.questionid AND t2.questiontype = 'shortAnswer') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t5.userid = t4.personid) WHERE t4.personid = '%s'"
        cur.execute(query % session['personid'])
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (multiple_choice_ans t5 INNER JOIN question_instance t2 ON (t5.instanceid = t2.instanceid) INNER JOIN multiple_choice_q t1 ON (t1.questionid = t2.questionid AND t2.questiontype = 'multipleChoice') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t5.userid = t4.personid) WHERE t4.personid = '%s'"
        cur.execute(query % session['personid'])
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"
    try:
        query = "SELECT t1.question, t2.instanceid, t3.classid FROM (map_selection_ans t5 INNER JOIN question_instance t2 ON (t5.instanceid = t2.instanceid) INNER JOIN map_selection_q t1 ON (t1.questionid = t2.questionid AND t2.questiontype = 'map') INNER JOIN class t3 ON t3.classid = t2.classid INNER JOIN person t4 on t5.userid = t4.personid) WHERE t4.personid = '%s'"
        cur.execute(query % session['personid'])
        elements = cur.fetchall()
        for element in elements:
            openQs.append(element)
    except:
        errorMessage = "Error Gathering Open Questions"
        print "Error Gathering Open Questions"

    return render_template('previousQuestions.html', openQs = openQs, classes=displayClasses)


@studentAPI.route('/viewResponse', methods=['GET', 'POST'])
def viewResponse():
    if 'admin' not in session:
        return redirect(url_for('welcome'))
        
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    questionType = ""
    answerInfo = ""
    choiceInfo = []
    questionInfo = []
    errorMessage = ""
    response = ""
    responseMap = []
    
    if request.method == 'POST':
        instanceID = request.form['instanceID']
        try:
            query1 = "SELECT questionid, questiontype FROM question_instance WHERE instanceid = '%s'"
            cur.execute(query1 % instanceID)
            instanceInfo = cur.fetchone()
            questionID = instanceInfo[0]
            typeID = instanceInfo[1]
            if typeID == "shortAnswer":
                try:
                    questionType = "Short Answer"
                    query1 = "SELECT question, image, answer, adminowner FROM short_answer_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query1 = "SELECT response FROM short_answer_ans WHERE userid = %s AND instanceid = %s"
                        cur.execute(query1, (session['personid'], instanceID))
                        response = cur.fetchone()[0]
                        try:
                            query5 = "SELECT username FROM person WHERE personid = '%s'"
                            cur.execute(query5 % questionInfo[3])
                            creator = cur.fetchone()[0]
                        except:
                            errorMessage = "Error Getting Question Creator"
                            print "Error Getting Question Creator"
                    except:
                        errorMessage = "Error Getting Short Anwser Response"
                        print "Error Getting Short Answer Response"
                except:
                    errorMessage = "Error Getting Short Answer Question"
                    print "Error Getting Short Answer Question"     
                    
            if typeID == "multipleChoice":
                try:
                    questionType = "Multiple Choice"
                    query1 = "SELECT question, image, answerid, adminowner FROM multiple_choice_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query2 = "SELECT choicetext, choiceid FROM choices WHERE questionid = '%s'"
                        cur.execute(query2 % questionID)
                        choiceInfo = cur.fetchall()
                        try:
                            query3 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                            cur.execute(query3 % questionInfo[2])
                            answerInfo = cur.fetchone()[0]
                            try:
                                query5 = "SELECT username FROM person WHERE personid = '%s'"
                                cur.execute(query5 % questionInfo[3])
                                creator = cur.fetchone()[0]
                                try:
                                    query1 = "SELECT choiceid FROM multiple_choice_ans WHERE userid = %s AND instanceid = %s"
                                    cur.execute(query1, (session['personid'], instanceID))
                                    responseAnswer = cur.fetchone()[0]
                                    try:
                                        query6 = "SELECT choicetext FROM choices WHERE choiceid = '%s'"
                                        cur.execute(query6 % responseAnswer)
                                        response = cur.fetchone()[0]
                                    except:
                                        errorMessage = "Error Getting Multiple Choice Answer Response"
                                        print "Error Getting Multiple Choice Answer Response"
                                except:
                                    errorMessage = "Error Getting Multiple Choice Response"
                                    print "Error Getting Multiple Choice Response"
                            except:
                                errorMessage = "Error Getting Question Creator"
                                print "Error Getting Question Creator"
                        except:
                            errorMessage = "Error Getting Answer"
                            print "Error Getting Answer" 
                    except:
                        errorMessage = "Error Getting Choices"
                        print "Error Getting Choices"  
                except:
                    errorMessage = "Error Getting Multiple Choice Question"
                    print "Error Getting Multiple Choice Question"  
                    
            if typeID == "map":
                try:
                    questionType = "Map"
                    query1 = "SELECT question, image, answer, adminowner FROM map_selection_q WHERE questionid = '%s'"
                    cur.execute(query1 % questionID)
                    questionInfo = cur.fetchone()
                    try:
                        query5 = "SELECT username FROM person WHERE personid = '%s'"
                        cur.execute(query5 % questionInfo[3])
                        creator = cur.fetchone()[0]
                        try:
                            query1 = "SELECT xco, yco FROM map_selection_ans WHERE userid = %s AND instanceid = %s"
                            cur.execute(query1, (session['personid'], instanceID))
                            response1 = cur.fetchone()
                            responseMap.append(response1[0])
                            responseMap.append(response1[1])
                        except:
                            errorMessage = "Error Getting Map Response"
                            print "Error Getting Map Response"
                    except:
                        errorMessage = "Error Getting Question Creator"
                        print "Error Getting Question Creator"
                except:
                    errorMessage = "Error Getting Map Question"
                    print "Error Getting map Question"  
        except:
            errorMessage = "Error Getting QuestionId"
            print "Error Getting QuestionID"

        return render_template('viewResponse.html', responseMap=responseMap, question=questionInfo, creator=creator, choices=choiceInfo, answerMC=answerInfo, questionType=questionType, questionID=questionID, error=errorMessage, instanceID=instanceID, response=response)

