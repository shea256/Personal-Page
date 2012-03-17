from flask import Flask, render_template, send_from_directory, request
import os
import base64

app = Flask(__name__)

app.config.update(
    DEBUG = False,
)

@app.route('/')
def aboutme():
    phone_number = request.args.get('phone_number', '')
    s1 = request.args.get('s1', '')
    email = request.args.get('email', '')
    s2 = request.args.get('s2', '')
    
    iv = request.args.get('v1', '')
    salt = request.args.get('v2', '')
    ct = request.args.get('v3', '')
    
    n = request.args.get('n', '')
    decoded_name = base64.b64decode(n)
    print decoded_name + " just visited your about page"
    
    return render_template('aboutme.html')

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