import pytest
import json
from app import app, Transaction, Session, encrypt_card_number, decrypt_card_number, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope='function')
def test_client():
    app.config['TESTING'] = True
    engine_test = create_engine('sqlite:///:memory:')  # In-memory database for testing
    Base.metadata.create_all(engine_test)
    SessionTest = sessionmaker(bind=engine_test)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Ensure app uses the test database
    with app.test_client() as client:
        with app.app_context():
            yield client, SessionTest  # Yield both client and SessionTest
    engine_test.dispose()  # Dispose the test engine.

def test_authorize_success(test_client):
    client, SessionTest = test_client
    response = client.post('/authorize', json={'card_number': '1234123412341234', 'amount': 100})
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'authorized'}
    session = SessionTest()  # Use the test session
    transaction = session.query(Transaction).filter_by(amount=100).first()
    assert transaction is not None
    session.close()

def test_authorize_fail_amount(test_client):
    client, SessionTest = test_client
    response = client.post('/authorize', json={'card_number': '1234123412341234', 'amount': 1001})
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'declined'}

def test_authorize_missing_data(test_client):
    client, SessionTest = test_client
    response = client.post('/authorize', json={'amount': 100})
    assert response.status_code == 400

def test_capture_success(test_client):
    client, SessionTest = test_client
    auth_response = client.post('/authorize', json={'card_number': '1234123412341234', 'amount': 100})
    assert auth_response.status_code == 200
    session = SessionTest()  # Use the test session
    transaction = session.query(Transaction).filter_by(amount=100).first()
    assert transaction is not None
    session.close()
    response = client.post('/capture', json={'transaction_id': transaction.id})
    assert response.status_code == 200
    assert json.loads(response.data) == {'status': 'captured'}

def test_capture_non_authorized(test_client):
    client, SessionTest = test_client
    response = client.post('/capture', json={'transaction_id': 9999})
    assert response.status_code == 404

def test_encryption_decryption(test_client):
    client, SessionTest = test_client
    card_number = '1234567890123456'
    encrypted = encrypt_card_number(card_number)
    decrypted = decrypt_card_number(encrypted)
    assert decrypted == card_number