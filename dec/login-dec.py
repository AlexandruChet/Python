from functools import wraps


def login_req(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_info = args[0]

        if not user_info.get("is_logged"):
            return "Error"

        return func(*args, **kwargs)
    return wrapper


@login_req
def get_profile(user):
    return f"Profile: {user['name']}"


user = {"name": "Alex", "is_logged": True}
print(get_profile(user))

user = {"name": "Jacob", "is_logged": False}
print(get_profile(user))
