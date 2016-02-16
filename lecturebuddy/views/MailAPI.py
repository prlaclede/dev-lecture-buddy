import os, logging
from flask import (Blueprint, Flask, session, render_template, request, 
redirect, url_for, jsonify, json, current_app)
from flask.ext.mail import Mail
from smtplib import SMTPException
from lecturebuddy.modules import *

mailAPI = Blueprint('mailAPI', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@mailAPI.route('/sendEmails', methods=['POST'])
def sendEmails():
    emails = request.values.get('emails')
    emails = emails.split(',')
    app = current_app._get_current_object()
    mail = Mail(app)
    emailer = Email()
    inviteURL = url_for('accountAPI.register', _external=True)
    invitePage = render_template('emailInviteTemplate.html', inviteURL=inviteURL)
    for email in emails: 
        print(email)
        msg = emailer.get_email(email, 'invite', invitePage)
        try:
            mail.send(msg)
            logger.info('email for ' + email + ' has been sent')
        except SMTPException as error:
            logger.error('Invite email for ' + email + ' failed to send')
            return jsonify(message='error')
    return jsonify(message='success')
        
    
    
''' TODO
def sendConfirmEmail():
    app = current_app._get_current_object()
    mail = Mail(app)
    emailer = Email()
    userEmail = request.values.get('email')
    token = emailer.generate_confirmation_token(userEmail)
    confirmUrl = url_for('.confirmEmail', token=token, purpose='confirm', _external=True)
    confirmPage = render_template('confirmAccountEmail.html', confirmUrl=confirmUrl)
    msg = emailer.get_email(userEmail, 'confirm', confirmPage)
    
    try:
        mail.send(msg)
        logger.info('email sent for ' + userEmail + " has been sent")
        db_session.query(User).filter(User.email==userEmail).update({'token': token, 'pending': False}, synchronize_session='fetch')
        db_session.commit()
        db_session.remove()
    except SMTPException as error:
        logger.error('confirmation email for ' + userEmail + ' failed to send')
        logger.error(error)
    return jsonify(message='success') 
 
@mailAPI.route('/sendResetEmail', methods=['POST'])
def sendResetEmail():
  app = current_app._get_current_object()
  mail = Mail(app)
  emailer = Email()
  
  userEmail = request.values.get('email')
  user = None
    
  try:
    user = db_session.query(User).filter(User.email==userEmail).all()
    user = [i.serialize for i in user]
    db_session.remove()
    
    if (len(user) == 0):
      logger.info('email not found')
      return jsonify(error="email not found")
    else:
        logger.info('email found')
        token = emailer.generate_confirmation_token(userEmail)
        confirmUrl = url_for('.confirmEmail', token=token, purpose='reset', _external=True)
        confirmPage = render_template('resetPasswordEmail.html', confirmUrl=confirmUrl, userEmail=userEmail)
        msg = emailer.get_email(userEmail, 'reset', confirmPage)
        
        try:
          mail.send(msg)
          logger.info('email sent for ' + userEmail + " has been sent")
          db_session.query(User).filter(User.email==userEmail).update({'token': token}, synchronize_session='fetch')
          db_session.commit()
          db_session.remove()
        except SMTPException as error:
          logger.error('password reset email for ' + userEmail + ' failed to send')
          logger.error(error)
        return jsonify(message='success')
  except:
      logger.error('email check failed')



@mailAPI.route('/confirmEmail/<token>/<purpose>')
def confirmEmail(token, purpose):
  emailer = Email()
  user = db_session.query(User).filter(User.token==token).all()
  user = [i.serialize for i in user]
  db_session.remove()
  try:
    email = emailer.confirm_token(token)
    print (user[0]['id'])
    if (purpose == 'confirm'): 
      return redirect(url_for('user_api.completePending', userId=user[0]['id']))
    elif (purpose == 'reset'):
      return redirect(url_for('user_api.resetPassword', userId=user[0]['id']))
  except:
      return "that email token is invalid or has expired!" 
      
'''
      
  