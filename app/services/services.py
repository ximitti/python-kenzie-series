import psycopg2

# ------------------------------


class DbConnection:
    def __init__(self) -> None:
        try:
            self.conn = psycopg2.connect(host="localhost", database="kenzie", user="ximitti", password="4282")
            self.is_conn = True
        except (Exception, psycopg2.Error) as error:
            print(error)
            self.is_conn = False

    # -------------------------------
    def create_register(self, serie: dict) -> dict:
        cursor = self.conn.cursor()

        try:
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

        except (Exception, psycopg2.Error) as error:
            print(error)
            cursor.close()
            self.conn.close()

            return {"error": "create table error"}

        try:

            data = [v for v in serie.values()]

            cursor.execute(
                """
                INSERT INTO ka_series
                    (serie, seasons, released_date, genre, imdb_rating)
                VALUES
                    (%s,%s,%s,%s,%s);
                """,
                data,
            )

            cursor.execute(
                """
                SELECT * FROM ka_series
                WHERE serie LIKE %s;
                """,
                serie.get("serie"),
            )

            insert_data = cursor.fetchone()

            self.conn.commit()

            cursor.close()
            self.conn.close()

            return {
                "id": insert_data[0],
                "serie": insert_data[1],
                "seasons": insert_data[2],
                "released_date": insert_data[3],
                "genre": insert_data[4],
                "imdb_rating": insert_data[5],
            }

        except (Exception, psycopg2.Error) as error:
            print(error)
            cursor.close()
            self.conn.close()

            return {"error": "create register error"}

    # -----------------------------------------

    def select_all_series(self) -> list:
        cursor = self.conn.cursor()

        try:
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

        except (Exception, psycopg2.Error) as error:
            print(error)
            cursor.close()
            self.conn.close()

            return {"error": "create table error"}

        try:
            cursor.execute(
                """
                SELECT * FROM ka_series;
                """
            )

            series_list = cursor.fetchall()

            cursor.close()
            self.conn.close()

            return series_list

        except (Exception, psycopg2.Error) as error:
            print(error)
            cursor.close()
            self.conn.close()

            return []

    # ---------------------------

    def select_serie(self, serie_id: int) -> dict:
        cursor = self.conn.cursor()

        try:
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

        except (Exception, psycopg2.Error) as error:
            print(error)
            cursor.close()
            self.conn.close()

            return {"error": "create table error"}

        try:
            print("parametro de entrada:", serie_id)
            cursor.execute(
                """
                SELECT * FROM ka_series
                WHERE id = %s;
                """,
                [serie_id],
            )

            serie = cursor.fetchone()

            cursor.close()
            self.conn.close()

            return serie

        except (Exception, psycopg2.Error) as error:
            print("erro ao pegar por id:", error)
            cursor.close()
            self.conn.close()

            return {"error": "Not Found"}


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

        print("parametro no service:", serie_id)

        return db_conn.select_serie(serie_id)
