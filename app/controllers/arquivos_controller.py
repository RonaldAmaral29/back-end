import os
from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from app import db
from app.models.arquivo import Arquivo

arquivos_bp = Blueprint("arquivos", __name__)

UPLOAD_FOLDER = "uploads"

# Cria a pasta caso não exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------------------------------
# GET /arquivos
# Lista todos os arquivos cadastrados
# ---------------------------------------------------------
@arquivos_bp.route("/", methods=["GET"])
def listar_arquivos():
    arquivos = Arquivo.query.all()

    return jsonify([
        {
            "id": a.id,
            "nome": a.nome,
            "caminho": a.caminho
        } for a in arquivos
    ]), 200


# ---------------------------------------------------------
# POST /arquivos (upload)
# Envia arquivo e salva no banco
# ---------------------------------------------------------
@arquivos_bp.route("/", methods=["POST"])
def upload_arquivo():
    if "arquivo" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    file = request.files["arquivo"]

    if file.filename == "":
        return jsonify({"erro": "Nome de arquivo inválido"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(save_path)

    novo = Arquivo(nome=filename, caminho=save_path)
    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Arquivo enviado com sucesso"}), 201


# ---------------------------------------------------------
# GET /arquivos/download/<id>
# Download do arquivo correto
# ---------------------------------------------------------
@arquivos_bp.route("/download/<int:id>", methods=["GET"])
def download_arquivo(id):
    arquivo = Arquivo.query.get(id)

    if not arquivo:
        return jsonify({"erro": "Arquivo não encontrado"}), 404

    folder = os.path.dirname(arquivo.caminho)
    filename = os.path.basename(arquivo.caminho)

    return send_from_directory(folder, filename, as_attachment=True)


# ---------------------------------------------------------
# DELETE /arquivos/<id>
# Remove arquivo físico + banco
# ---------------------------------------------------------
@arquivos_bp.route("/<int:id>", methods=["DELETE"])
def deletar_arquivo(id):
    arquivo = Arquivo.query.get(id)

    if not arquivo:
        return jsonify({"erro": "Arquivo não encontrado"}), 404

    # Remover fisicamente
    if os.path.exists(arquivo.caminho):
        os.remove(arquivo.caminho)

    db.session.delete(arquivo)
    db.session.commit()

    return jsonify({"mensagem": "Arquivo deletado com sucesso"}), 200
