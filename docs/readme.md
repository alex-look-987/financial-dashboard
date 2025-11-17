# financial_dashboard

---

Implementación de la funcionalidad de soporte de dashboards para más de 1 activo FOREX

Desde el archovio _main.py_ se establecerán cantidad y tipo de contrato.

Por ejemplo:

forex = {'EURUSD': [123, '5100', server_port], 'GBPUSD': [124, '5200', server_port]}

---

- key: nombre del contratio
- valor: [clientid, bokeh_port, server_port]
- clientid: número de conexión irrepetible para la TWS a través de la IBAPI
- bokeh_port: número de puerto único para el dashboard
- server_port: puerto de la TWS (constante ya definida)

---