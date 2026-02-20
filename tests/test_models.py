from models import User

def test_user_password_hashing_works_correctly():
    """test that password and checking works correctly"""

    # Arrange: Create a user
    user = User(username='Tester1')
    user.set_password('secret123!')

    # Act & Assert: Check that the password is hashed correctly
    assert user.check_password('secret123!') == True

    assert user.check_password('wrongpassword') == False

    assert user.password_hash != 'secret123!'

    assert user.password_hash is not None