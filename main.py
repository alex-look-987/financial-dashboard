import time, subprocess, sys, signal

def run_script(script_name, is_bokeh=False, bokeh_port=None, server_port=None, clientid=None, contract=None):
    """Ejecuta scripts Python y servidor Bokeh/dashboard"""
    if is_bokeh and bokeh_port:  # dashboard execution
        return subprocess.Popen([
            "bokeh", "serve", script_name,
            "--port", bokeh_port,
            f"--allow-websocket-origin=localhost:{bokeh_port}",
            "--show", "--args", contract
        ])
        
    elif server_port:
        return subprocess.Popen([
            sys.executable, script_name, server_port, clientid, contract
        ])
    else:
        return subprocess.Popen([sys.executable, script_name])

SERVER_PORT = "7496"

forex = {
    "EURUSD": [126, "5000", SERVER_PORT],
    # "GBPUSD": [124, "5101", SERVER_PORT]
}

if __name__ == "__main__":
    processes: list[subprocess.Popen] = []

    for contract, (clientid, bokeh_port, server_port) in forex.items():
        '''
        # IBAPI streaming data
        p_stream = run_script(
            "streaming_data.py",
            server_port=server_port,
            clientid=str(clientid),
            contract=contract)
        
        processes.append(p_stream)'''

        time.sleep(4) # time to get connected to API 
        
        # dashboard
        p_dash = run_script(
            "app.py",
            is_bokeh=True,
            bokeh_port=bokeh_port,
            contract=contract)
        
        processes.append(p_dash)

        print(f"Scripts para {contract} en ejecución...")

    def handler(sig, frame):
        print("\nTerminando procesos...")
        for p in processes:
            if p.poll() is None:  # if stills alive
                p.kill()
            
        sys.exit(0)

    # Capture Ctrl+C
    signal.signal(signal.SIGINT, handler)

    print("Presiona Ctrl+C para terminar todo.")

    try:
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        handler(None, None)
