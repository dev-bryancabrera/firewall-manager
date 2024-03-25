$(".editarReglaBtn").click(function () {
  var selectFromTo = document.querySelectorAll("#editFromTo");
  selectFromTo.forEach((fromto) => {
    fromto.disabled = true;
    fromto.setAttribute("value", "");
  });

  var ipAddrInput = document.querySelectorAll("#editaripaddr");
  ipAddrInput.forEach((ipaddr) => {
    ipaddr.disabled = true;
    ipaddr.setAttribute("value", "");
  });

  var netmaskInput = document.querySelectorAll("#editNetmask");
  netmaskInput.forEach((netmask) => {
    netmask.disabled = true;
    netmask.setAttribute("value", "");
  });

  /*  var ipDestInput = document.querySelectorAll("#editaripdest");
  ipDestInput.forEach((ipdest) => {
    ipdest.disabled = true;
    ipdest.setAttribute("value", "");
  }); */

  var maskdest = document.querySelectorAll("#editMaskdest");
  maskdest.forEach((netmask) => {
    netmask.disabled = true;
    netmask.setAttribute("value", "");
  });

  var selectPortRange = document.querySelectorAll("#editPortRange");
  selectPortRange.forEach((portRange) => {
    portRange.disabled = true;
  });

  var port = document.querySelectorAll("#editport");
  port.forEach((port) => {
    port.disabled = true;
    port.setAttribute("value", "");
  });

  var portStart = document.querySelectorAll("#editportStart");
  portStart.forEach((portstart) => {
    portstart.disabled = true;
    portstart.setAttribute("value", "");
  });

  var portEnd = document.querySelectorAll("#editportLimit");
  portEnd.forEach((portend) => {
    portend.disabled = true;
    portend.setAttribute("value", "");
  });

  var selectEntry = document.querySelectorAll("#editEntry");
  selectEntry.forEach((entry) => {
    entry.disabled = true;
  });

  var selectProtocol = document.querySelectorAll("#editProtocol");
  selectProtocol.forEach((protocol) => {
    protocol.disabled = true;
  });

  var fila = $(this).closest("tr");

  var direccion = fila.find(".direccion").text();
  direccion = direccion.replace(/\s*\(\s*v6\s*\)\s*/gi, ""); // Elimina "(v6)" con espacios opcionales alrededor
  var protocolo = fila.find(".protocolo").text();
  var entrada = fila.find(".entrada").text();
  var ip = fila.find(".ip").text();
  ip = ip.replace(/\s*\(\s*v6\s*\)\s*/gi, "");

  /* Direccion de inicio */
  if (direccion.includes(":")) {
    var splitdireccion = direccion.split(":");
    var ip_dest = splitdireccion[0];
    var port_End = splitdireccion[1];

    if (/^\d+\.\d+\.\d+\.\d+$/.test(ip_dest)) {
      /* ipDestInput.forEach((ipdest) => {
        ipdest.setAttribute("value", ip_dest);
      }); */
    } else {
      portStart.forEach((portstart) => {
        portstart.setAttribute("value", ip_dest);
      });
    }

    portEnd.forEach((portend) => {
      portend.setAttribute("value", port_End);
    });

    selectFromTo.forEach((fromto) => {
      direccion_regla = "Destino";
      fromto.setAttribute("value", direccion_regla);
    });

    selectPortRange.forEach((portrange) => {
      portrange.value = "yes";
      portrange.dispatchEvent(new Event("change"));
    });
  } else if (/^\d+\.\d+\.\d+\.\d+$/.test(direccion)) {
    /* ipDestInput.forEach((ipdest) => {
      ipdest.setAttribute("value", direccion);
    }); */
    selectFromTo.forEach((fromto) => {
      direccion_regla = "Destino";
      fromto.setAttribute("value", direccion_regla);
    });
  } else if (direccion === "Anywhere") {
    direccion = "";
    selectFromTo.forEach((fromto) => {
      direccion_regla = "Origen";
      fromto.setAttribute("value", direccion_regla);
    });
  } else if (
    !/^\d+\.\d+\.\d+\.\d+$/.test(ip) &&
    !ip.includes(":") &&
    ip !== "Anywhere"
  ) {
    portEnd.forEach((portend) => {
      portend.setAttribute("value", direccion);
    });
    selectFromTo.forEach((fromto) => {
      direccion_regla = "Origen";
      fromto.setAttribute("value", direccion_regla);
    });
    selectPortRange.forEach((portrange) => {
      portrange.value = "yes";
      portrange.dispatchEvent(new Event("change"));
    });
  } else {
    port.forEach((port) => {
      port.setAttribute("value", direccion);
    });
    if (ip !== "Anywhere") {
      selectFromTo.forEach((fromto) => {
        direccion_regla = "Origen";
        fromto.setAttribute("value", direccion_regla);
      });
    } else {
      selectFromTo.forEach((fromto) => {
        direccion_regla = "Destino";
        fromto.setAttribute("value", direccion_regla);
      });
    }

    selectPortRange.forEach((portrange) => {
      portrange.value = "no";
      portrange.dispatchEvent(new Event("change"));
    });
  }

  /* Direccion de Final */
  if (ip.includes(":")) {
    var splitip = ip.split(":");

    var ip_add = splitip[0];
    var port_Start = splitip[1];

    if (/^\d+\.\d+\.\d+\.\d+$/.test(ip_add)) {
      ipAddrInput.forEach((ipadd) => {
        ipadd.setAttribute("value", ip_add);
      });
      portStart.forEach((portstart) => {
        portstart.setAttribute("value", port_Start);
      });
    } else if (
      !/^\d+\.\d+\.\d+\.\d+$/.test(ip_add) &&
      !/^\d+\.\d+\.\d+\.\d+$/.test(port_Start)
    ) {
      portStart.forEach((portstart) => {
        portstart.setAttribute("value", ip_add);
      });
      portEnd.forEach((portend) => {
        portend.setAttribute("value", port_Start);
      });
    }
  } else if (/^\d+\.\d+\.\d+\.\d+$/.test(ip)) {
    ipAddrInput.forEach((ipaddr) => {
      ipaddr.setAttribute("value", ip);
    });
  } else if (ip === "Anywhere") {
    ip = "";
  } else {
    portStart.forEach((portstart) => {
      portstart.setAttribute("value", ip);
    });
  }

  if (protocolo === "TCP") {
    protocolo = "tcp";
    selectProtocol.forEach((protocol) => {
      protocol.value = protocolo;
      protocol.dispatchEvent(new Event("change")); // Disparar el evento change
    });
  } else if (protocolo === "UDP") {
    protocolo = "udp";
    selectProtocol.forEach((protocol) => {
      protocol.value = protocolo;
      protocol.dispatchEvent(new Event("change"));
    });
  } else if (protocolo === "TCP/UDP") {
    selectProtocol.forEach((protocol) => {
      if (protocolo === "TCP/UDP") {
        Array.from(protocol.options).forEach((option) => {
          if (option.value === "") {
            option.selected = true;
          } else {
            option.selected = false;
          }
        });
      } else {
        protocol.value = protocolo;
      }
      protocol.dispatchEvent(new Event("change"));
    });
  }

  if (entrada === "SALIDA") {
    entrada = "out";
    selectEntry.forEach((entry) => {
      entry.value = entrada;
      entry.dispatchEvent(new Event("change"));
    });
  } else if (entrada === "ENTRADA") {
    entrada = "in";
    selectEntry.forEach((entry) => {
      entry.value = entrada;
      entry.dispatchEvent(new Event("change"));
    });
  }
});
