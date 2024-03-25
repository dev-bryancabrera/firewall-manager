from flask_login import UserMixin


class Monitoreo(UserMixin):

    def __init__(self, id, nombre_reporte, reporte, fecha_creacion) -> None:
        self.id = id
        self.nombre_reporte = nombre_reporte
        self.reporte = reporte
        self.fecha_creacion = fecha_creacion
