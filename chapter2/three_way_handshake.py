from time import strftime
from datetime import datetime
import sys
from scapy.all import *
import optparse
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)  # noqa

'''The TCP Three-Way Handshake:
ref: https://null-byte.wonderhowto.com/how-to/build-stealth-port-scanner-with-scapy-and-python-0164779/
A three-way handshake take splace between the server and the client when establishing a connections with TCP.
The three TCP packet of relevance today are SYN (Synchronize), ACK (Aknowledgment) and RST (Reset).
'''


def scan_port(port):
    src_port = RandShort()  # Generates a small random number to use as a port
    conf.verb = 0  # This prevents output from sending packets from being printed on the screen
    # Craft out SYN packet, SYNACK_pkt holds the values of our recived packet
    SYNACK_pkt = sr1(
        IP(dst=target)/TCP(sport=src_port, dport=port, flags="S"))
    # Extract flagas fro out received packet
    pkt_flags = SYNACK_pkt.getlayer(TCP).flags
    if pkt_flags == SYNACK:
        return True
    else:
        return False
    # Craft RST packet, we dont use sr1(), instead we use the send() function,
    # this is because we dont expect a response
    RST_pkt = IP(dst=target)/TCP(sport=src_port, dport=port, flags="R")
    send(RST_pkt)


def check_host(ip):
    # Craft a ping packet and sends it to the target
    conf.verb = 0
    try:
        ping = sr1(IP(dst=ip)/ICMPT())
        print(f'Target is up, Beggining scann... [{ping}]')
    except Exception:
        print('Couldnt resolve target,\n', 'exiting...')
        sys.exit(1)


def main():
    parser = optparse.OptionParser(
        'usage%prog -H <target host> -minp <minimum ports> -maxp <maximum ports>'
    )
    parser.add_option('-H', dest='tgt_host', type='string', help='specify target host')
    parser.add_option('-minp', dest='min_ports', type='int', help='Specify min number of ports')
    parser.add_option('-minp', dest='max_ports', type='int', help='Specify max number of ports')
    options, args = parser.parse_args()

    tgt_host = options.tgt_host
    min_ports = options.min_ports
    max_ports = options.max_ports
    ports = range(min_ports, max_ports+1)

    try:
        if min_ports and max_ports and max_ports >= min_ports:
            pass
        else:
            print('Invalid range of ports,\n',
                  'Exiting... !')
            sys.exit(1)
    except KeyboardInterrupt:
        print('User requested shutdown...\n', 'Exiting...!')
        sys.exit(1)
    check_host(tgt_host)
    print(f'Scanning Started at {strftime("%H:%M:%S")} !\n')
    for port in ports:
        status = scan_port(port)
        if status:
            print(f'Port {str(port)}: Open')
    stop_clock = datetime.now()
    total_time = stop_clock - start_clock
    print('Scan Finished,\n',
          f'Total scan duration: {str(total_time)}')


if __name__ == '__main__':
    start_clock = datetime.now()
    SYNACK = 0x12
    RSTACK = 0x14
    main()
