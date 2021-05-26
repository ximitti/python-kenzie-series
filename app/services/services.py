import psycopg2
from environs import Env

# ------------------------------

env = Env()
env.read_env()

# ------------------------------


class DbConnection:
    fieldnames = ["id", "serie", "seasons", "released_date", "genre", "imdb_rating"]

    def __init__(self) -> None:
        try:
            self.conn = psycopg2.connect(
                host=env("host"), database=env("database"), user=env("user"), password=env("password")
            )
        except (Exception, psycopg2.Error) as error:
            print("Erro de conexão com database:", error)

    # -------------------------------
    def _create_table(self) -> None:
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ka_series(
                        id BIGSERIAL PRIMARY KEY,
                        serie VARCHAR(100) NOT NULL UNIQUE,
                        seasons INTEGER NOT NULL,
                        released_date DATE NOT NULL,
                        genre VARCHAR(50) NOT NULL,
                        imdb_rating FLOAT NOT NULL
                    );
                    """
                )

                self.conn.commit()

        except psycopg2.Error as error:
            print("Erro na criação da tabela:", error)
            self.conn.close()

            return {"error": "create table error"}

    # -------------------------------
    def create_register(self, serie: dict) -> dict:

        self._create_table()

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ka_series
                        (serie, seasons, released_date, genre, imdb_rating)
                    VALUES
                        (%(serie)s,%(seasons)s,%(released_date)s,%(genre)s,%(imdb_rating)s)
                    RETURNING *;
                    """,
                    serie,
                )

                query = cursor.fetchone()

                self.conn.commit()

                new_serie = dict(zip(self.fieldnames, query))
                serie_date = new_serie.get("released_date")
                new_serie["released_date"] = serie_date.strftime("%d/%m/%Y")

                return new_serie

        except (Exception, psycopg2.Error) as error:
            print("Erro ao criar registro:", error)
            self.conn.close()

            return {"error": "create register"}

        finally:
            self.conn.close()

    # -----------------------------------------

    def select_all_series(self) -> list:

        self._create_table()

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM ka_series;
                    """
                )

                query = cursor.fetchall()

                series_list = [dict(zip(self.fieldnames, serie)) for serie in query]
                for serie in series_list:
                    serie_date = serie.get("released_date")
                    serie["released_date"] = serie_date.strftime("%d/%m/%Y")

                return series_list

        except (Exception, psycopg2.Error) as error:
            print("erro ao selecionar todos os registros:", error)
            self.conn.close()

            return []

        finally:
            self.conn.close()

    # ---------------------------

    def select_serie(self, serie_id: int) -> dict:

        self._create_table()

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM ka_series
                    WHERE id = %s;
                    """,
                    (serie_id,),
                )

                query = cursor.fetchone()

                serie = dict(zip(self.fieldnames, query))
                serie_date = serie.get("released_date")
                serie["released_date"] = serie_date.strftime("%d/%m/%Y")

                return serie

        except (Exception, psycopg2.Error) as error:
            print("erro ao pegar por id:", error)
            self.conn.close()

            return {"error": "Not Found"}

        finally:
            self.conn.close()


# -------------------------------------------


class CallServices:
    @staticmethod
    def create(serie: dict) -> dict:
        db_conn = DbConnection()

        return db_conn.create_register(serie)

    @staticmethod
    def select_all_series() -> list:
        db_conn = DbConnection()

        return db_conn.select_all_series()

    @staticmethod
    def select_serie_by_id(serie_id: int) -> dict:
        db_conn = DbConnection()

        return db_conn.select_serie(serie_id)
