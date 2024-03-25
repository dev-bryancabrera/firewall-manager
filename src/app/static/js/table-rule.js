$(document).ready(function () {
  var $tableFirewallOut = $("#tableFirewallOut");

  $tableFirewallOut.bootstrapTable({
    search: true,
    showColumns: true,
    pagination: true,
    locale: "es-ES",
    columns: [
      {
        field: "numero",
        title: "N° Regla",
        sortable: true,
      },
      {
        field: "nombre",
        title: "NOMBRE DE REGLA",
        sortable: true,
      },
      {
        field: "fecha_creacion",
        title: "FECHA DE CREACION",
        sortable: true,
      },
      {
        field: "direccion",
        title: "DESTINO",
        sortable: true,
      },
      {
        field: "accion",
        title: "PERMISO",
        sortable: true,
      },
      {
        field: "protocolo",
        title: "PROTOCOLO",
        sortable: true,
      },
      {
        field: "entrada",
        title: "ENTRADA/SALIDA",
        sortable: true,
      },
      {
        field: "ip",
        title: "ORIGEN",
        sortable: true,
      },
    ],
  });
});

$(document).ready(function () {
  var $tableFirewallIn = $("#tableFirewallIn");

  $tableFirewallIn.bootstrapTable({
    search: true,
    showColumns: true,
    pagination: true,
    locale: "es-ES",
    columns: [
      {
        field: "numero",
        title: "N° Regla",
        sortable: true,
      },
      {
        field: "nombre",
        title: "NOMBRE DE REGLA",
        sortable: true,
      },
      {
        field: "fecha_creacion",
        title: "FECHA DE CREACION",
        sortable: true,
      },
      {
        field: "direccion",
        title: "DESTINO",
        sortable: true,
      },
      {
        field: "accion",
        title: "PERMISO",
        sortable: true,
      },
      {
        field: "protocolo",
        title: "PROTOCOLO",
        sortable: true,
      },
      {
        field: "entrada",
        title: "ENTRADA/SALIDA",
        sortable: true,
      },
      {
        field: "ip",
        title: "ORIGEN",
        sortable: true,
      },
    ],
  });
});
