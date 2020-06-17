# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-06-15.
# Copyright (c) 2020 3KWan.
# Description :
from flask import Response, jsonify


class JSONResponse(Response):

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
            return super(JSONResponse, cls).force_type(response, environ)


def fast_response(response: dict):
    print(response)
    if response.get('status') == 0:
        return response, 200
    else:
        return response, response.get('status')


def handle_request_params(p: str, ts: str) -> bool:
    if p is None or ts is None:
        print("a")
        return False
    elif p == "" or ts == "":
        print("bcd")
        return False
    else:

        return True
