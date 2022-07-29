import featureprobe as fp


def setup_function():
    global split, user  # noqa
    split = fp.Split([
        [[0, 5000]],
        [[5000, 10000]],
    ], None, None)  # noqa
    user = fp.User('test_user_key')


def test_get_user_group():
    common_index = split.find_index(user, 'test_toggle_key')
    assert common_index.index == 0

    split.bucket_by = 'email'
    split.salt = 'abcddeafasde'
    user['email'] = 'test@gmail.com'
    custom_index = split.find_index(user, 'test_toggle_key')
    assert custom_index.index == 1
