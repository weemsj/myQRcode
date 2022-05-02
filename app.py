from flask import Flask, request, render_template, send_file
from PIL import Image
import base64
import io
import segno
from segno import QRCode, helpers


app = Flask(__name__)
   

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/encode_my_life', methods=['GET'])
def encode_my_life():
    return render_template('encode_my_life.html')

@app.route('/text', methods=['POST', 'GET'])
def text():
    txt = request.form['text-input']
    print(txt)
    #img = segno.make(txt, micro=False)
    #data = io.BytesIO()
    #img.save(data, kind='png', scale=10)
    #img_data = base64.b64encode(data.getvalue())
    qrcode = segno.make(txt, micro=False)
    return render_template( 'encode_my_life.html', qrcode=qrcode)
    #return render_template('encode_my_life.html', txt=txt, code=img_data.decode('utf-8'))

@app.route('/url')
def url():
    text= request.form['url-input']
    qrcode = segno.make(text, micro=False)
    return render_template('encode_my_life.html', qrcode=qrcode)



@app.route('/wifi', methods=['POST'])
def wifi():
    ssid = request.form['ssid']
    password = request.form['password'] 
    security = request.form['inlineRadioSecurity']
    if security == "None":
        security = None
    qrcode = helpers.make_wifi(ssid=ssid, password=password, security=security, hidden=False)
    print(qrcode)
    #qrcode = segno.make_qr(qrcode_data, micro=False, error='h')
    #img_data = base64.b64decode(data.getvalue())
    return render_template('encode_my_life.html', qrcode=qrcode)
    

@app.route('/meCard', methods=['POST'])
def meCard():
    
    name= request.form['lastName'] + "," + request.form['firstName']
    email= request.form['email']
    primaryTel= request.form['primaryTel']
    secondaryTel= request.form['secondaryTel']
    nickname= request.form['nickname']
    birthday= request.form['birthDate'] # YYYY-MM-DD
    url= request.form['website']
    
    vals = [name, email, primaryTel, secondaryTel, nickname, birthday, url]
    
    for v in vals:
        if v == "":
            v = None
            
    if secondaryTel != None:
        tel = (primaryTel, secondaryTel)
    else:
        tel = primaryTel        
        
    qrcode = helpers.make_mecard(name=name, email=email, phone=tel, nickname=nickname, birthday=birthday, url=url)
    return render_template('encode_my_life.html', qrcode=qrcode)

    

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
