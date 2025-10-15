from flask import Flask, render_template, request, jsonify
import random
import string
import re

app = Flask(__name__)

class PasswordGenerator:
    def __init__(self):
        self.character_sets = {
            'uppercase': string.ascii_uppercase,
            'lowercase': string.ascii_lowercase,
            'numbers': string.digits,
            'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
    
    def generate_password(self, length=12, use_uppercase=True, use_lowercase=True, 
                         use_numbers=True, use_symbols=True, exclude_chars=''):
        """
        Generate a random password based on specified criteria
        """
        # Build character set based on user preferences
        charset = ''
        if use_uppercase:
            charset += self.character_sets['uppercase']
        if use_lowercase:
            charset += self.character_sets['lowercase']
        if use_numbers:
            charset += self.character_sets['numbers']
        if use_symbols:
            charset += self.character_sets['symbols']
        
        # Remove excluded characters
        if exclude_chars:
            for char in exclude_chars:
                charset = charset.replace(char, '')
        
        # Validate character set
        if not charset:
            return "Error: At least one character type must be selected"
        
        if length < 4:
            return "Error: Password length must be at least 4 characters"
        
        # Generate password
        password = ''.join(random.choice(charset) for _ in range(length))
        return password
    
    def calculate_strength(self, password):
        """
        Calculate password strength
        """
        if password.startswith("Error:"):
            return "None"
            
        score = 0
        
        # Length score
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if len(password) >= 16: score += 1
        
        # Character variety score
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(not c.isalnum() for c in password): score += 1
        
        # Determine strength
        if score <= 2: return "Weak"
        elif score <= 4: return "Fair"
        elif score <= 6: return "Good"
        else: return "Strong"

# Initialize password generator
pwd_generator = PasswordGenerator()

@app.route('/')
def index():
    """Render the main page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Python Password Generator</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                padding: 30px;
                max-width: 500px;
                width: 100%;
            }
            header {
                text-align: center;
                margin-bottom: 30px;
            }
            header h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 2rem;
            }
            header p {
                color: #666;
                font-size: 1rem;
            }
            .password-display {
                display: flex;
                margin-bottom: 25px;
                gap: 10px;
            }
            #password-output {
                flex: 1;
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 1.1rem;
                font-family: 'Courier New', monospace;
                background: #f9f9f9;
            }
            button {
                padding: 15px 20px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1rem;
                transition: background 0.3s;
            }
            button:hover {
                background: #45a049;
            }
            .controls {
                margin-bottom: 25px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: 600;
                color: #333;
            }
            input[type="range"], input[type="text"] {
                width: 100%;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }
            .checkbox-group {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .checkbox-group label {
                display: flex;
                align-items: center;
                gap: 10px;
                font-weight: normal;
                cursor: pointer;
            }
            .strength-bar {
                height: 10px;
                background: #ddd;
                border-radius: 5px;
                overflow: hidden;
                margin-top: 10px;
            }
            .strength-indicator {
                height: 100%;
                width: 0%;
                transition: all 0.3s ease;
                border-radius: 5px;
            }
            .strength-weak { background: #ff4757; width: 25%; }
            .strength-fair { background: #ffa502; width: 50%; }
            .strength-good { background: #2ed573; width: 75%; }
            .strength-strong { background: #1e90ff; width: 100%; }
            .generate-btn {
                width: 100%;
                padding: 15px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                margin-top: 10px;
            }
            .generate-btn:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🐍 Python Password Generator</h1>
                <p>Powered by Flask - Running on Localhost</p>
            </header>

            <div class="password-display">
                <input type="text" id="password-output" readonly value="Click Generate to create a password">
                <button onclick="copyToClipboard()">📋 Copy</button>
            </div>

            <div class="controls">
                <div class="form-group">
                    <label for="length">Password Length: <span id="length-value">12</span></label>
                    <input type="range" id="length" name="length" min="4" max="50" value="12" oninput="updateLengthValue(this.value)">
                </div>

                <div class="form-group">
                    <label>Character Types:</label>
                    <div class="checkbox-group">
                        <label><input type="checkbox" id="uppercase" checked> Uppercase Letters (A-Z)</label>
                        <label><input type="checkbox" id="lowercase" checked> Lowercase Letters (a-z)</label>
                        <label><input type="checkbox" id="numbers" checked> Numbers (0-9)</label>
                        <label><input type="checkbox" id="symbols" checked> Symbols (!@#$%^&*)</label>
                    </div>
                </div>

                <div class="form-group">
                    <label for="exclude">Exclude Characters:</label>
                    <input type="text" id="exclude" placeholder="e.g., 0O1l">
                </div>

                <button class="generate-btn" onclick="generatePassword()">Generate Password</button>
            </div>

            <div class="form-group">
                <label>Password Strength: <span id="strength-text">-</span></label>
                <div class="strength-bar">
                    <div id="strength-indicator" class="strength-indicator"></div>
                </div>
            </div>
        </div>

        <script>
            function updateLengthValue(value) {
                document.getElementById('length-value').textContent = value;
            }

            function generatePassword() {
                const length = document.getElementById('length').value;
                const uppercase = document.getElementById('uppercase').checked;
                const lowercase = document.getElementById('lowercase').checked;
                const numbers = document.getElementById('numbers').checked;
                const symbols = document.getElementById('symbols').checked;
                const exclude = document.getElementById('exclude').value;

                // Send request to Flask backend
                fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        length: parseInt(length),
                        uppercase: uppercase,
                        lowercase: lowercase,
                        numbers: numbers,
                        symbols: symbols,
                        exclude: exclude
                    })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('password-output').value = data.password;
                    updateStrengthIndicator(data.strength);
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('password-output').value = 'Error generating password';
                });
            }

            function updateStrengthIndicator(strength) {
                const strengthLabels = {
                    'None': { text: 'None', class: '' },
                    'Weak': { text: 'Weak', class: 'strength-weak' },
                    'Fair': { text: 'Fair', class: 'strength-fair' },
                    'Good': { text: 'Good', class: 'strength-good' },
                    'Strong': { text: 'Strong', class: 'strength-strong' }
                };

                const strengthInfo = strengthLabels[strength] || strengthLabels['None'];
                document.getElementById('strength-text').textContent = strengthInfo.text;
                document.getElementById('strength-indicator').className = 'strength-indicator ' + strengthInfo.class;
            }

            function copyToClipboard() {
                const passwordField = document.getElementById('password-output');
                passwordField.select();
                document.execCommand('copy');
                
                // Visual feedback
                const copyBtn = event.target;
                const originalText = copyBtn.textContent;
                copyBtn.textContent = '✓ Copied!';
                copyBtn.style.background = '#28a745';
                
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                    copyBtn.style.background = '';
                }, 2000);
            }

            // Generate initial password on page load
            window.onload = generatePassword;
        </script>
    </body>
    </html>
    """

@app.route('/generate', methods=['POST'])
def generate_password():
    """Generate password based on user input"""
    data = request.json
    
    password = pwd_generator.generate_password(
        length=data.get('length', 12),
        use_uppercase=data.get('uppercase', True),
        use_lowercase=data.get('lowercase', True),
        use_numbers=data.get('numbers', True),
        use_symbols=data.get('symbols', True),
        exclude_chars=data.get('exclude', '')
    )
    
    strength = pwd_generator.calculate_strength(password)
    
    return jsonify({
        'password': password,
        'strength': strength
    })

if __name__ == '__main__':
    print("Starting Python Password Generator...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='127.0.0.1', port=5000)