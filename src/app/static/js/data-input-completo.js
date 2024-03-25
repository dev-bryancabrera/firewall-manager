// Datos para posteriores Usos
/* var selectFromTo = document.getElementById("selectFromTo"); */
/* var netmaskInput = document.getElementById("netmask"); */
/* var ipDestInput = document.getElementById("ipdest"); */
/* var maskdest = document.getElementById("maskdest"); */

/* Configuracion para habilitar o deshabilitar campos */
var selectRegla = document.getElementById("formSelectRegla");
var name_rule = document.getElementById("comment");
var ipAddrInput = document.getElementById("ipaddr");
var selectPortRange = document.getElementById("selectPortRange");
var port = document.getElementById("port");
var portStart = document.getElementById("portStart");
var portEnd = document.getElementById("portEnd");
var selectEntry = document.getElementById("selectEntry");
var selectProtocol = document.getElementById("selectProtocol");

var label = document.getElementById("puertos");
var labelEntrada = document.getElementById("puertoEntrada");
var labelSalida = document.getElementById("puertoSalida");
var btnSaveRule = document.getElementById("btnSave");

$(document).ready(function () {
  // Datos para posteriores usos
  /* netmaskInput.disabled = true; */
  /* ipDestInput.disabled = true; */
  /* selectFromTo.disabled = true; */
  /* maskdest.disabled = true; */

  // Deshabilitar los campos por defecto
  ipAddrInput.disabled = true;
  selectPortRange.disabled = true;
  portStart.disabled = true;
  portEnd.disabled = true;
  selectEntry.disabled = true;
  selectProtocol.disabled = true;
  port.disabled = true;

  selectRegla.addEventListener("change", function () {
    var selectedOption = selectRegla.value;
    if (selectedOption === "ip") {
      /* netmaskInput.disabled = false; */
      /* ipDestInput.disabled = false; */
      /* selectFromTo.disabled = false; */
      /* maskdest.disabled = false; */
      /* selectFromTo.selectedIndex = 0; */
      /* netmaskInput.value = ""; */
      /* ipDestInput.value = ""; */
      /* maskdest.value = ""; */

      ipAddrInput.disabled = false;
      selectPortRange.disabled = true;
      portStart.disabled = true;
      portEnd.disabled = true;
      selectEntry.disabled = false;
      selectProtocol.disabled = false;
      port.disabled = true;

      /* Limpiar Campos */
      selectPortRange.selectedIndex = 0;
      selectEntry.selectedIndex = 0;
      selectProtocol.selectedIndex = 0;

      ipAddrInput.value = "";
      port.value = "";
      portStart.value = "";
      portEnd.value = "";
      var options = selectEntry.options;
      for (var i = 0; i < options.length; i++) {
        if (options[i].value === "in") {
          options[i].disabled = false;
        }
      }
    } else if (selectedOption === "port") {
      ipAddrInput.disabled = true;
      /* netmaskInput.disabled = true; */
      /* ipDestInput.disabled = true; */
      /* selectFromTo.disabled = false; */
      /* maskdest.disabled = true; */
      /* selectFromTo.selectedIndex = 0; */
      /* netmaskInput.value = ""; */
      /* ipDestInput.value = ""; */
      /* maskdest.value = ""; */

      selectPortRange.disabled = false;
      portStart.disabled = true;
      portEnd.disabled = true;
      selectEntry.disabled = false;
      selectProtocol.disabled = false;
      port.disabled = false;

      /* Limpiar Campos */
      selectPortRange.selectedIndex = 0;
      selectEntry.selectedIndex = 0;
      selectProtocol.selectedIndex = 0;

      ipAddrInput.value = "";
      port.value = "";
      portStart.value = "";
      portEnd.value = "";

      label.textContent = "Rango de Puertos";
      labelEntrada.textContent = "Puerto Inicial";
      labelSalida.textContent = "Puerto Final";

      var options = selectEntry.options;
      for (var i = 0; i < options.length; i++) {
        if (options[i].value === "in") {
          options[i].disabled = true;
        }
      }
    } else if (selectedOption === "ipPort") {
      /* netmaskInput.disabled = false; */
      /*  ipDestInput.disabled = false; */
      /* selectFromTo.disabled = false; */
      /* maskdest.disabled = false; */
      /* selectFromTo.selectedIndex = 0; */
      /* netmaskInput.value = ""; */
      /* ipDestInput.value = ""; */
      /* maskdest.value = ""; */
      /* label.textContent = "Puertos de entrada y salida";
      labelEntrada.textContent = "Puerto Entrada";
      labelSalida.textContent = "Puerto Salida"; */

      ipAddrInput.disabled = false;
      selectPortRange.disabled = true;
      portStart.disabled = true;
      portEnd.disabled = true;
      selectEntry.disabled = false;
      selectProtocol.disabled = false;
      port.disabled = false;

      /* Limpiar Campos */
      selectPortRange.selectedIndex = 0;
      selectEntry.selectedIndex = 0;
      selectProtocol.selectedIndex = 0;

      ipAddrInput.value = "";
      port.value = "";
      portStart.value = "";
      portEnd.value = "";

      var options = selectEntry.options;
      for (var i = 0; i < options.length; i++) {
        if (options[i].value === "in") {
          options[i].disabled = false;
        }
      }
    } else {
      /* netmaskInput.disabled = true; */
      /* ipDestInput.disabled = true; */
      /* selectFromTo.disabled = true; */
      /* maskdest.disabled = true; */

      ipAddrInput.disabled = true;
      selectPortRange.disabled = true;
      portStart.disabled = true;
      portEnd.disabled = true;
      selectEntry.disabled = true;
      selectProtocol.disabled = true;
      port.disabled = true;
    }
  });
  selectPortRange.addEventListener("change", function () {
    var selectedPort = selectPortRange.value;
    var selectedOption = selectRegla.value;
    /* if (
      selectedPort === "yes" &&
      selectedOption === "port" && ipDestInput.disabled !== true
    ) {
      portStart.disabled = false;
      portEnd.disabled = false;
      port.disabled = true;
    } else */
    if (
      /* ipDestInput.disabled === true && */
      selectedPort === "yes" &&
      selectedOption !== "port"
    ) {
      portStart.disabled = false;
      portEnd.disabled = true;
      port.disabled = true;
    } else if (selectedPort === "yes" && selectedOption === "port") {
      portStart.disabled = false;
      portEnd.disabled = false;
      port.value = "";
      port.disabled = true;
      selectProtocol.selectedIndex = 0;
      var options = selectProtocol.options;
      for (var i = 0; i < options.length; i++) {
        if (options[i].value === "") {
          options[i].disabled = false;
        }
      }
    } else if (selectedPort === "no") {
      portStart.disabled = true;
      portEnd.disabled = true;
      port.disabled = false;

      portStart.value = "";
      portEnd.value = "";
      selectProtocol.selectedIndex = 0;
      var options = selectProtocol.options;
      for (var i = 0; i < options.length; i++) {
        if (options[i].value === "") {
          options[i].disabled = false;
        }
      }
    } else {
      portStart.disabled = true;
      portEnd.disabled = true;
      port.disabled = false;
    }
  });
  /* selectFromTo.addEventListener("change", function () {
    var selectedFrom = selectFromTo.value;
    var selectedPort = selectPortRange.value;
    var selectedOption = selectRegla.value;
    if (
      selectedFrom === "to" &&
      (selectedOption === "ipPort" || selectedOption === "ip")
    ) {
      ipDestInput.disabled = true;
      portEnd.disabled = true;
    } else if (
      selectedFrom === "from" &&
      selectedPort === "yes" &&
      (selectedOption === "ipPort" || selectedOption === "ip")
    ) {
      ipDestInput.disabled = false;
      portEnd.disabled = false;
    } else if (
      selectedFrom === "from" &&
      selectedPort !== "yes" &&
      (selectedOption === "ipPort" || selectedOption === "ip")
    ) {
      ipDestInput.disabled = false;
      portEnd.disabled = true;
    }
  }); */

  $("#formFirewall").submit(function (event) {
    event.preventDefault();

    if (
      validarSelect(selectRegla, "Seleccione que tipo de regla desea crear") ||
      mostrarAlerta(name_rule, "Se debe asignar un nombre a la Regla") ||
      mostrarAlerta(ipAddrInput, "El campo de dirección IP es requerido.") ||
      mostrarAlerta(port, "El campo de puerto es requerido.") ||
      mostrarAlerta(portStart, "El campo de puerto de inicio es requerido.") ||
      mostrarAlerta(portEnd, "El campo de puerto de fin es requerido.") ||
      mostrarAlerta(selectEntry, "El campo de entrada es requerido.") ||
      mostrarAlerta(selectProtocol, "El campo de protocolo es requerido.")
    ) {
      return;
    }

    var formData = $(this).serialize();
    btnSaveRule.disabled = true;

    $.ajax({
      type: "POST",
      url: "/add_rule",
      data: formData,
      success: function (response) {
        location.reload();
        console.log(response);
        console.log("se enviarion los datos");
      },
      error: function (xhr, status, error) {
        console.error(error);
      },
    });
  });

  function validarCampo(elemento) {
    return elemento.disabled == false && elemento.value.trim() === "";
  }

  function validarSelect(elemento, mensaje) {
    if (elemento.value.trim() === "") {
      $("#liveToast .toast-body").text(mensaje);
      // Muestra el toast
      $("#liveToast").toast("show");
      return true;
    }
    return false;
  }

  function mostrarAlerta(elemento, mensaje) {
    if (validarCampo(elemento)) {
      $("#liveToast .toast-body").text(mensaje);
      $("#liveToast").toast("show");
      return true;
    }
    return false;
  }
});

// Función para limpiar el formulario
function limpiarFormulario() {
  var formulario = document.getElementById("formFirewall");
  formulario.reset();

  ipAddrInput.disabled = true;
  selectPortRange.disabled = true;
  portStart.disabled = true;
  portEnd.disabled = true;
  selectEntry.disabled = true;
  selectProtocol.disabled = true;
  port.disabled = true;

  // Campos para posteriores usos
  /* netmaskInput.disabled = true; */
  /* ipDestInput.disabled = true; */
  /* selectFromTo.disabled = true; */
  /* maskdest.disabled = true; */
}

// Asociar la función limpiarFormulario al evento click del botón "Cancelar"
document
  .getElementById("btnCancelar")
  .addEventListener("click", limpiarFormulario);

document
  .getElementById("btncreate")
  .addEventListener("click", limpiarFormulario);
