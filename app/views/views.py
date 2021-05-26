from flask import request, jsonify
from ..services.services import CallServices
from http import HTTPStatus

# -------------------------------


def register_series_views(app) -> None:
    @app.route("/series", methods=["POST"])
    def create() -> dict:

        return {"data": CallServices.create(request.json)}, HTTPStatus.CREATED

    @app.route("/series", methods=["GET"])
    def series() -> list:
        return {"data": CallServices.select_all_series()}, HTTPStatus.OK

    @app.route("/series/<int:serie_id>", methods=["GET"])
    def select_by_id(serie_id: int) -> dict:

        print("parametro na view:", serie_id)
        serie = CallServices.select_serie_by_id(serie_id)

        print(serie)
        if serie:
            return jsonify(serie), HTTPStatus.OK

        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
