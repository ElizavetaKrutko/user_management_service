from app.common.utils import get_hashed_password, verify_password


def test_get_hashed_password():
    password = "blablabla"
    hashed_password = get_hashed_password(password)

    assert hashed_password is not None
    assert len(hashed_password) > 0
    assert hashed_password != password


def test_verify_password():
    password = "blablabla"
    hashed_password = get_hashed_password(password)
    assert verify_password(password, hashed_password) is True


def test_verify_password_wrong_password():
    password = "blablabla"
    hashed_password = get_hashed_password(password)

    assert verify_password("lalala", hashed_password) is False


def test_verify_password_wrong_hash():
    password = "blablabla"

    hashed_password = get_hashed_password(password)

    invalid_hashed_password = get_hashed_password("lalala")

    assert verify_password(password, hashed_password) is True
    assert verify_password(password, invalid_hashed_password) is False
