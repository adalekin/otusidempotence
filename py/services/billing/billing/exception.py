import http

import connexion_buzz


class AlreadyExists(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.BAD_REQUEST


class AuthFailure(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.UNAUTHORIZED


class AccessDenied(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.FORBIDDEN


class InternalError(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR


class NoSuchAccount(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.NOT_FOUND
