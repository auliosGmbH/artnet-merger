from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
import socket

class MdnsListener(ServiceListener):
    def __init__(self):
        self.services = []

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        ip = socket.inet_ntoa(info.addresses[0])
        self.services.append((name, ip))
        print(f"Service {name} added, service ip: {ip}")
