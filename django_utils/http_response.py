from django.http import HttpResponse


def JsonHttpResponse(json):
    response = HttpResponse(json, mimetype="application/json; charset=utf-8")
    response['Pragma'] = "no cache"
    response['Cache-Control'] = "no-cache, must-revalidate"
    return response


def ErrorHttpResponse():
    response = HttpResponse()
    response.status_code = 500
    return response


def NotFoundHttpResponse():
    response = HttpResponse()
    response.status_code = 404
    return response
