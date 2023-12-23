import pymysql.cursors

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        db='rentacarro',
        charset='utf8mb4',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )

def execute_query(sql, args=None):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

class Rentacarro:
    @staticmethod
    def get_carros():
        sql = "SELECT * FROM carros"
        return execute_query(sql)

    @staticmethod
    def get_reservas():
        sql = "SELECT * FROM reservas"
        return execute_query(sql)
    
    @staticmethod
    def get_reservas_with_carros():
        sql = """
            SELECT reservas.*, carros.*
            FROM reservas
            JOIN carros ON reservas.idcarro = carros.id
        """
        return execute_query(sql)


    @staticmethod
    def insert_reserva(idcarro, inici_reserva, final_reserva, usuario):
        sql = """
            INSERT INTO reservas (idcarro, iniciReserva, finalReserva, usuario)
            VALUES (%s, %s, %s, %s)
        """
        execute_query(sql, (idcarro, inici_reserva, final_reserva, usuario))

