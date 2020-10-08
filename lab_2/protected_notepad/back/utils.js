const crypto = require('crypto')
const rand = require('random-key'); /*https://www.npmjs.com/package/random-key*/

module.exports = {
    generateSessionKey: () => {
        return rand.generate();
    },
    encrypt: (key, text) => {
        const cipher = crypto.createCipher('idea-ofb', key);
        let encrypted = cipher.update(text, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        console.log(encrypted);
        return encrypted;
    },
    decrypt: (key, text) => {
        const decipher = crypto.createDecipher('idea-ofb', key.toString());
        let decrypted = decipher.update(text, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        console.log(decrypted);
        return decrypted;
    }
}