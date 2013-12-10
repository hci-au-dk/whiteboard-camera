import socket
import fcntl
import struct

from util import printer

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


printer = printer.ThermalPrinter()
printer.print_text("Good Day!")
printer.linefeed()
printer.print_text("My ip address is:")
printer.linefeed()
printer.print_text(get_ip_address('eth0'))
printer.linefeed(3)
