import http

import connexion_buzz


class NoSuchUser(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.BAD_REQUEST


class AlreadyExists(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.BAD_REQUEST


class AuthFailure(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.UNAUTHORIZED


class AccessDenied(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.FORBIDDEN


class InternalError(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
