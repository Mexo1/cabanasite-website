
from flask import Flask, render_template, request # type: ignore
from flask_mail import Mail, Message # type: ignore
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cheia_ta_secreta'

# Configurare email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'alexvladan12345@gmail.com'
app.config['MAIL_PASSWORD'] = 'ohdd ycfv fcty pbbx'
app.config['MAIL_DEFAULT_SENDER'] = 'alexvladan12345@gmail.com'

mail = Mail(app)    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/camere')
def camere():
    return render_template('camere.html')

@app.route('/galerie')
def galerie():
    return render_template('galerie.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    confirmare = None
    if request.method == 'POST':
        nume = request.form.get('nume')
        email = request.form.get('email')
        mesaj = request.form.get('mesaj')

        corp_mesaj = f"Mesaj de la {nume} ({email}):\n\n{mesaj}"

        try:
            msg = Message(subject="Mesaj nou de la site",
                          body=corp_mesaj,
                          recipients=['alexvladan12345@gmail.com'])
            mail.send(msg)
            confirmare = f"Mulțumim, {nume}! Mesajul tău a fost trimis cu succes."
        except Exception as e:
            confirmare = f"Eroare la trimiterea mesajului: {e}"

    return render_template('contact.html', confirmare=confirmare)


@app.route('/recenzii', methods=['GET', 'POST'])
def recenzii():
    recenzii_path = os.path.join(os.path.dirname(__file__), 'recenzii.json')
    # Încarcă recenziile existente
    if os.path.exists(recenzii_path):
        with open(recenzii_path, 'r', encoding='utf-8') as f:
            recenzii = json.load(f)
    else:
        recenzii = []

    mesaj = None
    if request.method == 'POST':
        if request.form.get('delete_index') is not None:
            admin_pass = request.form.get('admin_pass')
            parola_corecta = 'admin123'  # Poți schimba parola aici
            if admin_pass == parola_corecta:
                try:
                    idx = int(request.form.get('delete_index'))
                    recenzii.pop(len(recenzii) - 1 - idx)
                    with open(recenzii_path, 'w', encoding='utf-8') as f:
                        json.dump(recenzii, f, ensure_ascii=False, indent=2)
                    mesaj = 'Recenzia a fost ștearsă!'
                except Exception:
                    mesaj = 'Eroare la ștergerea recenziei.'
            else:
                mesaj = 'Parolă greșită! Doar administratorul poate șterge recenzii.'
        else:
            autor = request.form.get('autor')
            text = request.form.get('text')
            data = datetime.now().strftime('%d %B %Y')
            recenzie_noua = {
                'autor': autor,
                'text': text,
                'data': data
            }
            recenzii.append(recenzie_noua)
            with open(recenzii_path, 'w', encoding='utf-8') as f:
                json.dump(recenzii, f, ensure_ascii=False, indent=2)
            mesaj = 'Recenzia a fost adăugată cu succes!'
    return render_template('recenzii.html', recenzii=recenzii[::-1], mesaj=mesaj)

@app.route("/sarah")
def sarah():
    return render_template("sarah.html")


if __name__ == '__main__':
    app.run(debug=True)