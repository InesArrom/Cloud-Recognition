from flask import Flask, render_template, request, flash, url_for, redirect
import os
from PIL import Image
from PIL import ImageEnhance
import numpy as np
import pandas as pd
import cv2
import math
from time import sleep


extensions = set(['png', 'jpg', 'JPG', 'PNG'])


def arxiu_permes(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in extensions


app = Flask(__name__)
app.secret_key = "abc"
app.config['UPLOAD_FOLDER'] = './static'


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/upload", methods=['POST'])
def uploader():
    if request.method == 'POST':
        imatge = request.files['archivo']
        X_variable = int(request.form['x'])
        Y_variable = int(request.form['y'])

        if not arxiu_permes(imatge.filename):
            flash('Les imatges només poden ser jpg o png')
            return redirect(url_for('index'))

        filename = "nuvol.png"
        imatge.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        rutaImatge = './static/nuvol.png'

        imatgeInicial = Image.open(rutaImatge)

        imgSize = 1000
        imatgeInicial = imatgeInicial.resize(
            (imgSize, imgSize), Image.ANTIALIAS)

        imatgeInicial = ImageEnhance.Brightness(imatgeInicial).enhance(1)

        npframe = np.array(imatgeInicial.getdata())
        imgrgbdf = pd.DataFrame(npframe)
        imgrgbdf = imgrgbdf.rename(columns={0: "R", 1: "G", 2: "B"})

        # Mitja del color vermell
        valorR = int(imgrgbdf.R.mean())

        # Convertim la imatge original a color blanc i negre
        # imgrgbdf['Rnou'] = np.where((imgrgbdf.R>30) & (imgrgbdf.B<200) & (imgrgbdf.G<170), 0, 255)
        imgrgbdf['Rnou'] = np.where((imgrgbdf.R > valorR), 0, 255)
        imgrgbdf['Gnou'] = imgrgbdf['Rnou']
        imgrgbdf['Bnou'] = imgrgbdf['Rnou']
        npModificat = imgrgbdf[['Rnou', 'Gnou', 'Bnou']].to_numpy()
        npModificat = npModificat.reshape(1000, 1000, 3)
        imgBlancNegre = Image.fromarray(npModificat.astype(np.uint8))

        # Guardam la imatge en blanc i negre i la llegim
        imgBlancNegre.save('./static/nuvol_blanc_negre.png')
        imgBlancNegre2 = cv2.imread('./static/nuvol_blanc_negre.png')

        # Contam els píxels blancs i negres
        n_white_pix = np.sum(imgBlancNegre2 == 255)
        n_black_pix = np.sum(imgBlancNegre2 == 0)
        output = f'Percentatge de cel clar: {round((n_white_pix/(n_white_pix+n_black_pix)) * 100, 2)}%'

        img = cv2.imread('./static/nuvol_blanc_negre.png', cv2.COLOR_BGR2GRAY)
        center_px = np.array([4, 3], dtype=np.uint8)

        BLACK = (0,0,0)
        center_px = img[X_variable,Y_variable]
        dist_final = 0
        nube_final = []
        nuvolONo = ""
        if ((center_px == BLACK).all()):
            nuvolONo = "El punt seleccionat és un núvol"
        else:
            for x in range(1000):
                for y in range(1000):
                    color_nube = img[x,y]
                    if(x==0 and y == 0):
                        dist_final = math.sqrt((x - X_variable)**2 + (y - Y_variable)**2)
                    if ((color_nube == BLACK).all()):
                        dist = math.sqrt((x - X_variable)**2 + (y - Y_variable)**2)
                    if dist < dist_final:
                        nube_final = [x,y]
                        dist_final = dist
            nuvolONo = "Coordenades del núvol més pròxim: " + str(nube_final) + " la distància del núvol és de "+ str(round(dist_final, 2))+ " píxels"
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return render_template('upload.html', output=output, nuvol = nuvolONo)

if __name__ == "__main__":
    app.run()