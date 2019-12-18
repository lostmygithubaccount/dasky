def dashboard_url(ws, dashboard, ci_port):
    import socket, subprocess

    socat = subprocess.Popen(['/usr/bin/socat',
                              f'tcp-listen:{ci_port},resuseaddr,fork',
                              f'tcp:{dashboard}'],
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

    hostname = socket.gethostname
    region   = ws.get_details()['location']

    dashboard_url = 'https://{hostname}-{ci_port}.{region}.instances.azureml.net/status'

    return dashboard_url
