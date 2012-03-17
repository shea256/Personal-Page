from flask import Flask, render_template, send_from_directory
import os
app = Flask(__name__)

@app.route('/')
def aboutme():
    return render_template('aboutme.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)