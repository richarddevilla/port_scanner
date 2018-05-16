import optparse
from socket import *
from threading import *
screenLock = Semaphore(value=1)

ports = {
            1:{'port': 20,'name': 'File Transfer Protocol (FTP)'},
            2:{'port': 21,'name': 'File Transfer Protocol (FTP)'},
            3:{'port': 22,'name': 'Secure Shell (SSH)'},
            4:{'port': 23,'name': 'Telnet'},
            5:{'port': 25,'name': 'Simple Mail Transfer Protocol (SMTP)'},
            6:{'port': 53,'name': 'Domain name Server (DNS)'},
            7:{'port': 80,'name': 'HyperText Transfer Protocol (HTTP)'},
            8:{'port': 110,'name': 'Post Office Protocol (POP3)'},
            9:{'port': 119,'name': 'Network News Transport Protocol (NNTP)'},
            10:{'port': 135,'name': 'NetBIOS'},
            11:{'port': 136,'name': 'NetBIOS'},
            12:{'port': 137,'name': 'NetBIOS'},
            13:{'port': 138,'name': 'NetBIOS'},
            14:{'port': 139,'name': 'NetBIOS'},
            15:{'port': 143,'name': 'Internet Message Access Protocol (IMAP4)'},
            16:{'port': 161,'name': 'Simple Network Management Protocol'},
            17:{'port': 162,'name': 'Simple Network Management Protocol'},
            18:{'port': 389,'name': 'Lightweight Directory Access Protocol'},
            19:{'port': 443,'name': 'HTTP with Secure Sockets Layer (SSL)'}
}


def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('Zzzzzzzzzzzzzzzzz')
        results = connSkt.recv(100)
        screenLock.acquire()
        print('[+]%d/tcp open'% tgtPort)
        print('[+] ' + str(results))
    except BaseException:
        screenLock.acquire()
        print('[-]%d/tcp closed'% tgtPort)
    finally:
        screenLock.release()
        connSkt.close()


def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host"%tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan Results for: ' + tgtName[0])
    except:
        print('\n[+] Scan Results for: ' + tgtIP)
        setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main():
    parser = optparse.OptionParser('usage%prog ' + \
                                   '-H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', \
                                    help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', \
                                    help='specify target port[s] separated by comma or \
                                     type "common" to scan all common ports')
    options, args = parser.parse_args()
    tgtHost = options.tgtHost
    if options.tgtPort == 'common':
        tgtPorts = []
        for key, values in ports.items():
            tgtPorts.append(values['port'])
    else:
        tgtPorts = options.tgtPort.split(',')

    if (tgtHost == None) | (tgtPorts[0] == None):
        print
        parser.usage
        exit(0)
    portScan(tgtHost, tgtPorts)

if __name__ == "__main__":
    main()


