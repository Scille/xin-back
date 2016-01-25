for cmd in [
    "from tests.test_auth import user",
    "from tests.test_user import another_user",
]:
    try:
        exec(cmd)
    except ImportError as e:
        continue
