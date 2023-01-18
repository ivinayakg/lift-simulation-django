from elevator.utils import env


def getCookie(request):
    try:
        cookie = request.COOKIES[env("COOKIE_NAME")]
        return cookie
    except KeyError:
        raise Exception("Cookie invalid or doesn't exists")
    except Exception:
        raise Exception("Cookie invalid or doesn't exists")
