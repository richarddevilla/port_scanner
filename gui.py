from tkinter import ttk, Tk, StringVar, messagebox
from socket import *
from threading import *

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

def main():
    root = Tk()
    host_var = StringVar()
    port_var = StringVar()
    host_label = ttk.Label(root,text='Host Name or IP')
    host_entry = ttk.Entry(root,textvariable=host_var)
    port_label = ttk.Label(root,text='Port Number')
    port_entry = ttk.Entry(root, textvariable=port_var)
    result_tree = ttk.Treeview(root,columns=['Port',
                                             'Port Name',
                                             'Result'])
    result_tree.heading('Port', text='Port')
    result_tree.heading('Port Name', text='Port Name')
    result_tree.heading('Result', text='Result')
    result_tree['show'] = 'headings'
    def scan_conn(host,port,name='NA'):
        try:
            socket_conn = socket(AF_INET, SOCK_STREAM)
            socket_conn.connect((host,port))
            socket_conn.send('TestTestTest')
            result = socket_conn.recv(100)
            port_status = 'Open'
        except:
            port_status = 'Close'
        finally:
            result_tree.insert('', 'end', values=(port,name,port_status))
            socket_conn.close()

    def port_scan(host,ports):
        try:
            host_ip = gethostbyname(host)
        except:
            messagebox.showerror('Unknown Host!')
            return
        ports = ports.split(',')
        for port in ports:
            t = Thread(target=scan_conn, args=(host,int(port)))
            t.start()

    def port_scan_all(host):
        try:
            host_ip = gethostbyname(host)
        except:
            messagebox.showerror('Unknown Host!')
            return
        print(ports)
        for port,values in ports.items():
            t = Thread(target=scan_conn, args=(host,values['port'],values['name']))
            t.start()

    def clear():
        result_tree.delete(*result_tree.get_children())
        host_var.set('')
        port_var.set('')

    scan_btn = ttk.Button(root,text='Scan',command=lambda :port_scan(host_var.get(),port_var.get()))
    scan_all_btn = ttk.Button(root, text='Scan All Common Ports', command=lambda :port_scan_all(host_var.get()))
    clear_btn = ttk.Button(root, text='Clear',command=lambda :clear())
    host_label.pack()
    host_entry.pack()
    port_label.pack()
    port_entry.pack()
    result_tree.pack()
    scan_btn.pack()
    clear_btn.pack()
    scan_all_btn.pack()
    root.mainloop()







main()



