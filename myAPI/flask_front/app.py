from flask import Flask, request, redirect, render_template
import requests

app = Flask(__name__)

API_URL = "http://api:5000"

@app.route("/")
def home():
    return redirect("/usuarios")

@app.route("/usuarios")
def usuarios():
    r = requests.get(f"{API_URL}/v1/usuarios/")
    datos = r.json()["data"]
    return render_template("usuarios.html", usuarios=datos)

@app.route("/agregar", methods=["POST"])
def agregar():
    usuario = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }

    r = requests.post(f"{API_URL}/v1/usuarios/", json=usuario)

    if r.status_code != 200:
        return f"Error API: {r.text}"

    return redirect("/usuarios")


@app.route("/editar/<int:id>")
def editar(id):
    r = requests.get(f"{API_URL}/v1/usuarios/{id}")
    return render_template("editar.html", u=r.json())

@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    usuario = {
        "id": id,
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }
    requests.put(f"{API_URL}/v1/usuarios/{id}", json=usuario)
    return redirect("/usuarios")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    requests.delete(f"{API_URL}/v1/usuarios/{id}")
    return redirect("/usuarios")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
