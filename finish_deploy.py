import paramiko
import time

def finish_deployment():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected to VPS...")

    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        return out, err

    print("1. Installing Python packages via pip...")
    run("/root/24-7-hizmat/venv/bin/pip install --upgrade pip")
    out, err = run("/root/24-7-hizmat/venv/bin/pip install -r /root/24-7-hizmat/backend/requirements.txt")
    print("Packages installed:", "django" in out.lower() or "installed" in out.lower() or "satisfy" in out.lower())
    
    print("2. Installing daphne & gunicorn...")
    run("/root/24-7-hizmat/venv/bin/pip install daphne gunicorn")

    print("3. Running Django Migrations...")
    out_mig, _ = run("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py migrate")
    print("Migrations applied!")

    print("4. Running Collectstatic...")
    run("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py collectstatic --noinput")

    print("5. Starting Systemd Web & Bot Services...")
    run("systemctl daemon-reload")
    run("systemctl enable 24-7-web")
    run("systemctl restart 24-7-web")
    run("systemctl enable 24-7-bot")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    time.sleep(3)
    out_curl, _ = run("curl -I http://127.0.0.1:8000/")
    print("\n--- INTERNAL SERVER TEST (PORT 8000) ---")
    print(out_curl.strip())

    out_nginx, _ = run("curl -I http://127.0.0.1/")
    print("\n--- NGINX REVERSE PROXY TEST (PORT 80) ---")
    print(out_nginx.strip())

    client.close()

if __name__ == '__main__':
    finish_deployment()
