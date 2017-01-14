from requests import Response


def return_response(status_code=200):
    resp = Response()
    resp.status_code = status_code
    return resp
