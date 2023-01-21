from elevator.utils import env
from django.http import JsonResponse


def getCookieMiddleware(request, *args, **kwargs):
    try:
        cookie = request.COOKIES[env("COOKIE_NAME")]
        return {
            "request": request,
            "args": args,
            "kwargs": {"cookie": cookie, **kwargs},
        }
    except KeyError:
        raise Exception("Cookie invalid or doesn't exists")
    except Exception as e:
        raise Exception("Cookie invalid or doesn't exists")


def middlewareWrapper(*middlewares, view):
    def main(request, *args, **kwargs):
        state = {}
        state["request"] = request
        state["args"] = args
        state["kwargs"] = kwargs

        try:
            for middleware in middlewares:
                result = middleware(state["request"], *
                                    state["args"], **state["kwargs"])
                state = result
            return view(state["request"], *state["args"], **state["kwargs"])
        except Exception as e:
            return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})
    return main
