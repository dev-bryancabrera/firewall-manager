from .db.connectDB import get_connection


class modelPaquetes:

    @classmethod
    def insertPacket(self, monitoreo):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "INSERT INTO monitoreo_paquetes(nombre_reporte, reporte, fecha_creacion) VALUES (%s, %s, %s)"
            cursor.execute(
                sql,
                (
                    monitoreo.nombre_paquete,
                    monitoreo.reporte,
                    monitoreo.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            db.commit()
            db.close()
            return cursor.lastrowid
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def updatePacket(self, monitoreo):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "UPDATE monitoreo_paquetes SET nombre_reporte = %s, reporte = %s, fecha_creacion = %s WHERE id = %s"
            cursor.execute(
                sql,
                (
                    monitoreo.nombre_reporte,
                    monitoreo.reporte,
                    monitoreo.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
                    monitoreo.id,
                ),
            )
            db.commit()
            db.close()
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def deletePacket(self, id):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "DELETE FROM monitoreo_paquetes WHERE id='{}'".format(id)
            cursor.execute(sql)
            db.commit()
            db.close()
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def getPackets(self):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "SELECT id, nombre_reporte, reporte, fecha_creacion FROM monitoreo_paquetes"
            cursor.execute(sql)
            db.close()
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getPacketById(self, id):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "SELECT id, nombre_reporte, reporte, fecha_creacion FROM monitoreo_paquetes WHERE id='{}'".format(
                id
            )
            cursor.execute(sql)
            db.close()
            return cursor.fetchone()
        except Exception as ex:
            raise Exception(ex)
