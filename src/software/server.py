from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from time import time
from base64 import b64encode
from conf import PORT
import os

from .primavera.primavera.primavera import primavera
from .venus.venus import venus

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html");


palette_locations = {'RGB': 'software/primavera/primavera/palettes/rgb.json',
                     'BW': 'software/primavera/primavera/palettes/bw.json',
                     'CMYK': 'software/primavera/primavera/palettes/cmyk.json',
                     'Montana': 'software/primavera/primavera/palettes/montana.json'}

@app.route("/submit",methods=["POST"])
def queue_run():
    '''takes posts to /submit and runs it through primavera'''
    if not 'image' in request.files:
        print("document malformed")
        return "needed submit image"

    ## Querying various requests for primavera
    image = request.files['image']
    palette = palette_locations[request.form['palette']]
    entire = False
    numcolors = int(request.form['colors'])
    dither = request.form['dither']
    overshoot = int(request.form['overshoot'])
    merge = None

    if dither == 'None': dither = None
    if palette != 'software/primavera/palettes/montana.json': entire = True
    if 'merge' in request.form: merge = request.form['merge']

    ## Saving the image so that it can be used by primavera
    save_name = str(time())
    file_path = 'software/primavera/process_queue/'+save_name+'.jpg'
    image.save(file_path)

    ## Calling primavera
    primavera_output = primavera(image=file_path, colors=palette,
                                 palette_size=numcolors, overshoot=overshoot,
                                 merge=merge, dither=dither, entire=entire,
				                 save_labels='out')

    venus(labels=primavera_output, write="hardware/robot/image.tsv")
    print("Robot hardware image updated")

    ## Saving image produced by primavera
    with open("out.png", "rb") as output_image:
        img_data = output_image.read()
        data_uri_header = "data:image/png;base64,"
        data_uri_content = b64encode(img_data).decode("utf-8")
        data_uri = data_uri_header + data_uri_content
        os.remove(file_path)
        return jsonify(**{'img': data_uri})

if __name__ == "__main__":
    app.run(port=PORT, host='0.0.0.0')
