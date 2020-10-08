const crypto = require('crypto')

module.exports = {
    encrypt: (key, text) => {
        const cipher = crypto.createCipher('idea-ofb', key);
        let encrypted = cipher.update(text, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        return encrypted;
    },
    decrypt: (key, text) => {
        const decipher = crypto.createDecipher('idea-ofb', key);
        let decrypted = decipher.update(text, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        return decrypted;
    }
}