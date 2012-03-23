from flask import Flask, render_template, send_from_directory, request
import os
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA
import string
import re
from flaskext.mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config.update(
    DEBUG = False,
    #Email settings
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587, # 465 or 587
    MAIL_USE_TLS = True,
    MAIL_USERNAME = 'mailbot@ryanshea.org',
    MAIL_PASSWORD = 'ballsohard',
    MAIL_FAIL_SILENTLY = True,
)

mail = Mail(app)

regex_name = "^[A-Z]'?[- a-zA-Z]+$"
regex_email = "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"

@app.route('/')
def aboutme():
    #pn_salt = 'd786dff79a90'
    #email_salt = 'b2832fa81995'
    correct_phone_hash = 'YKHeeo7VOTo/OTI9Q+fPy/UUirw='
    email_hash1 = 'UYTI6hPxlbUROrPG8L6DRh2gvdo='
    email_hash2 = 'eWnrgcZ7f6h7dRjgCm1DjJRPQQY='
    email_hash3 = 'SYk+FeQ18NpWPwve4tK8C/0gAfE='
    phone_number = ""
    email = ""
    
    # grab
    unverified_phone_number = request.args.get('phone_number', '')
    s1 = request.args.get('s1', '')
    unverified_email = request.args.get('email', '')
    s2 = request.args.get('s2', '')
    
    # verifying phone number
    hash1 = SHA.new()
    hash1.update(str(s1) + str(unverified_phone_number))
    if (base64.b64encode(hash1.digest()) == correct_phone_hash):
        phone_number = unverified_phone_number
    
    # verifying email address
    hash2 = SHA.new()
    hash2.update(str(s2) + str(unverified_email))
    b = base64.b64encode(hash2.digest())
    if (b == email_hash1 or b == email_hash2 or b == email_hash3):
        email = unverified_email
    
    # capture encrypted and base64-encoded parameter
    # if no viewer tracking id is present, stop and render the template
    i1 = request.args.get('i1', '')
    encrypted_name = i1
    i2 = request.args.get('i2', '')
    encrypted_email = i2
    
    if (len(encrypted_name) < 1) or (len(encrypted_email) < 1):
        return render_template('aboutme.html', email=email, phone_number=phone_number)
    
    # parse url options
    a1 = request.args.get('a1', '')
    show_welcome_popup = False
    if a1 is "1":
        show_welcome_popup = True
    a2 = request.args.get('a2', '')
    send_welcome_email = False
    if a2 == "1":
        send_welcome_email = True
    
    # base64 decoding name
    try:
        encrypted_name = base64.urlsafe_b64decode(str(encrypted_name))
    except:
        print "base64 decoding... invalid URL attempted (name)"
        return render_template('aboutme.html', email=email, phone_number=phone_number)
    
    # base64 decoding email
    try:
        encrypted_email = base64.urlsafe_b64decode(str(encrypted_email))
    except:
        print "base64 decoding... invalid URL attempted (email)"
        return render_template('aboutme.html', email=email, phone_number=phone_number)
    
    # ensuring parameter is 16 characters for decryption
    if (len(encrypted_name) != 16) or (len(encrypted_email) != 64):
        print "checking length of string... invalid URL attempted"
        return render_template('aboutme.html', email=email, phone_number=phone_number)
    
    # decrypting name and email
    obj = AES.new('ball so hard808s', AES.MODE_ECB)
    decrypted_name = obj.decrypt(encrypted_name)
    decrypted_email = obj.decrypt(encrypted_email)

    # stripping parameter of whitespace
    decrypted_name = string.rstrip(decrypted_name)
    decrypted_email = string.rstrip(decrypted_email)
    if (re.match(regex_name, decrypted_name)) and (re.match(regex_email, decrypted_email)):
        # our name and email is now verified - let's do some fun stuff
        
        # log our visitor
        print "#####_____##### " + decrypted_name + " (" + decrypted_email + ")" + " just visited your about page #####_____#####"
        
        # send our visitor a thank you for visiting our page
        if send_welcome_email:
            message_html = '<p>' + decrypted_name + ', thank you for visiting my about page!' + '</p>'
            msg = Message("Thank you for visiting my about page!", sender=("Ryan Shea's Mailbot", "info@princetoneclub.com"), recipients=[decrypted_email])
            #msg.html = message_text
            msg.html = message_html
            #print "sending welcome email... To: " + str(msg.recipients)
            mail.send(msg)
    else:
        print "invalid URL attempted"
    
    return render_template('aboutme.html', email=email, phone_number=phone_number, show_welcome_popup=show_welcome_popup)

def encryptname(name):
    if len(name) > 16:
        return "<p>Name must be limited to 16 characters<p>"
    
    if not re.match(regex_name, name):
        return "<p>Incorrectly formatted name</p>"
    
    name = name[0:16]
    name = string.ljust(name, 16)
    if len(name) != 16:
        return "<p>Error adjusting string length<p>"
    
    obj = AES.new('ball so hard808s', AES.MODE_ECB)
    
    name_encrypted = obj.encrypt(name)
    name_encrypted_encoded = base64.urlsafe_b64encode(name_encrypted)
    
    return name_encrypted_encoded

def encryptemail(email):
    if len(email) > 64:
        return "<p>Email must be limited to 64 characters<p>"
    
    if not re.match(regex_email, email):
        return "<p>Incorrectly formatted email</p>"
    
    email = email[0:64]
    email = string.ljust(email, 64)
    if len(email) != 64:
        return "<p>Error adjusting string length</p"
    
    obj = AES.new('ball so hard808s', AES.MODE_ECB)
    
    email_encrypted = obj.encrypt(email)
    email_encrypted_encoded = base64.urlsafe_b64encode(email_encrypted)
    
    return email_encrypted_encoded

@app.route('/encryptcontact/<name>/<email>')
def encryptcontact(name, email):
    url_tracker = "<h3>URL Tracker</h3><p>&i1=" + encryptname(name) + "&i2=" + encryptemail(email) + "</p>"
    return url_tracker

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/bio')
def bio():
    return render_template('bio.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)