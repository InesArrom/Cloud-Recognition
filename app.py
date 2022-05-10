from flask import Flask, render_template, request, flash, url_for, redirect
import os


extensions= set(['png', 'jpg', 'JPG', 'PNG'])
def arxiu_permes(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in extensions

app = Flask(__name__)
app.secret_key = "abc"
app.config['UPLOAD_FOLDER'] = './imatges'
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def uploader():
    if request.method == 'POST':
        imatge = request.files['archivo']
        print(arxiu_permes(imatge.filename))

        if not arxiu_permes(imatge.filename):
            flash('Les imatges només poden ser jpg o png')
            return redirect(url_for('index'))

        filename = "nuvol.png"
        imatge.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "<h1>Archivo subido exitosamente</h1>"

if __name__ == "__main__":
    app.run()