from ..models.ka_series_model import TabelaKaSeries


# -------------------------------------------


class CallServices:
    @staticmethod
    def create(serie: dict) -> dict:
        ka_series = TabelaKaSeries()

        return ka_series.create_register(serie)

    @staticmethod
    def select_all_series() -> list:
        ka_series = TabelaKaSeries()

        return ka_series.select_all_series()

    @staticmethod
    def select_serie_by_id(serie_id: int) -> dict:
        ka_series = TabelaKaSeries()

        return ka_series.select_serie(serie_id)
