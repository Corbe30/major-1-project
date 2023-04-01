import rsa

blacklist = []

def RSAencrypt(pt, key):
    return rsa.encrypt(pt.encode('ascii'), key)

def RSAdecrypt(ct, key):
    try:
        return rsa.decrypt(ct, key).decode('ascii')
    except:
        return False
    
def RSAsign(message, key):
    return rsa.sign(message.encode('ascii'), key, 'SHA-1')

def RSAverify(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key,) == 'SHA-1'
    except:
        return False