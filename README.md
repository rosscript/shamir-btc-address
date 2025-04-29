# Shamir BTC Address

Un tool per la generazione sicura di indirizzi Bitcoin utili al sequestro di criptovalute, utilizzando lo schema di condivisione segreta di Shamir.

## Descrizione

Questo progetto implementa lo schema di condivisione segreta di Shamir (SSS) per dividere in modo sicuro un indirizzo Bitcoin privato in più parti (shares). Questo approccio permette di:

- Dividere una chiave privata Bitcoin in n parti
- Richiedere k parti (dove k ≤ n) per ricostruire la chiave originale
- Mantenere la sicurezza anche se alcune parti vengono compromesse

## Caratteristiche

- Generazione sicura di shares per indirizzi Bitcoin
- Ricostruzione della chiave privata da un sottoinsieme di shares
- Supporto per diversi schemi di condivisione (n,k)
- Implementazione sicura delle operazioni crittografiche

## Requisiti

- Python 3.8+
- Dependencies (vedi requirements.txt)

## Installazione

```bash
git clone https://github.com/yourusername/shamir-btc-address.git
cd shamir-btc-address
pip install -r requirements.txt
```

## Utilizzo

```bash
python3 app.py
```

