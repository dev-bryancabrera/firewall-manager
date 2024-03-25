class Firewall:

    def __init__(
        self,
        id,
        nombre_regla,
        deactivate_rule,
        tipo_regla,
        regla,
        fecha_creacion,
        estado,
        user_id,
    ) -> None:
        self.id = id
        self.nombre_regla = nombre_regla
        self.deactivate_rule = deactivate_rule
        self.tipo_regla = tipo_regla
        self.regla = regla
        self.fecha_creacion = fecha_creacion
        self.estado = estado
        self.user_id = user_id
