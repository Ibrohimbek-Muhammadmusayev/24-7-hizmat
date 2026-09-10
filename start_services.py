import paramiko
import time

def start_services():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected to VPS...")

    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        return out, err

    print("1. Running Django Migrations...")
    out, err = run("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py migrate")
    print("Migrate done.")

    print("2. Running collectstatic...")
    run("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py collectstatic --noinput")

    print("3. Restarting Services...")
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    time.sleep(4)

    out_curl8000, _ = run("curl -I http://127.0.0.1:8000/")
    print("\n--- TEST PORT 8000 ---")
    print(out_curl8000.strip())

    out_curl80, _ = run("curl -I http://127.0.0.1/")
    print("\n--- TEST NGINX PORT 80 ---")
    print(out_curl80.strip())

    client.close()

if __name__ == '__main__':
    start_services()
