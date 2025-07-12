from app.app_types.UserType import UserType


def test_is_valid_usertype():
    assert UserType.is_valid_usertype("user")
    assert UserType.is_valid_usertype("User")
    assert UserType.is_valid_usertype(" staff ")
    assert not UserType.is_valid_usertype("admin")
    assert not UserType.is_valid_usertype("")
    assert not UserType.is_valid_usertype("random")
    assert not UserType.is_valid_usertype(None)
