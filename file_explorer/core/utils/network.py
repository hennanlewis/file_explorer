import socket
import logging

logger = logging.getLogger(__name__)

def get_host_ips():
    ips = {"127.0.0.1", "localhost", "::1"}
    try:
        hostname = socket.gethostname()
        ips.add(hostname)
        results = socket.getaddrinfo(hostname, None, socket.AF_INET)
        for result in results:
            ip = result[4][0]
            if ip and ip not in ips:
                ips.add(ip)
                logger.debug(f"IP local detectado: {ip}")
    except Exception as e:
        logger.warning(f"Detecção de IPs limitada: {e}")

    logger.info(f"IPs para acesso local: {list(ips)}")
    return ips

def is_host_request(req):
    client_ip = req.remote_addr
    host_ips = get_host_ips()
    is_host = client_ip in host_ips
    if is_host:
        logger.debug(f"Acesso local de: {client_ip}")
    else:
        logger.info(f"Acesso remoto de: {client_ip}")
    return is_host
