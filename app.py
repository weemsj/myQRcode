from flask import Flask, request, render_template
from PIL import Image
import base64
import io
import segno

app = Flask(__name__)


@app.route('/gen_qrcode', methods=['GET', 'POST'])
def gen_qrcode():
    if request.method == 'POST':
        text = request.form['encode-text-input']
        # dark = request.form['']
        # data_dark = request.from['']
        # light = request.form['']
        # scale = request.form['']
        print(text)
        img = segno.make(text, micro=False)
        data = io.BytesIO()
        img.save(data, kind='png', scale=10)
        img_data = base64.b64encode(data.getvalue())

        return render_template('gen_qrcode.j2', code=img_data.decode('utf-8'))
    else:
        return render_template('gen_qrcode.j2')


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


if __name__ == "__main__":
    app.run(debug=True)
