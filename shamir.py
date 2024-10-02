import secrets
import base64
from Crypto.Util import number

def text_to_int(text):
    return int.from_bytes(text.encode('utf-8'), 'big')

def int_to_text(n):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8')

def generate_large_prime(n_bits):
    return number.getPrime(n_bits, randfunc=secrets.token_bytes)

def eval_polynomial(coefficients, x, p):
    result = 0
    for i, coeff in enumerate(coefficients):
        term = coeff * pow(x, i, p)
        result = (result + term) % p
    return result

def int_to_base64(n):
    return base64.b64encode(n.to_bytes((n.bit_length() + 7) // 8, 'big')).decode('ascii')

def base64_to_int(s):
    return int.from_bytes(base64.b64decode(s), 'big')

def shamir_create(privkey, n, k):
    if k > n:
        raise ValueError("Il valore k non può essere maggiore di n.")
    if k < 2:
        raise ValueError("Il valore k deve essere almeno 2.")

    secret_int = text_to_int(privkey)

    # Genera un primo p sufficientemente grande
    prime_bits = max(2048, secret_int.bit_length() + 128)
    p = generate_large_prime(prime_bits)

    # Usa un generatore di numeri casuali crittograficamente sicuro
    coefficients = [secret_int] + [secrets.randbelow(p) for _ in range(k - 1)]

    shares = []
    for i in range(1, n+1):
        x = i
        y = eval_polynomial(coefficients, x, p)
        shares.append((x, y))

    # Converti p e y in base64 per la visualizzazione
    p_base64 = int_to_base64(p)

    shares_base64 = []
    for share in shares:
        x, y = share
        y_base64 = int_to_base64(y)
        shares_base64.append((x, y_base64))

    # Restituisci la chiave master e le parti generate
    return p_base64, shares_base64

def shamir_reconstruct(shares, p_base64):
    p = base64_to_int(p_base64)

    def lagrange_interpolate(x, x_s, y_s, p):
        total = 0
        n = len(x_s)
        for i in range(n):
            xi, yi = x_s[i], y_s[i]
            prod = yi
            for j in range(n):
                if i != j:
                    xj = x_s[j]
                    denom = (xi - xj) % p
                    inv_denom = pow(denom, -1, p)
                    prod = (prod * (x - xj) * inv_denom) % p
            total = (total + prod) % p
        return total

    x_s = [x for x, _ in shares]
    y_s = [base64_to_int(y_base64) for _, y_base64 in shares]

    secret_int = lagrange_interpolate(0, x_s, y_s, p)
    privkey = int_to_text(secret_int)
    return privkey
