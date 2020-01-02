import optparse
from socket import *
from threading import *


screen_lock = Semaphore(value=1)
def conn_scan(tgt_host, tgt_port):
    try:
        conn_skt = socket(AF_INET, SOCK_STREAM)
        conn_skt.connect((tgt_host,tgt_port))
        conn_skt.send('ViolentPython\r\n')
        results = conn_skt.recv(100)
        screen_lock.acquire()
        print(f'{tgt_port}/tcp open')
        print('Results: ',str(results))
        conn_skt.close()
    except Exception as e:
        screen_lock.acquire()
        print(str(e))
        print(f'{tgt_port}/tcp closed')
    finally:
        screen_lock.release()
        conn_skt.close()

def port_scan(tgt_host, tgt_ports):
    try:
        tgt_ip = gethostbyname(tgt_host)
    except Exception as e:
        print(str(e))
        print(f'Cannot resolve {tgt_host}: Unknown host')
    try:
        tgt_name = gethostbyaddr(tgt_ip)
        print(f'Scan results for: {tgt_name[0]}')
    except Exception as e:
        print(str(e))
        print(f'Scan results for: {tgt_ip}')
        setdefaulttimeout(1)
        for tgt_port in tgt_ports:
            t = Thread(target=conn_scan, args=(tgt_host, int(tgt_port)))
            t.start()

def main():
    parser = optparse.OptionParser(
        'usage%prog -H <target host> p <target port>')
    parser.add_option('-H', dest='tgt_host', type='string',help='specify target port')
    parser.add_option('-p', dest='tgt_port', type='string', help='specify target ports by coma')
    options, args = parser.parse_args()
    tgt_host = options.tgt_host
    tgt_ports = str(options.tgt_port).split(',')
    print(tgt_ports)
    if not tgt_host or not tgt_ports[0]:
        print(parser.usage)
        exit(0)
    port_scan(tgt_host,tgt_ports)

if __name__ == '__main__':
    main()
