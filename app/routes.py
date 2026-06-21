from flask import Blueprint, request, jsonify, redirect, send_file, render_template, current_app
from . import db
from .models import URL
import random
import string
import qrcode
import io

main = Blueprint('main', __name__)

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not URL.query.filter_by(short_code=code).first():
            return code

def check_api_key():
    # Mengambil key dari config, default ke 'dev-secret-key' agar tidak error
    required_key = current_app.config.get('API_KEY', 'aokway-secret-2026')
    api_key = request.headers.get('X-API-Key')
    return api_key == required_key

@main.route('/', methods=['GET'])
def index():
    # Pastikan file index.html ada di folder 'templates'
    return render_template('index.html')

@main.route('/shorten', methods=['POST'])
def shorten_url():
    if not check_api_key():
        return jsonify({'error': 'Invalid API key'}), 401
    
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL required'}), 400
        
    # ... (sisa logika shorten_url tetap sama)
    original_url = data['url']
    short_code = data.get('alias') or generate_short_code()
    
    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()
    return jsonify({'data': new_url.to_dict()}), 201

@main.route('/all', methods=['GET'])
def get_all_urls():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return jsonify({'data': [u.to_dict() for u in urls]})

@main.route('/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    if not check_api_key():
        return jsonify({'error': 'Invalid API key'}), 401
    
    url = URL.query.filter_by(short_code=short_code).first()
    if not url:
        return jsonify({'error': 'Not found'}), 404
        
    db.session.delete(url)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@main.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if not url:
        return jsonify({'error': 'Not found'}), 404
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)