from database.db import _hash_password

def test_password_hash_is_salted_and_repeatable_for_same_salt():
    salt="01"*16
    assert _hash_password("a-strong-password",salt)==_hash_password("a-strong-password",salt)
    assert _hash_password("different-password",salt)!=_hash_password("a-strong-password",salt)
