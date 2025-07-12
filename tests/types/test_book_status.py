from app.app_types.BookStatus import BookStatus


def test_is_valid_status():
    assert BookStatus.is_valid_status("available")
    assert BookStatus.is_valid_status("AVAILABLE")
    assert BookStatus.is_valid_status(" borrowed ")

    assert not BookStatus.is_valid_status("lost")
    assert not BookStatus.is_valid_status("")
    assert not BookStatus.is_valid_status("random")
    assert not BookStatus.is_valid_status(None)
