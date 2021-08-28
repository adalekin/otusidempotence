import http

import connexion_buzz


class AccessDenied(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.FORBIDDEN


class InternalError(connexion_buzz.ConnexionBuzz):
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
