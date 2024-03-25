from .db.connectDB import get_connection


class modelFirewall:

    @classmethod
    def insertRule(self, firewall):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "INSERT INTO firewall_rules(nombre_regla, deactivate_rule, tipo_regla, regla, fecha_creacion, estado, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(
                sql,
                (
                    firewall.nombre_regla,
                    firewall.deactivate_rule,
                    firewall.tipo_regla,
                    firewall.regla,
                    firewall.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
                    firewall.estado,
                    firewall.user_id,
                ),
            )
            db.commit()
            db.close()
            return cursor.lastrowid
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def updateRule(self, estado, deactivate_rule, nombre_regla):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "UPDATE firewall_rules SET estado = %s, deactivate_rule = %s WHERE nombre_regla = %s"
            cursor.execute(
                sql,
                (
                    estado,
                    deactivate_rule,
                    nombre_regla,
                ),
            )
            db.commit()
            db.close()
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def deleteRule(self, regla_nombre):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "DELETE FROM firewall_rules WHERE nombre_regla='{}'".format(
                regla_nombre
            )
            cursor.execute(sql)
            db.commit()
            db.close()
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @classmethod
    def getRulesDeactivate(self):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "SELECT nombre_regla, deactivate_rule, estado FROM firewall_rules WHERE deactivate_rule IS NOT NULL"
            cursor.execute(sql)
            db.close()
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getRules(self):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "SELECT id, nombre_regla, deactivate_rule, tipo_regla, fecha_creacion, estado FROM firewall_rules"
            cursor.execute(sql)
            db.close()
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getRuleByName(self, regla_nombre):
        try:
            db = get_connection()
            cursor = db.cursor()
            sql = "SELECT id, user_id, nombre_regla, deactivate_rule, tipo_regla, fecha_creacion, estado, regla FROM firewall_rules WHERE nombre_regla='{}'".format(
                regla_nombre
            )
            cursor.execute(sql)
            db.close()
            return cursor.fetchone()
        except Exception as ex:
            raise Exception(ex)
