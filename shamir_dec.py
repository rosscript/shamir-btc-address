import base64
from functools import reduce

def int_to_text(n):
    try:
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8')
    except OverflowError:
        return ''

def base64_to_int(s):
    return int.from_bytes(base64.b64decode(s), 'big')

def lagrange_interpolation(x_values, y_values, p):
    """Calcola il termine costante del polinomio utilizzando l'interpolazione di Lagrange."""
    k = len(x_values)
    assert k == len(set(x_values)), "I valori di x devono essere unici"

    def _PI(vals):
        acc = 1
        for v in vals:
            acc *= v
        return acc

    secret = 0
    for i in range(k):
        xi, yi = x_values[i], y_values[i]
        others = x_values[:i] + x_values[i+1:]
        numerator = _PI(-other for other in others)
        denominator = _PI(xi - other for other in others)
        inv_denominator = pow(denominator, -1, p)
        term = yi * numerator * inv_denominator
        secret = (secret + term) % p
    return secret

def shamir_reconstruct(k, p_base64, shares):
    """
    Ricostruisce il segreto a partire dalle parti e dalla chiave master.

    Parametri:
    - k: numero di parti necessarie per ricostruire il messaggio
    - p_base64: la chiave master codificata in base64
    - shares: lista di tuple (x, y_base64), dove x è un intero e y_base64 è una stringa base64

    Restituisce:
    - secret_text: la chiave privata ricostruita come stringa
    """
    p = base64_to_int(p_base64.strip())

    x_values = []
    y_values = []

    for x, y_base64 in shares:
        y = base64_to_int(y_base64.strip())
        x_values.append(x)
        y_values.append(y)

    secret_int = lagrange_interpolation(x_values, y_values, p)
    secret_text = int_to_text(secret_int)
    return secret_text
