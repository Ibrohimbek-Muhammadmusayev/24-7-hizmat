import paramiko
import time

def build_python():
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
            # Avoid printing non-ascii bullet points that crash windows terminal
            print(out[:500] if len(out) > 500 else out)
        if err:
            print("[ERR]", err[:500] if len(err) > 500 else err)
        return out

    # Install build deps for Python 3.10
    run("DEBIAN_FRONTEND=noninteractive apt-get update -y")
    run("DEBIAN_FRONTEND=noninteractive apt-get install -y wget build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev")

    # Download Python 3.10.13 source and compile
    run("cd /tmp && wget -q https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz && tar -xf Python-3.10.13.tgz")
    run("cd /tmp/Python-3.10.13 && ./configure --enable-optimizations --prefix=/usr/local/python3.10 && make -j2 && make altinstall")

    # Test python3.10
    run("/usr/local/python3.10/bin/python3.10 --version")

    # Create venv and install dependencies
    run("rm -rf /root/24-7-hizmat/venv")
    run("/usr/local/python3.10/bin/python3.10 -m venv /root/24-7-hizmat/venv")
    run("/root/24-7-hizmat/venv/bin/pip install --upgrade pip setuptools wheel")
    run("/root/24-7-hizmat/venv/bin/pip install -r /root/24-7-hizmat/backend/requirements.txt")
    run("/root/24-7-hizmat/venv/bin/pip install daphne gunicorn")

    # Run Django Migrations and Collectstatic
    run("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py migrate")
    run("/root/24-7-hizmat/venv/bin/python /root/24-7-hizmat/backend/manage.py collectstatic --noinput")

    # Update systemd services
    service_web = """[Unit]
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
    run(f"cat << 'EOF' > /etc/systemd/system/24-7-web.service\n{service_web}\nEOF")

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
    run(f"cat << 'EOF' > /etc/systemd/system/24-7-bot.service\n{service_bot}\nEOF")

    run("systemctl daemon-reload")
    run("systemctl enable 24-7-web")
    run("systemctl restart 24-7-web")
    run("systemctl enable 24-7-bot")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    time.sleep(3)
    run("curl -I http://127.0.0.1:8000/")
    run("curl -I http://127.0.0.1/")

    print("\n--- SERVER DEPLOYMENT COMPLETED SUCCESSFULLY! ---")
    client.close()

if __name__ == '__main__':
    build_python()
