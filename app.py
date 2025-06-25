from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import os

PORT = 5000

class MeuHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length).decode()
            dados = urllib.parse.parse_qs(data)
            usuario = dados['usuario'][0].strip()
            senha = dados['senha'][0].strip()

            if not os.path.exists('usuarios.txt'):
                open('usuarios.txt', 'w', encoding='utf-8').close()

            with open('usuarios.txt', 'r', encoding='utf-8') as f:
                for linha in f:
                    if ',' in linha:
                        u, s = linha.strip().split(',')
                        if u == usuario and s == senha:
                            self.send_response(200)
                            self.send_header('Content-type', 'text/html; charset=utf-8')
                            self.end_headers()
                            with open("templates/home.html", "r", encoding="utf-8") as file:
                                content = file.read().replace("{{usuario}}", usuario)
                                self.wfile.write(content.encode("utf-8"))
                            return

            # Login inválido
            self.send_response(401)
            self.end_headers()

        elif self.path == "/cadastro":
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length).decode()
            dados = urllib.parse.parse_qs(data)
            usuario = dados['usuario'][0].strip()
            senha = dados['senha'][0].strip()

            if not os.path.exists('usuarios.txt'):
                open('usuarios.txt', 'w', encoding='utf-8').close()

            with open('usuarios.txt', 'r', encoding='utf-8') as f:
                existentes = [linha.strip().split(',')[0] for linha in f if ',' in linha]

            if usuario in existentes:
                # Usuário já existe
                self.send_response(409)  # conflito
                self.end_headers()
                return

            with open('usuarios.txt', 'a', encoding="utf-8") as f:
                f.write(f"{usuario},{senha}\n")

            # Redireciona para login
            self.send_response(302)
            self.send_header('Location', '/templates/login.html')
            self.end_headers()
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        if self.path == "/":
            self.path = "/templates/index.html"
        elif self.path.startswith("/templates/") or self.path.startswith("/templates/static/"):
            pass
        else:
            self.send_error(404)
            return
        return super().do_GET()


# Inicia o servidor
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Servidor rodando em http://localhost:{PORT}")
HTTPServer(('localhost', PORT), MeuHandler).serve_forever()
