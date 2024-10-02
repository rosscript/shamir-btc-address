from flask import Flask, render_template, request
from crea_btc import generate_private_key_and_address, btclegacy
from shamir import shamir_create
from shamir_dec import shamir_reconstruct
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        user_string = request.form['user_string']
        n = int(request.form['n'])
        k = int(request.form['k'])

        try:
            if k > n:
                error = "k non può essere maggiore di n."
                return render_template('form.html', error=error)

            if k < 2:
                error = "k deve essere almeno 2."
                return render_template('form.html', error=error)

            # Genera chiave privata e indirizzo Bitcoin
            private_key, bitcoin_address = generate_private_key_and_address(user_string)

            # Calcola l'hash SHA256 della chiave privata
            private_key_hash = hashlib.sha256(private_key.encode('utf-8')).hexdigest()

            # Divide la chiave privata usando Shamir
            master_key, shares = shamir_create(private_key, n, k)

            # Passa i risultati alla pagina dei risultati
            return render_template(
                'result.html',
                bitcoin_address=bitcoin_address,
                shares=shares,
                n=n,
                k=k,
                master_key=master_key,
                private_key_hash=private_key_hash  # Passa l'hash al template
            )
        except Exception as e:
            error = str(e)
            return render_template('form.html', error=error)
    else:
        return render_template('form.html')
    
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        try:
            k = int(request.form['k'])
            p_base64 = request.form['master_key'].strip()
            provided_hash = request.form['private_key_hash'].strip()
            shares_input = request.form['shares']
            shares_lines = shares_input.strip().split('\n')
            shares = []
            for line in shares_lines:
                if ',' in line:
                    x_str, y_base64 = line.strip().split(',', 1)
                    x = int(x_str.strip())
                    y_base64 = y_base64.strip()
                    shares.append((x, y_base64))

            if len(shares) < k:
                error = f"Devi inserire almeno {k} parti."
                return render_template('verify.html', error=error)

            # Ricostruisci la chiave privata
            private_key = shamir_reconstruct(k, p_base64, shares)

            # Calcola l'hash SHA256 della chiave privata ricostruita
            private_key_hash = hashlib.sha256(private_key.encode('utf-8')).hexdigest()

            # Confronta l'hash calcolato con quello fornito dall'utente
            if private_key_hash == provided_hash:
                result = "Gli hash corrispondono. La chiave privata è stata ricostruita correttamente."
                hashes_match = True
            else:
                result = "Gli hash NON corrispondono. Potrebbe esserci un errore nei dati forniti."
                hashes_match = False

            return render_template('verify_result.html', result=result, hashes_match=hashes_match)
        except Exception as e:
            error = str(e)
            return render_template('verify.html', error=error)
    else:
        return render_template('verify.html')

    

@app.route('/reconstruct', methods=['GET', 'POST'])
def reconstruct():
    if request.method == 'POST':
        try:
            k = int(request.form['k'])
            p_base64 = request.form['master_key'].strip()
            shares_input = request.form['shares']
            shares_lines = shares_input.strip().split('\n')
            shares = []
            for line in shares_lines:
                if ',' in line:
                    x_str, y_base64 = line.strip().split(',', 1)
                    x = int(x_str.strip())
                    y_base64 = y_base64.strip()
                    shares.append((x, y_base64))

            if len(shares) < k:
                error = f"Devi inserire almeno {k} parti."
                return render_template('reconstruct.html', error=error)

            # Ricostruisci la chiave privata
            private_key = shamir_reconstruct(k, p_base64, shares)

            return render_template('reconstruct_result.html', private_key=private_key)
        except Exception as e:
            error = str(e)
            return render_template('reconstruct.html', error=error)
    else:
        return render_template('reconstruct.html')


@app.route('/display_scanned_content', methods=['GET', 'POST'])
def display_scanned_content():
    qr_content = request.form.get('qr_content') if request.method == 'POST' else ''
    return render_template('display_content.html', qr_content=qr_content)


if __name__ == '__main__':
    app.run(debug=True)
