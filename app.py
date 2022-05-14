from time import sleep
from flask import Flask, request, render_template, send_file
from PIL import Image
import base64
import io
import qrCodeLive
import segno
from segno import QRCode, helpers

live = qrCodeLive

app = Flask(__name__)

colors = {
    'red': 127,
    'green': 127,
    'blue': 127
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/encode_my_life', methods=['GET'])
def encode_my_life():
    return render_template('encode_my_life.html')


@app.route('/decode_my_life')
def decode_my_life():
    return render_template('decode_my_life.html')


@app.route('/text', methods=['POST', 'GET'])
def text():
    if request.method == 'POST':
        text = request.form['text-input']
        r = request.form.get('redText')
        g = request.form.get('greenText')
        b = request.form.get('blueText')
        qrcode = segno.make(text, micro=False)
        if r == None:
            return render_template( 'encode_my_life.html', qrcode=qrcode, text=text, route='text', color=colors)    
        colors['red'] = int(r)    
        colors['green'] = int(g)
        colors['blue'] = int(b)
        return render_template( 'encode_my_life.html', qrcode=qrcode, text=text, route='text', color=colors)


@app.route('/url', methods=['POST'])
def url():
    if request.method == 'POST':
        text = request.form.get('url-input')
        print(text)
        r = request.form.get('redURL')
        g = request.form.get('greenURL')
        b = request.form.get('blueURL')
        qrcode = segno.make(text, micro=False)
        if r == None:
            return render_template( 'encode_my_life.html', qrcode=qrcode, text=text, route='text', color=colors)
        
        colors['red'] = int(r)    
        colors['green'] = int(g)
        colors['blue'] = int(b)
        return render_template( 'encode_my_life.html', qrcode=qrcode, text=text, route='url', color=colors)



@app.route('/wifi', methods=['POST'])
def wifi():
    ssid = request.form['ssid']
    password = request.form['password'] 
    security = request.form['inlineRadioSecurity']
    if security == "None":
        security = None
    qrcode = helpers.make_wifi(ssid=ssid, password=password, security=security, hidden=False)
    text = "wifi"+ ssid
    r = request.form.get('redWifi')
    g = request.form.get('greenWifi')
    b = request.form.get('blueWifi')
    if r == None:    
        return render_template('encode_my_life.html', qrcode=qrcode, text=text, route='wifi', color=colors)
    colors['red'] = int(r)    
    colors['green'] = int(g)
    colors['blue'] = int(b)    
    return render_template('encode_my_life.html', qrcode=qrcode, text=text, route='wifi', color=colors) 


@app.route('/meCard', methods=['POST'])
def meCard():
    
    name= request.form['lastName'] + "," + request.form['firstName']
    email= request.form['email']
    primaryTel= request.form['primaryTel']
    secondaryTel= request.form['secondaryTel']
    nickname= request.form['nickname']
    birthday= request.form['birthDate'] # YYYY-MM-DD
    url= request.form['website']
    
    r = request.form.get('redMeCard')
    g = request.form.get('greenMeCard')
    b = request.form.get('blueMeCard')
    
    vals = [name, email, primaryTel, secondaryTel, nickname, birthday, url]
    
    for v in vals:
        if v == "":
            v = None
            
    if secondaryTel != None:
        tel = (primaryTel, secondaryTel)
    else:
        tel = primaryTel        
        
    text = name + "'s_meCard"
    qrcode = helpers.make_mecard(name=name, email=email, phone=tel, nickname=nickname, birthday=birthday, url=url)
    
    if r == None:
        return render_template('encode_my_life.html', qrcode=qrcode, text=text, route='meCard', color=colors)
    colors['red'] = int(r)    
    colors['green'] = int(g)
    colors['blue'] = int(b)
    return render_template('encode_my_life.html', qrcode=qrcode, text=text, route='meCard', color=colors)
    

@app.route('/geo', methods=['POST'])
def geo():
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    text = address + ', ' + city + ', ' + state
    with open('geo-location/input.txt', 'w') as f:
        f.write(text)
    sleep(5)
    f = open('geo-location/output.txt', 'r')
    coor = f.read() 
    latt, long = coor.split(', ')
    latitude = float(latt)
    longitude = float(long)  
    qrcode = segno.helpers.make_geo(latitude, longitude)
    r = request.form.get('redGeo')
    g = request.form.get('greenGeo')
    b = request.form.get('blueGeo')
    if r == None:
        return render_template('encode_my_life.html', qrcode=qrcode, text=text, route='geo', color=colors)
    colors['red'] = int(r)    
    colors['green'] = int(g)
    colors['blue'] = int(b)
    return render_template('encode_my_life.html', qrcode=qrcode, text=text, route='geo', color=colors)
    
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
