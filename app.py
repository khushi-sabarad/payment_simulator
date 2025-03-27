from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from cryptography.fernet import Fernet
import secrets
import base64

app = Flask(__name__)

# Database Setup
engine = create_engine('sqlite:///transactions.db')
Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    card_number_encrypted = Column(String)
    amount = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Encryption Setup
secret_key = base64.urlsafe_b64encode(secrets.token_bytes(32)) # Correct Key Generation
fernet = Fernet(secret_key)

def encrypt_card_number(card_number):
    encrypted_card = fernet.encrypt(card_number.encode())
    return encrypted_card.decode()

def decrypt_card_number(encrypted_card_number):
    decrypted_card = fernet.decrypt(encrypted_card_number.encode())
    return decrypted_card.decode()

@app.route('/authorize', methods=['POST'])
def authorize_transaction():
    data = request.get_json()
    card_number = data.get('card_number')
    amount = data.get('amount')

    if not card_number or not amount:
        return jsonify({'error': 'Missing card_number or amount'}), 400

    encrypted_card = encrypt_card_number(card_number)

    # Simulate authorization logic (e.g., check dummy card balance)
    if amount > 1000: # Simulate insufficient funds
        status = 'declined'
    else:
        status = 'authorized'

    session = Session()
    transaction = Transaction(card_number_encrypted=encrypted_card, amount=amount, status=status)
    session.add(transaction)
    session.commit()
    session.close()

    return jsonify({'status': status}), 200

@app.route('/capture', methods=['POST'])
def capture_transaction():
    data = request.get_json()
    transaction_id = data.get('transaction_id')

    if not transaction_id:
        return jsonify({'error': 'Missing transaction_id'}), 400

    session = Session()
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()

    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    if transaction.status == 'authorized':
        transaction.status = 'captured'
        session.commit()
        session.close()
        return jsonify({'status': 'captured'}), 200
    else:
        session.close()
        return jsonify({'error': 'Transaction not authorized'}), 400

@app.route('/refund', methods=['POST'])
def refund_transaction():
    data = request.get_json()
    transaction_id = data.get('transaction_id')

    if not transaction_id:
        return jsonify({'error': 'Missing transaction_id'}), 400

    session = Session()
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()

    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    if transaction.status == 'captured':
        transaction.status = 'refunded'
        session.commit()
        session.close()
        return jsonify({'status': 'refunded'}), 200
    else:
        session.close()
        return jsonify({'error': 'Transaction not captured'}), 400

if __name__ == '__main__':
    app.run(debug=True)