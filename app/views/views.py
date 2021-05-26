from flask import request
from ..services.services import CallServices
from http import HTTPStatus

# -------------------------------


def register_series_views(app) -> None:
    @app.route("/series", methods=["POST"])
    def create() -> dict:

        new_serie = CallServices.create(request.get_json())

        if new_serie.get("id"):
            return new_serie, HTTPStatus.CREATED

        return new_serie, HTTPStatus.NOT_ACCEPTABLE

    @app.route("/series", methods=["GET"])
    def series() -> list:

        return {"data": CallServices.select_all_series()}, HTTPStatus.OK

    @app.route("/series/<int:serie_id>", methods=["GET"])
    def select_by_id(serie_id: int) -> dict:

        serie = CallServices.select_serie_by_id(serie_id)

        if serie.get("id"):
            return {"data": serie}, HTTPStatus.OK

        return serie, HTTPStatus.NOT_FOUND
