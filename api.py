# coding: utf-8
from flask import Blueprint, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth
from banco import Banco

bp_api = Blueprint('api', __name__, url_prefix='/jogos/api/v1/lista')
banco = Banco()

auth = HTTPBasicAuth()

lista = []


@auth.get_password

def verificar_acesso(username) :
	if username == 'tulio' :
		return '123'
	return None

@auth.error_handler

def acesso_negado() :
	return make_response(jsonify({'error': 'acesso negado'}), 403)


@bp_api.route('/', methods=['GET'])
@bp_api.route('/<int:id>', methods=['GET'])
@auth.login_required
def get_games( id = None ):
	lista = banco.listJogos()
	if lista != False:
		if id != None :
			lista = banco.getJogo(id)
			return jsonify({'lista': lista})
		return jsonify({'lista': lista})

	return make_response(jsonify({'error': u'Nenhum dado encontrado!'}), 404)

@bp_api.route('/add/', methods=['POST'])
@auth.login_required
def add_games():
    if request.json :
    	banco.saveJogo(request.json[0])
    return make_response(jsonify({'error': u'Dados inseridos com sucesso!'}), 404)

@bp_api.route('/alter/<int:id>', methods=['PUT'])
@auth.login_required
def put_games( id = None ):
    if request.json and id != None :
    	banco.updateJogo(id, request.json[0])
    return make_response(jsonify({'error': u'Dados alterado com sucesso!'}), 404)

@bp_api.route('/del/<id>', methods=['DELETE'])
@auth.login_required
def del_games( id = None ):
    if id != None :
        banco.deleteJogo(id)
    return make_response(jsonify({'error': u'O item ({}) foi excluido com sucesso!'.format(id)}), 404)
