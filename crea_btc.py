import secrets
import hashlib
import ecdsa
import base58

def generate_secure_random_string(user_input):
    """
    Genera una stringa casuale sicura combinata con l'input dell'utente.
    """
    # Genera una stringa casuale di 256 bit (32 byte) usando secrets
    random_bytes = secrets.token_bytes(32)

    # Verifica che l'input dell'utente sia alfanumerico
    if not user_input.isalnum():
        raise ValueError("Assicurati di inserire solo caratteri alfanumerici.")

    # Converte l'input dell'utente in bytes
    user_bytes = user_input.encode('utf-8')

    # Combina i bytes casuali con quelli dell'utente
    combined_bytes = random_bytes + user_bytes

    # Applica una funzione di hash per ottenere una stringa a lunghezza fissa
    hash_object = hashlib.sha256(combined_bytes)
    hex_string = hash_object.hexdigest()

    return hex_string

# Creazione di un indirizzo Legacy (P2PKH) bitcoin (1..)
def btclegacy(x):
    def hash256(key):
        """Restituisce il doppio sha256."""
        return hashlib.sha256(hashlib.sha256(key).digest()).digest()

    def hash160(key):
        """Restituisce l'hash ripemd160 dopo sha256."""
        ripemd = hashlib.new('ripemd160')
        ripemd.update(hashlib.sha256(key).digest())
        return ripemd.digest()

    def wif(key):
        """Restituisce la chiave privata in formato WIF."""
        sk_net = bytes.fromhex('80') + key
        addr = sk_net + hash256(sk_net)[:4]
        return base58.b58encode(addr)

    def addr(key):
        """Restituisce l'indirizzo Bitcoin."""
        ec_sk = ecdsa.SigningKey.from_string(key, curve=ecdsa.SECP256k1)
        ec_pubk = ec_sk.get_verifying_key()
        pubk = bytes.fromhex('04') + ec_pubk.to_string()
        pkh = bytes.fromhex('00') + hash160(pubk)
        checksum = hash256(pkh)[:4]
        return base58.b58encode(pkh + checksum)

    def pub_key(key):
        """Restituisce la chiave pubblica."""
        ec_sk = ecdsa.SigningKey.from_string(key, curve=ecdsa.SECP256k1)
        ec_pubk = ec_sk.get_verifying_key()
        pubk = bytes.fromhex('04') + ec_pubk.to_string()
        return pubk.hex()

    # Calcolo dell'hash della stringa ottenuta
    secretKey = hashlib.sha256(x.encode()).digest()
    secretKeyW = wif(secretKey)

    # Chiave privata e indirizzo
    privkey2 = secretKeyW.decode("utf-8")
    pubkey2 = addr(secretKey).decode("utf-8")
    pub2 = pub_key(secretKey)

    return privkey2, pubkey2

def generate_private_key_and_address(user_string):
    """
    Funzione principale per generare la chiave privata e l'indirizzo Bitcoin.
    """
    # Genera una stringa casuale sicura combinata con l'input dell'utente
    secure_string = generate_secure_random_string(user_string)

    # Genera la chiave privata e l'indirizzo Bitcoin
    private_key, bitcoin_address = btclegacy(secure_string)

    return private_key, bitcoin_address
