from flask import request, jsonify
import jwt

SECRET = "chave-super-secreta"

def require_auth(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"erro": "Token não fornecido"}), 401
        
        try:
            token = token.replace("Bearer ", "")
            jwt.decode(token, SECRET, algorithms=["HS256"])
        except:
            return jsonify({"erro": "Token inválido ou expirado"}), 401
        
        return f(*args, **kwargs)
    
    wrapper.__name__ = f.__name__
    return wrapper
