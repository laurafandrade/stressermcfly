from flask import Flask, render_template, request, redirect, url_for, session, send_file
import threading
import time
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'mcflykeysupersecreta'

# Cria pasta de logs se não existir
if not os.path.exists('logs'):
    os.makedirs('logs')

# Usuário e senha
USERNAME = 'admin'
PASSWORD = '123456'

# Função simulada de ataque
def start_attack(url, time_attack):
    print(f"Iniciando ataque para {url} por {time_attack} segundos...")
    now = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    code = os.urandom(4).hex()

    log = f"URL:{url} | DATA&HORA:{now} | CÓDIGO:{code}\n"
    with open(f"logs/log_{now}.txt", 'w') as file:
        file.write(log)

    time.sleep(time_attack)
    print(f"Ataque para {url} finalizado.")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if user == USERNAME and password == PASSWORD:
            session['user'] = user
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        url = request.form['url']
        time_attack = int(request.form['time'])
        if time_attack > 200:
            time_attack = 200

        threading.Thread(target=start_attack, args=(url, time_attack)).start()

        return render_template('index.html', message=f"Ataque iniciado para {url} por {time_attack} segundos!")

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/logs')
def download_logs():
    list_logs = os.listdir('logs')
    if list_logs:
        latest_log = sorted(list_logs)[-1]
        return send_file(f'logs/{latest_log}', as_attachment=True)
    return "Nenhum log encontrado."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
