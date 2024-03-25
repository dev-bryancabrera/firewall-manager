$(document).ready(function () {
  preLoadData();

  /* Manejo de entrada de datos */
  var filterIp = document.getElementById("selectFilterIp");
  var filterMac = document.getElementById("selectFilterMac");
  var filterPort = document.getElementById("selectFilterPort");
  var filterProtocolRed = document.getElementById("selectFilterProtocolRed");

  var ipAddr = document.getElementById("ipaddr");
  var macAddr = document.getElementById("macaddr");
  var portSrc = document.getElementById("portSrc");
  var protocolRedSrc = document.getElementById("protocolRedSrc");
  var ipDest = document.getElementById("ipdest");
  var macDest = document.getElementById("macdest");
  var portDst = document.getElementById("portDst");
  var protocolRedDst = document.getElementById("protocolRedDst");

  var generalip = document.getElementById("generalip");
  var generalport = document.getElementById("generalport");
  var generalProtocolRed = document.getElementById("generalProtocolRed");

  /* Bloque de Entradas */
  var generalIpContainer = document.getElementById("generalIpContainer");
  var generalPortContainer = document.getElementById("generalPortContainer");
  var generalProtocolRedContainer = document.getElementById(
    "generalProtocolRedContainer"
  );

  var ipSrcContainer = document.getElementById("ipAddrContainer");
  var ipDstContainer = document.getElementById("ipDstContainer");

  var macSrcContainer = document.getElementById("macSrcContainer");
  var macDstContainer = document.getElementById("macDstContainer");

  var portSrcContainer = document.getElementById("portSrcContainer");
  var portDstContainer = document.getElementById("portDstContainer");

  var protocolRedSrcContainer = document.getElementById(
    "protocolRedSrcContainer"
  );
  var protocolRedDstContainer = document.getElementById(
    "protocolRedDstContainer"
  );

  /* Dialog */
  var modalDialog = document.getElementById("modal-dialog");

  /* Comparadores */
  var filterOperatorIp = document.getElementById("filterOperatorIp");
  var filterOperatorMac = document.getElementById("filterOperatorMac");
  var filterOperatorPort = document.getElementById("filterOperatorPort");
  var filterOperatorProtoRed = document.getElementById(
    "filterOperatorProtoRed"
  );

  /* Comparadores Entre Bloques */
  var filterOperatorMacPort = document.getElementById("filterOperatorMacPort");
  var filterOperatorProtoRedProto = document.getElementById(
    "filterOperatorProtoRedProto"
  );

  /* Comparadores */
  var logicOperatorMacPort = document.getElementById("logicOperatorMacPort");
  var logicOperatorProtoRedProto = document.getElementById(
    "logicOperatorProtoRedProto"
  );

  var logicOperatorIp = document.getElementById("logicOperatorIp");
  var logicOperatorMac = document.getElementById("logicOperatorMac");
  var logicOperatorPort = document.getElementById("logicOperatorPort");
  var logicOperatorProtoRed = document.getElementById("logicOperatorProtoRed");

  /* Ocultar Elementos de la vista principal */

  generalIpContainer.style.display = "none";
  generalPortContainer.style.display = "none";
  generalProtocolRedContainer.style.display = "none";

  filterOperatorIp.style.display = "none";
  filterOperatorMac.style.display = "none";
  filterOperatorPort.style.display = "none";
  filterOperatorProtoRed.style.display = "none";

  filterOperatorMacPort.style.display = "none";
  filterOperatorProtoRedProto.style.display = "none";

  generalip.disabled = true;
  generalport.disabled = true;
  generalProtocolRed.disabled = true;
  ipAddr.disabled = true;
  macAddr.disabled = true;
  portSrc.disabled = true;
  protocolRedSrc.disabled = true;
  ipDest.disabled = true;
  macDest.disabled = true;
  portDst.disabled = true;
  protocolRedDst.disabled = true;

  function validaModal() {
    if (
      filterOperatorIp.style.display === "none" &&
      filterOperatorMac.style.display === "none" &&
      filterOperatorPort.style.display === "none" &&
      filterOperatorProtoRed.style.display === "none"
    ) {
      modalDialog.style.setProperty("max-width", "925px", "important");
    } else {
      modalDialog.style.setProperty("max-width", "1125px", "important");
    }
  }

  /* Verifica el cambio que se hace con el select */
  filterIp.addEventListener("change", function () {
    var selecteFilterIp = filterIp.value;
    if (selecteFilterIp === "ipSrc") {
      generalip.value = "";
      ipDest.value = "";
      $("#generalip").tagsinput("removeAll");
      $("#ipdest").tagsinput("removeAll");
      ipAddr.disabled = false;
      ipDest.disabled = true;
      generalip.disabled = true;
      logicOperatorIp.selectedIndex = 0;

      generalIpContainer.style.display = "none";
      filterOperatorIp.style.display = "none";
      ipSrcContainer.style.display = "block";
      ipDstContainer.style.display = "none";
      validaModal();
    } else if (selecteFilterIp === "ipDst") {
      generalip.value = "";
      ipAddr.value = "";
      $("#generalip").tagsinput("removeAll");
      $("#ipaddr").tagsinput("removeAll");
      logicOperatorIp.selectedIndex = 0;
      generalip.disabled = true;
      ipAddr.disabled = true;
      ipDest.disabled = false;

      generalIpContainer.style.display = "none";
      filterOperatorIp.style.display = "none";
      ipSrcContainer.style.display = "none";
      ipDstContainer.style.display = "block";
      validaModal();
    } else if (selecteFilterIp === "ipSrcDst") {
      generalip.value = "";
      $("#generalip").tagsinput("removeAll");
      generalip.disabled = true;
      ipAddr.disabled = false;
      ipDest.disabled = false;

      generalIpContainer.style.display = "none";
      filterOperatorIp.style.display = "block";
      ipDstContainer.style.display = "block";
      ipSrcContainer.style.display = "block";

      validaModal();
    } else if (selecteFilterIp === "ipGeneral") {
      ipDest.value = "";
      ipAddr.value = "";
      $("#ipdest").tagsinput("removeAll");
      $("#ipaddr").tagsinput("removeAll");
      logicOperatorIp.selectedIndex = 0;
      generalip.disabled = false;
      ipAddr.disabled = true;
      ipDest.disabled = true;

      filterOperatorIp.style.display = "none";
      generalIpContainer.style.display = "block";
      ipSrcContainer.style.display = "none";
      ipDstContainer.style.display = "none";
      validaModal();
    }
  });

  filterMac.addEventListener("change", function () {
    var selecteFilterMac = filterMac.value;
    if (selecteFilterMac === "macSrc") {
      macDest.value = "";
      $("#macdest").tagsinput("removeAll");
      macAddr.disabled = false;
      macDest.disabled = true;
      logicOperatorMac.selectedIndex = 0;

      filterOperatorMac.style.display = "none";
      macSrcContainer.style.display = "block";
      macDstContainer.style.display = "none";
      validaModal();
    } else if (selecteFilterMac === "macDst") {
      macAddr.value = "";
      $("#macaddr").tagsinput("removeAll");
      logicOperatorMac.selectedIndex = 0;
      macAddr.disabled = true;
      macDest.disabled = false;

      filterOperatorMac.style.display = "none";
      macSrcContainer.style.display = "none";
      macDstContainer.style.display = "block";
      validaModal();
    } else if (selecteFilterMac === "macSrcDst") {
      macAddr.disabled = false;
      macDest.disabled = false;

      filterOperatorMac.style.display = "block";
      macSrcContainer.style.display = "block";
      macDstContainer.style.display = "block";
      validaModal();
    }
  });

  filterPort.addEventListener("change", function () {
    var selecteFilterPort = filterPort.value;
    if (selecteFilterPort === "portSrc") {
      generalport.value = "";
      portDst.value = "";
      $("#generalport").tagsinput("removeAll");
      $("#portDst").tagsinput("removeAll");
      logicOperatorPort.selectedIndex = 0;
      generalport.disabled = true;
      portSrc.disabled = false;
      portDst.disabled = true;

      generalPortContainer.style.display = "none";
      filterOperatorPort.style.display = "none";
      portSrcContainer.style.display = "block";
      portDstContainer.style.display = "none";
      validaModal();
    } else if (selecteFilterPort === "portDst") {
      generalport.value = "";
      portSrc.value = "";
      $("#generalport").tagsinput("removeAll");
      $("#portSrc").tagsinput("removeAll");
      logicOperatorPort.selectedIndex = 0;
      generalport.disabled = true;
      portSrc.disabled = true;
      portDst.disabled = false;

      generalPortContainer.style.display = "none";
      filterOperatorPort.style.display = "none";
      portSrcContainer.style.display = "none";
      portDstContainer.style.display = "block";
      validaModal();
    } else if (selecteFilterPort === "portSrcDst") {
      generalport.value = "";
      $("#generalport").tagsinput("removeAll");
      generalport.disabled = true;
      portSrc.disabled = false;
      portDst.disabled = false;

      generalPortContainer.style.display = "none";
      filterOperatorPort.style.display = "block";
      portSrcContainer.style.display = "block";
      portDstContainer.style.display = "block";
      validaModal();
    } else if (selecteFilterPort === "portGeneral") {
      portSrc.value = "";
      portDst.value = "";
      $("#portSrc").tagsinput("removeAll");
      $("#portDst").tagsinput("removeAll");
      logicOperatorPort.selectedIndex = 0;
      generalport.disabled = false;
      portSrc.disabled = true;
      portDst.disabled = true;

      generalPortContainer.style.display = "block";
      filterOperatorPort.style.display = "none";
      portSrcContainer.style.display = "none";
      portDstContainer.style.display = "none";
      validaModal();
    }
  });

  filterProtocolRed.addEventListener("change", function () {
    var selecteFilterProtocolRed = filterProtocolRed.value;
    var protocolResetRedSrc = $("#protocolRedSrc");
    var protocolResetRedDst = $("#protocolRedDst");
    var protocolResetGeneral = $("#generalProtocolRed");

    if (selecteFilterProtocolRed === "protocolRedSrc") {
      logicOperatorProtoRed.selectedIndex = 0;
      generalProtocolRedContainer.style.width = "none";
      filterOperatorProtoRed.style.display = "none";
      protocolRedSrcContainer.style.display = "block";
      protocolRedDstContainer.style.display = "none";
      generalProtocolRed.disabled = true;
      protocolRedSrc.disabled = false;
      protocolRedDst.disabled = true;

      protocolResetRedDst.val([]);
      protocolResetGeneral.val([]);
      protocolResetGeneral.selectpicker("refresh");
      protocolResetRedSrc.selectpicker("refresh");
      protocolResetRedDst.selectpicker("refresh");
      validaModal();
    } else if (selecteFilterProtocolRed === "protocolRedDst") {
      logicOperatorProtoRed.selectedIndex = 0;
      generalProtocolRedContainer.style.width = "none";
      filterOperatorProtoRed.style.display = "none";
      protocolRedSrcContainer.style.display = "none";
      protocolRedDstContainer.style.display = "block";
      generalProtocolRed.disabled = true;
      protocolRedSrc.disabled = true;
      protocolRedDst.disabled = false;

      protocolResetRedSrc.val([]);
      protocolResetGeneral.val([]);
      protocolResetGeneral.selectpicker("refresh");
      protocolResetRedSrc.selectpicker("refresh");
      protocolResetRedDst.selectpicker("refresh");
      validaModal();
    } else if (selecteFilterProtocolRed === "protocolRedSrcDst") {
      generalProtocolRedContainer.style.width = "none";
      filterOperatorProtoRed.style.display = "block";
      protocolRedSrcContainer.style.display = "block";
      protocolRedDstContainer.style.display = "block";
      generalProtocolRed.disabled = true;
      protocolRedSrc.disabled = false;
      protocolRedDst.disabled = false;

      protocolResetRedSrc.val([]);
      protocolResetRedDst.val([]);
      protocolResetGeneral.val([]);
      protocolResetGeneral.selectpicker("refresh");
      protocolResetRedSrc.selectpicker("refresh");
      protocolResetRedDst.selectpicker("refresh");
      validaModal();
    } else if (selecteFilterProtocolRed === "protocolRedGeneral") {
      logicOperatorProtoRed.selectedIndex = 0;
      generalProtocolRedContainer.style.display = "block";
      filterOperatorProtoRed.style.display = "none";
      protocolRedSrcContainer.style.display = "none";
      protocolRedDstContainer.style.display = "none";
      generalProtocolRed.disabled = false;
      protocolRedSrc.disabled = true;
      protocolRedDst.disabled = true;

      protocolResetRedSrc.val([]);
      protocolResetRedDst.val([]);
      protocolResetRedSrc.selectpicker("refresh");
      protocolResetRedDst.selectpicker("refresh");
      protocolResetGeneral.selectpicker("refresh");
      validaModal();
    }
  });

  /* Verifica Entrada de Texto en el Input */
  $(".ips").on("input change keypress", function () {
    if (
      ipAddr.value.trim() !== "" ||
      ipDest.value.trim() !== "" ||
      generalip.value.trim() !== "" ||
      macAddr.value.trim() !== "" ||
      macDest.value.trim() !== ""
    ) {
      filterOperatorMacPort.style.display = "block";
    } else {
      logicOperatorMacPort.selectedIndex = 0;
      filterOperatorMacPort.style.display = "none";
    }
  });

  $(".ports").on("input change keypress", function (e) {
    if (
      portSrc.value.trim() !== "" ||
      portDst.value.trim() !== "" ||
      generalport.value.trim() !== "" ||
      protocolRedSrc.value.trim() !== "" ||
      protocolRedDst.value.trim() !== "" ||
      generalProtocolRed.value.trim() !== ""
    ) {
      filterOperatorProtoRedProto.style.display = "block";
    } else {
      logicOperatorProtoRedProto.selectedIndex = 0;
      filterOperatorProtoRedProto.style.display = "none";
    }
  });

  $(".multiple-input").tagsinput({
    trimValue: true,
    confirmKeys: [13, 44, 32],
    focusClass: "my-focus-class",
  });

  $(".bootstrap-tagsinput input")
    .on("focus", function () {
      $(this).closest(".bootstrap-tagsinput").addClass("has-focus");
    })
    .on("blur", function () {
      $(this).closest(".bootstrap-tagsinput").removeClass("has-focus");
    });

  var $packetTable = $("#packetTable");

  $packetTable.bootstrapTable({
    showColumns: true,
    showExport: true,
    exportTypes: ["json", "xml", "txt", "excel", "pdf"],
    locale: "es-ES",
    columns: [
      {
        field: "time",
        title: "Marca de tiempo",
        sortable: true,
      },
      {
        field: "src_ip",
        title: "Dirección IP de origen",
        sortable: true,
      },
      {
        field: "src_port",
        title: "Puerto de origen",
        sortable: true,
      },
      {
        field: "dst_ip",
        title: "Dirección IP de destino",
        sortable: true,
      },
      {
        field: "dst_port",
        title: "Puerto de destino",
        sortable: true,
      },
      {
        field: "protocol",
        title: "Protocolo",
        sortable: true,
      },
      {
        field: "info",
        title: "Informacion de Captura",
        sortable: true,
      },
    ],
  });

  $("#formPacket").submit(function (event) {
    // Evita que el formulario se envíe normalmente
    event.preventDefault();

    if (
      mostrarAlerta(ipAddr, "El campo de dirección IP es requerido.") ||
      mostrarAlerta(macAddr, "El campo de dirección MAC es requerido.") ||
      mostrarAlerta(portSrc, "El campo de puerto de origen es requerido.") ||
      mostrarAlerta(
        protocolRedSrc,
        "El campo de protocolo de red de origen es requerido."
      ) ||
      mostrarAlerta(
        ipDest,
        "El campo de dirección IP de destino es requerido."
      ) ||
      mostrarAlerta(
        macDest,
        "El campo de dirección MAC de destino es requerido."
      ) ||
      mostrarAlerta(portDst, "El campo de puerto de destino es requerido.") ||
      mostrarAlerta(
        protocolRedDst,
        "El campo de protocolo de red de destino es requerido."
      ) ||
      mostrarAlerta(
        generalip,
        "El campo de dirección IP general es requerido."
      ) ||
      mostrarAlerta(generalport, "El campo de puerto general es requerido.") ||
      mostrarAlerta(
        generalProtocolRed,
        "El campo de protocolo de red general es requerido."
      )
    ) {
      return; // Detiene el envío del formulario si la validación falla
    }

    var formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: "/packetdata",
      data: formData,
      success: function (response) {
        console.log(response);
        console.log("se enviarion los datos");
        loadData();
      },
      error: function (xhr, status, error) {
        console.error(error);
      },
    });
  });

  function validarCampo(elemento) {
    return elemento.disabled == false && elemento.value.trim() === "";
  }

  function mostrarAlerta(elemento, mensaje) {
    if (validarCampo(elemento)) {
      $("#liveToast .toast-body").text(mensaje);
      // Muestra el toast
      $("#liveToast").toast("show");
      return true;
    }
    return false;
  }

  var pageLoaded = false;

  function preLoadData() {
    if (!pageLoaded) {
      pageLoaded = true;
      console.log("Cargando datos por primera vez...");
      const eventSource = new EventSource("/pre_start_capture");

      eventSource.onmessage = function (event) {
        const packetData = event.data;

        const packetInfo = packetData.split(" ");
        const time = packetInfo[0] + " " + packetInfo[1];
        const src_ip = packetInfo[2].split(":")[0];
        const src_port = packetInfo[2].split(":")[1];
        const dst_ip = packetInfo[4].split(":")[0];
        const dst_port = packetInfo[4].split(":")[1];
        const protocol = packetInfo[5];
        const info = packetInfo.slice(6).join(" ");

        const row = {
          time: time,
          src_ip: src_ip,
          src_port: src_port,
          dst_ip: dst_ip,
          dst_port: dst_port,
          protocol: protocol,
          info: info,
        };

        // Agregar la fila a la tabla usando bootstrapTable
        $("#packetTable").bootstrapTable("append", row);
      };
    }
  }

  // Cargar los datos en la tabla
  function loadData() {
    resetData();
    const eventSource = new EventSource("/packetdata");

    eventSource.onmessage = function (event) {
      const packetData = event.data;

      const packetInfo = packetData.split(" ");
      const time = packetInfo[0] + " " + packetInfo[1];
      const src_ip = packetInfo[2].split(":")[0];
      const src_port = packetInfo[2].split(":")[1];
      const dst_ip = packetInfo[4].split(":")[0];
      const dst_port = packetInfo[4].split(":")[1];
      const protocol = packetInfo[5];
      const info = packetInfo.slice(6).join(" ");

      const row = {
        time: time,
        src_ip: src_ip,
        src_port: src_port,
        dst_ip: dst_ip,
        dst_port: dst_port,
        protocol: protocol,
        info: info,
      };

      // Agregar la fila a la tabla usando bootstrapTable
      $("#packetTable").bootstrapTable("append", row);
    };
  }

  function togglePlayPause() {
    var isPaused = $("#pause-icon").is(":visible");

    // Cambiar el ícono del botón según si se pausa o se reanuda la captura
    if (isPaused) {
      $("#play-icon").show();
      $("#pause-icon").hide();
    } else {
      $("#play-icon").hide();
      $("#pause-icon").show();
    }

    // Enviar una solicitud POST al servidor de Flask indicando si se pausa o se reanuda la captura
    $.ajax({
      type: "POST",
      url: "/toggle-play-pause",
      data: {
        isPaused: isPaused,
      },
      success: function (response) {
        console.log(response);
      },
      error: function (xhr, status, error) {
        console.error(error);
      },
    });
  }
});

async function resetData() {
  var $packetTable = $("#packetTable");
  $packetTable.bootstrapTable("removeAll");
}

document.getElementById("btn-clean").addEventListener("click", resetData());
