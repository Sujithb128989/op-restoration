# CosmicRAT - Cross-Platform C2 Server Demo

⚠️ **EDUCATIONAL PURPOSE ONLY** ⚠️

This is a **simulated RAT (Remote Access Trojan) demonstration** created for educational and portfolio purposes only. This project is designed to help understand cybersecurity concepts, threat analysis, and defensive strategies.

**IMPORTANT DISCLAIMERS:**
- This is NOT intended for malicious use
- All payloads are dummy/harmless files
- This is for cybersecurity education and demonstration only
- Use only in controlled, authorized environments
- Always comply with local laws and regulations

## 🚀 Project Overview

CosmicRAT simulates a cross-platform RAT backend server with:
- Meme delivery page as a social engineering front
- Disguised payload delivery system (dummy files only)
- Command & Control (C2) server functionality
- REST API for data collection and management
- SQLite database for storing simulated client data

## 🏗️ Architecture

```
CosmicRAT/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Meme delivery page
├── payloads/             # Dummy payload storage
├── uploads/              # File upload storage
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 📋 Features

### Frontend (Meme Delivery Page)
- **Space-themed design** with animated stars and cosmic gradients
- **Tenor GIF integration** for legitimate appearance
- **Download button** that delivers disguised payload
- **Responsive design** for all devices
- **Social engineering simulation** (educational)

### Backend API Endpoints

#### Public Endpoints
- `GET /` - Serves the meme delivery page
- `GET /download` - Delivers disguised dummy payload

#### Payload Communication Endpoints
- `POST /api/register` - Register new client/payload
- `POST /api/upload/keylogs` - Upload keylog data
- `POST /api/upload/tokens` - Upload token data  
- `POST /api/upload/files` - Upload file information

#### Administrative Endpoints
- `GET /api/clients` - List all registered clients
- `GET /api/client/<id>` - Get detailed client information
- `GET /api/stats` - Get overall statistics

### Database Schema

#### Clients Table
- `id` - Primary key
- `client_id` - Unique client identifier
- `ip_address` - Client IP address
- `hostname` - Client hostname
- `operating_system` - Client OS information
- `first_seen` - Registration timestamp
- `last_seen` - Last activity timestamp
- `status` - Client status (active/inactive)

#### Keylogs Table
- `id` - Primary key
- `client_id` - Associated client
- `timestamp` - Log timestamp
- `window_title` - Active window title
- `keystrokes` - Captured keystrokes

#### Tokens Table
- `id` - Primary key
- `client_id` - Associated client
- `timestamp` - Capture timestamp
- `token_type` - Type of token
- `token_value` - Token content
- `source` - Token source application

#### FileInfo Table
- `id` - Primary key
- `client_id` - Associated client
- `timestamp` - File timestamp
- `filename` - File name
- `filepath` - Full file path
- `filesize` - File size in bytes
- `file_type` - File type/extension

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Application**
   - Meme delivery page: `http://localhost:5000`
   - API endpoints: `http://localhost:5000/api/`

## 🔧 API Usage Examples

### Register a Client
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "demo-client-001",
    "hostname": "demo-pc",
    "os": "Windows 10",
    "ip": "192.168.1.100"
  }'
```

### Upload Keylog Data
```bash
curl -X POST http://localhost:5000/api/upload/keylogs \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "demo-client-001",
    "keylogs": [
      {
        "timestamp": "2024-01-15T10:30:00",
        "window_title": "Notepad",
        "keystrokes": "Hello World [DEMO]"
      }
    ]
  }'
```

### Get Client List
```bash
curl http://localhost:5000/api/clients
```

### Get Client Details
```bash
curl http://localhost:5000/api/client/demo-client-001
```

## 🎯 Educational Use Cases

This project demonstrates:

1. **Social Engineering Techniques**
   - Legitimate-looking delivery pages
   - Disguised payload distribution
   - User psychology exploitation

2. **C2 Communication Patterns**
   - Client registration protocols
   - Data exfiltration methods
   - Command and control architecture

3. **Web Application Security**
   - API endpoint design
   - Data validation and handling
   - Database security considerations

4. **Cybersecurity Defense**
   - Understanding attack vectors
   - Identifying malicious patterns
   - Implementing detection mechanisms

## 🛡️ Security Considerations

When studying this code:

- **Network Monitoring**: Learn to detect C2 traffic patterns
- **Behavioral Analysis**: Understand suspicious application behavior
- **Endpoint Protection**: Study how to prevent payload execution
- **User Education**: Recognize social engineering tactics

## ⚠️ Legal and Ethical Guidelines

- **Only use in authorized environments**
- **Never deploy against systems you don't own**
- **Always obtain proper permissions**
- **Follow responsible disclosure practices**
- **Comply with local cybersecurity laws**

## 🎓 Learning Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [SANS Cybersecurity Training](https://www.sans.org/)
- [Cybersecurity Best Practices](https://www.cisa.gov/cybersecurity)

## 🤝 Contributing

This is an educational project. If you're using this for learning:

1. Focus on understanding the security implications
2. Practice implementing defensive measures
3. Study the code to identify vulnerabilities
4. Learn about responsible disclosure

## 📞 Support

For educational questions or cybersecurity discussions, please ensure you're using this knowledge responsibly and ethically.

---

**Remember: With great power comes great responsibility. Use this knowledge to protect, not to harm.**