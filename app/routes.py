from flask import Blueprint, request, jsonify, redirect
from . import db
from .models import URL
import random
import string

main = Blueprint('main', __name__)


def generate_short_code(length=6):
    """Generate a random short code."""
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not URL.query.filter_by(short_code=code).first():
            return code


@main.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'URL Shortener API',
        'endpoints': {
            'POST /shorten': 'Shorten a URL',
            'GET /<short_code>': 'Redirect to original URL',
            'GET /stats/<short_code>': 'Get URL stats',
            'GET /all': 'Get all shortened URLs'
        }
    })


@main.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({'error': 'Please provide a URL'}), 400

    original_url = data['url']

    # Validate URL format
    if not original_url.startswith(('http://', 'https://')):
        return jsonify({'error': 'URL must start with http:// or https://'}), 400

    # Check if URL already shortened
    existing = URL.query.filter_by(original_url=original_url).first()
    if existing:
        return jsonify({
            'message': 'URL already shortened',
            'data': existing.to_dict()
        }), 200

    # Use custom alias or generate one
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


@main.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({'error': 'Short URL not found'}), 404

    url.clicks += 1
    db.session.commit()

    return redirect(url.original_url)


@main.route('/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({'error': 'Short URL not found'}), 404

    return jsonify({
        'message': 'URL stats',
        'data': url.to_dict()
    })


@main.route('/all', methods=['GET'])
def get_all_urls():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return jsonify({
        'message': 'All shortened URLs',
        'count': len(urls),
        'data': [url.to_dict() for url in urls]
    })


@main.route('/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({'error': 'Short URL not found'}), 404

    db.session.delete(url)
    db.session.commit()

    return jsonify({'message': f'Short URL "{short_code}" deleted successfully'})
