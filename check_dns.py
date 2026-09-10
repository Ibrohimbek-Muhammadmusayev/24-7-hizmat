import paramiko

def check_server_dns():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    
    stdin, stdout, stderr = client.exec_command("nslookup ishtop24.uz 8.8.8.8; nslookup admin.ishtop24.uz 8.8.8.8; ping -c 1 ishtop24.uz")
    out = stdout.read().decode('ascii', errors='ignore')
    print("DNS Lookup from Server:")
    print(out)
    
    client.close()

if __name__ == '__main__':
    check_server_dns()
