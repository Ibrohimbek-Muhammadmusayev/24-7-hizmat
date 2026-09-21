import paramiko

def check_vps_db():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    
    stdin, stdout, stderr = client.exec_command("cd /root/24-7-hizmat/backend && /usr/local/python3.10/bin/python3.10 manage.py shell -c 'from locations.models import reverse_geocode; from accounts.models import User; print(\"GEO:\", reverse_geocode(40.47403, 72.003687)); u = User.objects.filter(telegram_id=6481018655).first(); print(\"USER:\", u.first_name, u.region_id, u.district, u.latitude, u.longitude)'")
    out = stdout.read().decode('ascii', errors='ignore')
    err = stderr.read().decode('ascii', errors='ignore')
    print("OUT:", out)
    print("ERR:", err)
    client.close()

if __name__ == '__main__':
    check_vps_db()
