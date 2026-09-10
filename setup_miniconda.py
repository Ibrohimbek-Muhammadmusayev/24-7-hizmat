import paramiko
import time

def setup_python():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected to VPS...")

    def run(cmd):
        print(f"\n[RUN] {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        if out:
            print(out)
        if err:
            print("[ERR]", err)
        return out

    # Check if miniconda installer exists or download
    run("curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh")
    run("bash /tmp/miniconda.sh -b -u -p /root/miniconda3")
    run("/root/miniconda3/bin/conda create -y -n py311 python=3.11")
    run("/root/miniconda3/envs/py311/bin/python --version")

    # Pip install requirements
    run("/root/miniconda3/envs/py311/bin/pip install --upgrade pip")
    run("/root/miniconda3/envs/py311/bin/pip install -r /root/24-7-hizmat/backend/requirements.txt")
    run("/root/miniconda3/envs/py311/bin/pip install daphne gunicorn")

    # Run migrations and collectstatic
    run("/root/miniconda3/envs/py311/bin/python /root/24-7-hizmat/backend/manage.py migrate")
    run("/root/miniconda3/envs/py311/bin/python /root/24-7-hizmat/backend/manage.py collectstatic --noinput")

    # Update systemd services
    service_web = """[Unit]
Description=24/7-ishlar Django Web Server (Daphne / ASGI)
After=network.target

[Service]
User=root
WorkingDirectory=/root/24-7-hizmat/backend
ExecStart=/root/miniconda3/envs/py311/bin/daphne -b 127.0.0.1 -p 8000 config.asgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
    run(f"cat << 'EOF' > /etc/systemd/system/24-7-web.service\n{service_web}\nEOF")

    service_bot = """[Unit]
Description=24/7-ishlar Telegram Bot Supervisor
After=network.target

[Service]
User=root
WorkingDirectory=/root/24-7-hizmat/backend
ExecStart=/root/miniconda3/envs/py311/bin/python manage.py runbot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    run(f"cat << 'EOF' > /etc/systemd/system/24-7-bot.service\n{service_bot}\nEOF")

    run("systemctl daemon-reload")
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    time.sleep(3)
    run("systemctl status 24-7-web --no-pager")
    run("curl -I http://127.0.0.1:8000/")
    run("curl -I http://127.0.0.1/")

    print("\n--- ALL DONE SUCCESSFULLY! ---")
    client.close()

if __name__ == '__main__':
    setup_python()
