import paramiko
import time
import sys

def run_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to 185.196.215.231...")
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected successfully!")

    def exec_cmd(cmd, check_err=False):
        print(f"\n--- RUNNING: {cmd} ---")
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        if out:
            print(out)
        if err and check_err:
            print("STDERR:", err)
        return out, err

    # Step 1: Install Python 3.10 / deadsnakes PPA or check apt
    exec_cmd("DEBIAN_FRONTEND=noninteractive apt-get update -y")
    exec_cmd("DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common curl build-essential libssl-dev libffi-dev nginx supervisor git")
    exec_cmd("add-apt-repository -y ppa:deadsnakes/ppa")
    exec_cmd("DEBIAN_FRONTEND=noninteractive apt-get update -y")
    exec_cmd("DEBIAN_FRONTEND=noninteractive apt-get install -y python3.10 python3.10-venv python3.10-dev")
    
    # Check python3.10 version
    exec_cmd("python3.10 --version")

    # Step 2: Clone or Pull repository
    exec_cmd("rm -rf /root/24-7-hizmat")
    exec_cmd("git clone https://github.com/Ibrohimbek-Muhammadmusayev/24-7-hizmat.git /root/24-7-hizmat")

    # Step 3: Setup Virtualenv and Install dependencies
    exec_cmd("python3.10 -m venv /root/24-7-hizmat/venv")
    exec_cmd("/root/24-7-hizmat/venv/bin/pip install --upgrade pip setuptools wheel")
    exec_cmd("/root/24-7-hizmat/venv/bin/pip install -r /root/24-7-hizmat/backend/requirements.txt")
    exec_cmd("/root/24-7-hizmat/venv/bin/pip install gunicorn")

    # Step 4: Run Django Migrations & Collectstatic
    exec_cmd("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py migrate")
    exec_cmd("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py collectstatic --noinput")

    # Step 5: Configure Systemd Service for Gunicorn / Daphne and Bot Runner
    service_gunicorn = """[Unit]
Description=24/7-ishlar Django Web Server (Daphne / ASGI)
After=network.target

[Service]
User=root
WorkingDirectory=/root/24-7-hizmat/backend
ExecStart=/root/24-7-hizmat/venv/bin/daphne -b 127.0.0.1 -p 8000 config.asgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
    exec_cmd(f"cat << 'EOF' > /etc/systemd/system/24-7-web.service\n{service_gunicorn}\nEOF")

    # Bot Supervisor Systemd Service
    service_bot = """[Unit]
Description=24/7-ishlar Telegram Bot Supervisor
After=network.target

[Service]
User=root
WorkingDirectory=/root/24-7-hizmat/backend
ExecStart=/root/24-7-hizmat/venv/bin/python manage.py runbot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    exec_cmd(f"cat << 'EOF' > /etc/systemd/system/24-7-bot.service\n{service_bot}\nEOF")

    # Step 6: Configure Nginx
    nginx_conf = """server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    client_max_body_size 50M;

    location /static/ {
        alias /root/24-7-hizmat/backend/staticfiles/;
    }

    location /media/ {
        alias /root/24-7-hizmat/backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
    exec_cmd(f"cat << 'EOF' > /etc/nginx/sites-available/default\n{nginx_conf}\nEOF")
    exec_cmd("nginx -t")
    exec_cmd("systemctl restart nginx")

    # Step 7: Reload Systemd & Start Services
    exec_cmd("systemctl daemon-reload")
    exec_cmd("systemctl enable 24-7-web")
    exec_cmd("systemctl restart 24-7-web")
    exec_cmd("systemctl enable 24-7-bot")
    exec_cmd("systemctl restart 24-7-bot")

    # Verify status
    time.sleep(3)
    exec_cmd("systemctl status 24-7-web --no-pager")
    exec_cmd("systemctl status 24-7-bot --no-pager")
    exec_cmd("curl -I http://127.0.0.1/")

    print("\n--- DEPLOYMENT FINISHED SUCCESSFULLY! ---")
    client.close()

if __name__ == '__main__':
    run_ssh()
