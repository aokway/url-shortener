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
    api_key = request.headers.get('X-API-Key')
    if api_key != current_app.config['API_KEY']:
        return False
    return True


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/api', methods=['GET'])
def api_info():
    return jsonify({
        'message': 'URL Shortener API',
        'endpoints': {
            'POST /shorten': 'Shorten a URL (requires API key)',
            'GET /<short_code>': 'Redirect to original URL',
            'GET /stats/<short_code>': 'Get URL stats',
            'GET /qr/<short_code>': 'Generate QR Code',
            'GET /all': 'Get all shortened URLs',
            'DELETE /<short_code>': 'Delete a URL (requires API key)'
        }
    })


@main.route('/shorten', methods=['POST'])
def shorten_url():
    if not check_api_key():
        return jsonify({'error': 'Invalid or missing API key'}), 401

    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({'error': 'Please provide a URL'}), 400

    original_url = data['url']

    if not original_url.startswith(('http://', 'https://')):
        return jsonify({'error': 'URL must start with http:// or https://'}), 400

    existing = URL.query.filter_by(original_url=original_url).first()
    if existing:
        return jsonify({
            'message': 'URL already shortened',
            'data': existing.to_dict()
        }), 200

    custom_alias = data.get('alias')
    if custom_alias:
        if URL.query.filter_by(short_code=custom_alias).first():
            return jsonify({'error': 'Alias already taken'}), 409
        short_code = custom_alias
    else:
        short_code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        'message': 'URL shortened successfully',
        'data': new_url.to_dict()
    }), 201


@main.route('/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({'error': 'Short URL not found'}), 404

    return jsonify({
        'message': 'URL stats',
        'data': url.to_dict()
    })


@main.route('/qr/<short_code>', methods=['GET'])
def generate_qr(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({'error': 'Short URL not found'}), 404

    qr = qrcode.make(f"https://shortway-links.up.railway.app/{short_code}")
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


@main.route('/all', methods=['GET'])
def get_all_urls():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return jsonify({
        'message': 'All shortened URLs',
        'count': len(urls),
        'data': [url.to_dict() for url in urls]
    })


@main.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({'error': 'Short URL not found'}), 404

    url.clicks += 1
    db.session.commit()

    return redirect(url.original_url)


@main.route('/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    if not check_api_key():
        return jsonify({'error': 'Invalid or missing API key'}), 401

    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({'error': 'Short URL not found'}), 404

    db.session.delete(url)
    db.session.commit()

    return jsonify({'message': f'Short URL "{short_code}" deleted successfully'})