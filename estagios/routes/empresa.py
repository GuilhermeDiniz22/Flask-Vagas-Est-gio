from flask import Blueprint, request, jsonify
from estagios import db
from estagios.models import Empresa
from sqlalchemy import func

empresa_bp = Blueprint('empresa', __name__, url_prefix='/empresa')

@empresa_bp.route('', methods=['POST'])
def criar_empresa():
    dados = request.get_json()

    if Empresa.query.filter_by(CNPJ=dados.get('CNPJ')).first():
        return jsonify({'erro': 'CNPJ já cadastrado'}), 409

    if Empresa.query.filter_by(email=dados.get('email')).first():
        return jsonify({'erro': 'Email já cadastrado'}), 409

    empresa = Empresa(
        CNPJ=dados.get('CNPJ'),
        endereco=dados.get('endereco'),
        nome=dados.get('nome'),
        descricao=dados.get('descricao'),
        telefone=dados.get('telefone'),
        email=dados.get('email')
    )
    db.session.add(empresa)
    db.session.commit()

    return jsonify({'mensagem': 'Empresa criada com sucesso', 'id': empresa.id}), 201

@empresa_bp.route('/<int:id>', methods=['GET'])
def pegar_empresa(id):
    empresa = Empresa.query.get(id)
    if not empresa:
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    return jsonify({
        'id': empresa.id,
        'nome': empresa.nome,
        'CNPJ': empresa.CNPJ,
        'endereco': empresa.endereco,
        'descricao': empresa.descricao,
        'telefone': empresa.telefone,
        'email': empresa.email
    })

@empresa_bp.route('/buscar', methods=['GET'])
def buscar_empresa_por_nome():
    nome = request.args.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome da empresa'}), 400

    empresa = Empresa.query.filter(func.lower(Empresa.nome).like(f'%{nome.lower()}%')).first()
    if not empresa:
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    return jsonify({
        'id': empresa.id,
        'nome': empresa.nome,
        'CNPJ': empresa.CNPJ,
        'endereco': empresa.endereco,
        'descricao': empresa.descricao,
        'telefone': empresa.telefone,
        'email': empresa.email
    })

@empresa_bp.route('/<int:id>', methods=['PUT'])
def atualizar_empresa(id):
    dados = request.get_json()
    empresa = Empresa.query.get(id)
    if not empresa:
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    empresa.CNPJ = dados.get('CNPJ', empresa.CNPJ)
    empresa.endereco = dados.get('endereco', empresa.endereco)
    empresa.nome = dados.get('nome', empresa.nome)
    empresa.descricao = dados.get('descricao', empresa.descricao)
    empresa.telefone = dados.get('telefone', empresa.telefone)
    empresa.email = dados.get('email', empresa.email)

    db.session.commit()
    return jsonify({'mensagem': 'Empresa atualizada com sucesso'})

@empresa_bp.route('/<int:id>', methods=['DELETE'])
def deletar_empresa(id):
    empresa = Empresa.query.get(id)
    if not empresa:
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    db.session.delete(empresa)
    db.session.commit()
    return jsonify({'mensagem': 'Empresa deletada com sucesso'})
