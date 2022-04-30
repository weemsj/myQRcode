from flask import Flask, request, render_template, send_file
from PIL import Image
import base64
import io
import segno
from segno import helpers


app = Flask(__name__)
   

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/encode_my_life', methods=['GET'])
def encode_my_life():
    return render_template('encode_my_life.html')

@app.route('/text', methods=['POST', 'GET'])
def text():
    # txt = request.form['text-input']
    txt = request.args.get('value')
    print(txt)
    img = segno.make(txt, micro=False)
    data = io.BytesIO()
    img.save(data, kind='png', scale=10)
    img_data = base64.b64encode(data.getvalue())
    data.seek(0)
    return send_file(data, mimetype='image/png')

    #return render_template('encode_my_life.j2', code=img_data.decode('utf-8'))

@app.route('/url')
def url():
    text= request.form['url-input']
    
    return render_template('encode_my_life.html', code=text)



@app.route('/wifi', methods=['POST'])
def wifi():
    ssid = request.form['ssid']
    password = request.form['password'] 
    security = request.form['security']
    qrcode_data = helpers.make_wifi(ssid=ssid, password=password, security=security)
    data = io.BytesIO()
    qrcode_data.save(data, kind='png', scale=10)
    qrcode_data.save('.png')
    #img_data = base64.b64decode(data.getvalue())
    #return render_template('encode_my_life.j2', code=img_data.decode('utf-8'))
    

@app.route('/save', methods=['POST'])
def gen_qrcode_save(save_type):
    # try to send qr code back for saving
    text = request.form['encode-text-input']
    qrcode = segno.make(text)
    if save_type == 'SVG':
        qrcode.save(text +'.svg')
    elif save_type == 'PNG':
        qrcode.save(text + '.png')
    elif save_type == 'EPS':
        qrcode.save(text + '.eps')
    elif save_type == 'TXT':
        qrcode.save(text + '.txt')
    else:
        qrcode.save(text + '.png')


if __name__ == "__main__":
    app.run(debug=True)
