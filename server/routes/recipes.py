from flask import Blueprint, request, jsonify, session
from database.models import Users, Recetas
from database import db
from utils.helpers import parse_receta

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/guardar_receta', methods=['POST'])
def guardar_receta():
    try:
        data = request.get_json()
        response = data.get('response')

        if not response:
            return jsonify({'error': 'No se recibió ninguna receta para guardar'}), 400

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Usuario no está logueado'}), 401

        user = Users.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        titulo = parse_receta(response)
        if not titulo:
            return jsonify({'error': 'No se pudo extraer el título de la receta'}), 400

        nueva_receta = Recetas(titulo=titulo, descripcion=response, user_id=user.id)
        db.session.add(nueva_receta)
        db.session.commit()

        return jsonify({'message': 'Receta guardada exitosamente'}), 200

    except Exception as e:
        print(f"Error al guardar receta: {str(e)}")  # Imprime el error en la consola del servidor
        return jsonify({'error': str(e)}), 500

@recipes_bp.route('/get_recipes', methods=['GET'])
def get_recipes():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'No hay usuario logeado'}), 401

    user_id = session.get('user_id')
    user = Users.query.get(user_id)

    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    recetas = Recetas.query.filter_by(user_id=user_id).all()

    if not recetas:
        return jsonify({'error': 'El usuario no tiene recetas guardadas'}), 404

    recetas_dic = [
        {
            'id': recetas.id,
            'titulo': recetas.titulo,
            'descripcion': recetas.descripcion,
        } for recetas in recetas
    ]

    return jsonify({'message': 'Recetas obtenidas correctamente', 'recetas': recetas_dic}), 200