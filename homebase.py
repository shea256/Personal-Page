from flask import Flask, render_template, send_from_directory, request
import os
import base64
from Crypto.Cipher import AES
import string
import re

app = Flask(__name__)

app.config.update(
    DEBUG = True,
)

@app.route('/')
def aboutme():
    phone_number = request.args.get('phone_number', '')
    s1 = request.args.get('s1', '')
    email = request.args.get('email', '')
    s2 = request.args.get('s2', '')
    
    # capturing encrypted and base64-encoded parameter
    m = request.args.get('m', '')
    
    if len(m) < 1:
        return render_template('aboutme.html')
    
    # base64 decoding parameter
    try:
        m = base64.urlsafe_b64decode(str(m))
    except:
        print "base64 decoding... invalid URL attempted"
        return render_template('aboutme.html')        
    
    # ensuring parameter is 16 characters for decryption
    if len(m) != 16:
        print "checking length of string... invalid URL attempted"
        return render_template('aboutme.html')
    
    # decrypting parameter
    obj2 = AES.new('ball so hard808s', AES.MODE_ECB)
    decoded_name = obj2.decrypt(m)

    # stripping parameter of whitespace
    decoded_name = string.rstrip(decoded_name)
    if re.match("^[A-Z]'?[- a-zA-Z]+$", decoded_name):
        print decoded_name + " just visited your about page"
    else:
        print "invalid URL attempted"
    
    return render_template('aboutme.html')

@app.route('/encryptname/<name>')
def encryptname(name):
    
    if not re.match("^[A-Z]'?[- a-zA-Z]+$", name):
        return "<p>Invalid characters in name</p>"
    
    name = name[0:16]
    name = string.ljust(name, 16)
    
    if len(name) != 16:
        return "<p>Invalid length of string<p>"
    
    obj = AES.new('ball so hard808s', AES.MODE_ECB)
    
    ciphertext = obj.encrypt(name)
    encoded64 = base64.urlsafe_b64encode(ciphertext)
    
    return "<p>Encoded name: " + encoded64 + "</p>"

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