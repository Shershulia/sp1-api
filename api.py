from flask import Flask, jsonify
import random

app = Flask(__name__)

WORDS = [
    "yinger", "give", "code", "addy", "lean", "lil", "succinct", "sp1up",
    "succant", "freakybird", "crabby", "cargo", "pruffer", "be", "prover",
    "PROVEDURLUV", "proof", "content", "deploy", "crash", "sing", "sprint",
    "drip", "flex", "vibe", "cook", "hack", "ship", "zap"
]

def generate_phrase():
    return ' '.join(random.choices(WORDS, k=4))

def phrase_to_hex(phrase):
    return phrase.encode('utf-8').hex()

def random_hex(length):
    return ''.join(random.choices('0123456789abcdef', k=length))

# TASK 1 — Explain proof structure
@app.route('/task_one', methods=['GET'])
def task_one():
    data = {
        "proof": random_hex(512),
        "public_inputs": random_hex(16),
        "vkey_hash": "0x" + random_hex(64),
        "hint": "Identify what each field does in an SP1 proof"
    }
    return jsonify(data)

# TASK 2 — Decode public_inputs
@app.route('/task_two', methods=['GET'])
def task_two():
    phrase = generate_phrase()
    data = {
        "public_inputs": phrase_to_hex(phrase),
        "hint": "Decode public_inputs into a readable phrase"
    }
    return jsonify(data)

# TASK 3 — Find phrase hidden in proof
@app.route('/task_three', methods=['GET'])
def task_three():
    phrase = generate_phrase()
    phrase_hex = phrase_to_hex(phrase)
    proof = phrase_hex + random_hex(512 - len(phrase_hex))
    data = {
        "proof": proof,
        "hint": "A phrase is hidden inside this proof (in hex), find it"
    }
    return jsonify(data)

# TASK 4 — Pick the correct proof
@app.route('/task_four', methods=['GET'])
def task_four():
    correct_phrase = generate_phrase()
    correct_proof = random_hex(512)
    correct_public_inputs = phrase_to_hex(correct_phrase)
    correct_vkey_hash = "0x" + random_hex(64)

    correct_index = random.randint(0, 2)
    proofs = []
    for i in range(3):
        if i == correct_index:
            proofs.append({
                "proof": correct_proof,
                "public_inputs": correct_public_inputs,
                "vkey_hash": correct_vkey_hash,
                "valid": True
            })
        else:
            proofs.append({
                "proof": random_hex(512),
                "public_inputs": phrase_to_hex(generate_phrase()),
                "vkey_hash": "0x" + random_hex(64),
                "valid": False
            })
    data = {
        "hint": f"The correct phrase starts with: '{correct_phrase.split()[0]}'",
        "proofs": proofs
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
