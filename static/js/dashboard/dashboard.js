document.addEventListener("DOMContentLoaded", () => {
  "use strict";

  // URL del backend obtenida del motor de plantillas de Django.
  const apiUrlTemplate = Obtener_Api_ventas;

  // Inicializar las variables para el contexto y la instancia de la gráfica
  const ctx = document.getElementById("myChart");
  let myChart;
  let selectedYear;

  // Configurar el input de tipo 'number' para el año
  const yearFilter = document.getElementById("yearFilter");
  const currentYear = new Date().getFullYear();
  yearFilter.value = currentYear;
  selectedYear = currentYear;

  // Escuchar cambios en el selector de año
  yearFilter.addEventListener("change", (e) => {
    selectedYear = parseInt(e.target.value);
    // Validar que el año es un número válido
    if (
      !isNaN(selectedYear) &&
      selectedYear >= 2020 &&
      selectedYear <= currentYear
    ) {
      updateChart(selectedYear);
    } else {
      console.error(
        "Año no válido. Por favor, ingrese un año entre 2020 y el año actual."
      );
    }
  });

  // Función que realiza la llamada real al backend
  const getVentasData = async (year) => {
    // Se construye la URL usando el año seleccionado
    const url = apiUrlTemplate.replace("0", year);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error al obtener los datos de ventas:", error);
      // Si la llamada falla, devuelve datos vacíos para no romper la gráfica
      return {
        labels: [],
        chipsVendidos: [],
        montoTotal: [],
      };
    }
  };

  // Función para renderizar o actualizar la gráfica con nuevos datos
  const updateChart = async (year) => {
    try {
      // Obtener los datos del backend para el año seleccionado
      const data = await getVentasData(year);

      const meses = [
        "Ene",
        "Feb",
        "Mar",
        "Abr",
        "May",
        "Jun",
        "Jul",
        "Ago",
        "Sep",
        "Oct",
        "Nov",
        "Dic",
      ];
      const datasets = [
        {
          label: "Chips Vendidos",
          data: data.chipsVendidos,
          backgroundColor: "transparent",
          borderColor: "#3187e2ff",
          borderWidth: 4,
          pointBackgroundColor: "#3187e2ff",
          lineTension: 0,
          yAxisID: "y",
        },
        {
          label: "Monto Total",
          data: data.montoTotal,
          backgroundColor: "transparent",
          borderColor: "#28a745",
          borderWidth: 4,
          pointBackgroundColor: "#28a745",
          lineTension: 0,
          yAxisID: "y1",
        },
      ];

      // Si la gráfica ya existe, la actualizamos
      if (myChart) {
        myChart.data.labels = meses;
        myChart.data.datasets = datasets;
        myChart.update();
      } else {
        // Si no existe, la creamos
        myChart = new Chart(ctx, {
          type: "line", // Cambiado a 'line' para un gráfico de líneas
          data: {
            labels: meses,
            datasets: datasets,
          },
          options: {
            responsive: true,
            scales: {
              y: {
                type: "linear",
                display: true,
                position: "left",
                title: {
                  display: true,
                  text: "Chips Vendidos",
                },
              },
              y1: {
                type: "linear",
                display: true,
                position: "right",
                grid: {
                  drawOnChartArea: false,
                },
                title: {
                  display: true,
                  text: "Monto Total Recaudado",
                },
              },
            },
            plugins: {
              legend: {
                display: true,
                position: "top",
              },
              tooltip: {
                mode: "index",
                intersect: false,
              },
            },
          },
        });
      }
    } catch (error) {
      console.error("Error al renderizar la gráfica:", error);
    }
  };

  // Cargar la gráfica con los datos del año actual al iniciar la página
  updateChart(selectedYear);
});
