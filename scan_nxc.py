import argparse
import os
import time

#BASE_CMD_RDP = "proxychains -q -f /etc/proxychains4_17171.conf nxc rdp "
#BASE_CMD_WINRM = "proxychains -q -f /etc/proxychains4_17171.conf nxc winrm "
#BASE_CMD_RDP = "proxychains -q nxc rdp "
#BASE_CMD_WINRM = "proxychains -q nxc winrm "
BASE_CMD_RDP = "nxc rdp "
BASE_CMD_WINRM = "nxc winrm "
BASE_CMD_SMB = "nxc smb "

def parse_args():
    parser = argparse.ArgumentParser(description='Run commands on remote hosts')
    parser.add_argument('--host', type=str, default=None, help='IP address of the host to connect to')
    parser.add_argument('--file', type=str, default=None, help='Path to file with list of IP addresses')
    parser.add_argument('-p', type=str, default=None, help='The scan uses this password for authorization')
    parser.add_argument('-u', type=str, default=None, help='The scan uses this login for authorization')
    parser.add_argument('-H', type=str, default=None, help='The scan uses this hash for authorization')
    parser.add_argument('--winrm', action='store_true', help='Scan by winrm')
    parser.add_argument('--smb', action='store_true', help='Scan by smb')
    parser.add_argument('--rdp', action='store_true', help='Scan by rdp')
    parser.add_argument('--sto', type=int, default=0, help='The beginning of the third octet of ip (default=0)')
    parser.add_argument('--eto', type=int, default=255, help='The end of the third octet of ip (default=255)')
    parser.add_argument('--sfo', type=int, default=0, help='The beginning of the fourth octet of ip (default=0)')
    parser.add_argument('--efo', type=int, default=255, help='The end of the third octet of ip (default=255)')

    return parser.parse_args()

def read_ip_list(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def octet_enum(net_addr, username=None, password=None, hash=None):
        args = parse_args()
        net_addr  = net_addr.split('.')
        net_addr = net_addr[:2]
        start_third_octet = args.sto
        end_third_octet = args.efo
        start_fourth_octet = args.sfo
        end_fourth_octet = args.eto
        for octet in range(start_third_octet,end_third_octet+1): 
            for octet2 in range(start_fourth_octet,end_fourth_octet+1):
                ip = f"{net_addr[0]}.{net_addr[1]}.{octet}.{octet2}"
                if username is None:
                    command1 = BASE_CMD_RDP + f" {ip}"
                    command2 = BASE_CMD_WINRM + f" {ip}"
                    command3 = BASE_CMD_SMB + f" {ip}"
                    output(command1,command2,command3,ip)

                if username is not None and password is not None:
                    command1 = BASE_CMD_RDP + f" {ip}" + f" -u {username}"+f" -p {password}"
                    command2 = BASE_CMD_WINRM + f" {ip}" + f" -u {username}"+f" -p {password}"
                    command2 = BASE_CMD_SMB + f" {ip}" + f" -u {username}"+f" -p {password}"
                    output(command1,command2,command3,ip)


                if username is not None and hash is not None:
                    command1 = BASE_CMD_RDP + f" {ip}" +  f" -u {username}"+f" -H {hash}"
                    command2 = BASE_CMD_WINRM +  f" {ip}" +  f" -u {username}"+f" -H {hash}"
                    command3 = BASE_CMD_SMB +  f" {ip}" +  f" -u {username}"+f" -H {hash}"
                    output(command1,command2,command3,ip)

def from_ip_list(file, username=None, password=None, hash=None):
        ip_list = read_ip_list(file)
        for ip in ip_list:
            if username is None:
                command1 = BASE_CMD_RDP + f" {ip}"
                command2 = BASE_CMD_WINRM + f" {ip}"
                command3 = BASE_CMD_SMB + f" {ip}"
                output(command1,command2,command3,ip)


            
            if username is not None and password is not None:
                command1 = BASE_CMD_RDP + f" {ip}" + f" -u {username}"+f" -p {password}"
                command2 = BASE_CMD_WINRM + f" {ip}" + f" -u {username}"+f" -p {password}"
                command3 = BASE_CMD_SMB + f" {ip}" + f" -u {username}"+f" -p {password}"
                output(command1,command2,command3,ip)

               
            if username is not None and hash is not None:
                command1 = BASE_CMD_RDP + f" {ip}" +  f" -u {username}"+f" -H {hash}"
                command2 = BASE_CMD_WINRM +  f" {ip}" +  f" -u {username}"+f" -H {hash}"
                command3 = BASE_CMD_SMB +  f" {ip}" +  f" -u {username}"+f" -H {hash}"
                output(command1,command2,command3,ip)

def output(command1,command2,command3,ip):
    args = parse_args()
    if args.rdp:
        print(f"RDP -> {ip}")
        output = os.system(command1)
        time.sleep(0.3)
    if args.winrm:
        print(f"WIN -> {ip}")
        output = os.system(command2)
        time.sleep(0.3)
    if args.smb:
        print(f"SMB -> {ip}")
        output = os.system(command3)
        time.sleep(0.3)




def main():
    args = parse_args()
    if args.file is not None:
        if args.u is not None:
            if args.p is not None:
                from_ip_list(args.file, args.u, args.p )
            if args.H is not None:
                from_ip_list(args.file, args.u, hash=args.H)
        if args.u is None:
            from_ip_list(args.file)


    if args.file is None:
        if args.u is not None:
            if args.p is not None:
                octet_enum(args.host, args.u, args.p )
            if args.H is not None:
                octet_enum(args.host, args.u, hash=args.H)
        if args.u is None:
            octet_enum(args.host)
              
        

if __name__ == '__main__':
    main()
