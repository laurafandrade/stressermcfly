from flask import Flask, render_template, request, redirect, url_for, session
import threading
import time
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'McFlySystem2025'  # Chave secreta pro login

# Diretório de logs
if not os.path.exists('logs'):
    os.makedirs('logs')

# Login
USERNAME = 'mcflyoperador123'
PASSWORD = 'apenasumasenha12345'  # Altere sua senha aqui

# Função de ataque (simulação)
def ataque(url, tempo, threads):
    fim = time.time() + tempo
    while time.time() < fim:
        for _ in range(threads):
            print(f"Enviando requisição para {url}")
        time.sleep(1)

    gerar_log(url)


# Gera relatório
def gerar_log(url):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    codigo = os.urandom(4).hex().upper()
    log = f"URL:{url} | DATA&HORA:{agora} | CÓDIGO:{codigo}\n"

    with open('logs/relatorio.txt', 'a') as f:
        f.write(log)


@app.route('/')
def home():
    if 'logged_in' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (request.form['username'] == USERNAME and
                request.form['password'] == PASSWORD):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', erro='Credenciais incorretas')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/ataque', methods=['POST'])
def iniciar_ataque():
    if 'logged_in' in session:
        url = request.form['url']
        tempo = min(int(request.form['tempo']), 200)  # Limite de 200 segundos
        threads = int(request.form['threads'])

        thread = threading.Thread(target=ataque, args=(url, tempo, threads))
        thread.start()

        return f"Ataque iniciado em {url} por {tempo} segundos com {threads} threads."
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
