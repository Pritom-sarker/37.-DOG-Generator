from flask import Flask
from flask import send_file
app = Flask(__name__)

@app.route('/get_image')
def get_image():
    filename = 'Black#100.png'
    return send_file(filename, mimetype='image/gif')

@app.route('/get_data')
def get_data():
   return 'Hello World'

if __name__ == '__main__':
   app.run()