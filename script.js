class PasswordGenerator {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
        this.generatePassword(); // Generate initial password
    }

    initializeElements() {
        // Input elements
        this.passwordOutput = document.getElementById('password-output');
        this.lengthSlider = document.getElementById('length-slider');
        this.lengthValue = document.getElementById('length-value');
        this.uppercaseCheck = document.getElementById('uppercase');
        this.lowercaseCheck = document.getElementById('lowercase');
        this.numbersCheck = document.getElementById('numbers');
        this.symbolsCheck = document.getElementById('symbols');
        this.excludeChars = document.getElementById('exclude-chars');
        
        // Button elements
        this.generateBtn = document.getElementById('generate-btn');
        this.copyBtn = document.getElementById('copy-btn');
        
        // Strength indicator
        this.strengthText = document.getElementById('strength-text');
        this.strengthIndicator = document.getElementById('strength-indicator');
    }

    setupEventListeners() {
        this.lengthSlider.addEventListener('input', () => {
            this.lengthValue.textContent = this.lengthSlider.value;
            this.generatePassword();
        });

        this.generateBtn.addEventListener('click', () => {
            this.generatePassword();
        });

        this.copyBtn.addEventListener('click', () => {
            this.copyToClipboard();
        });

        // Update password when character options change
        const options = [this.uppercaseCheck, this.lowercaseCheck, this.numbersCheck, this.symbolsCheck];
        options.forEach(option => {
            option.addEventListener('change', () => {
                this.generatePassword();
            });
        });

        this.excludeChars.addEventListener('input', () => {
            this.generatePassword();
        });
    }

    generatePassword() {
        const length = parseInt(this.lengthSlider.value);
        const useUppercase = this.uppercaseCheck.checked;
        const useLowercase = this.lowercaseCheck.checked;
        const useNumbers = this.numbersCheck.checked;
        const useSymbols = this.symbolsCheck.checked;
        const exclude = this.excludeChars.value;

        // Validate at least one character type is selected
        if (!useUppercase && !useLowercase && !useNumbers && !useSymbols) {
            this.passwordOutput.value = 'Select at least one character type';
            this.updateStrengthIndicator('none');
            return;
        }

        let charset = '';
        if (useUppercase) charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        if (useLowercase) charset += 'abcdefghijklmnopqrstuvwxyz';
        if (useNumbers) charset += '0123456789';
        if (useSymbols) charset += '!@#$%^&*()_+-=[]{}|;:,.<>?';

        // Remove excluded characters
        if (exclude) {
            charset = charset.split('').filter(char => !exclude.includes(char)).join('');
        }

        // Generate password
        let password = '';
        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * charset.length);
            password += charset[randomIndex];
        }

        this.passwordOutput.value = password;
        this.updateStrengthIndicator(this.calculatePasswordStrength(password));
    }

    calculatePasswordStrength(password) {
        let score = 0;
        
        // Length score
        if (password.length >= 8) score += 1;
        if (password.length >= 12) score += 1;
        if (password.length >= 16) score += 1;
        
        // Character variety score
        if (/[a-z]/.test(password)) score += 1;
        if (/[A-Z]/.test(password)) score += 1;
        if (/[0-9]/.test(password)) score += 1;
        if (/[^a-zA-Z0-9]/.test(password)) score += 1;
        
        // Determine strength level
        if (score <= 2) return 'weak';
        if (score <= 4) return 'fair';
        if (score <= 6) return 'good';
        return 'strong';
    }

    updateStrengthIndicator(strength) {
        const strengthLabels = {
            'none': { text: 'No password', class: '' },
            'weak': { text: 'Weak', class: 'strength-weak' },
            'fair': { text: 'Fair', class: 'strength-fair' },
            'good': { text: 'Good', class: 'strength-good' },
            'strong': { text: 'Strong', class: 'strength-strong' }
        };

        const strengthInfo = strengthLabels[strength];
        this.strengthText.textContent = strengthInfo.text;
        this.strengthIndicator.className = 'strength-indicator ' + strengthInfo.class;
    }

    copyToClipboard() {
        const password = this.passwordOutput.value;
        
        if (!password || password === 'Select at least one character type') {
            alert('Please generate a password first!');
            return;
        }

        navigator.clipboard.writeText(password).then(() => {
            // Visual feedback
            const originalText = this.copyBtn.textContent;
            this.copyBtn.textContent = '✓ Copied!';
            this.copyBtn.style.background = '#28a745';
            
            setTimeout(() => {
                this.copyBtn.textContent = originalText;
                this.copyBtn.style.background = '';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy: ', err);
            alert('Failed to copy password to clipboard');
        });
    }
}

// Initialize the password generator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new PasswordGenerator();
});