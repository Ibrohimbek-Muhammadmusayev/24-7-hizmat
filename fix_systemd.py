import paramiko

def fix_systemd():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected...")

    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('ascii', errors='ignore')
        err = stderr.read().decode('ascii', errors='ignore')
        return out, err

    # Inspect Python and Django
    out, err = run("/root/24-7-hizmat/venv/bin/python -c 'import django; print(django.__file__)'")
    print("Django location:", out.strip() or err.strip())

    # Correct Systemd config for Web Service
    service_web = """[Unit]
Description=24/7-ishlar Django Web Server (Daphne / ASGI)
After=network.target

[Service]
User=root
WorkingDirectory=/root/24-7-hizmat/backend
Environment="PATH=/root/24-7-hizmat/venv/bin:/usr/local/python3.10/bin:/usr/bin:/bin"
Environment="PYTHONPATH=/root/24-7-hizmat/backend:/root/24-7-hizmat/venv/lib/python3.10/site-packages"
ExecStart=/root/24-7-hizmat/venv/bin/python -m daphne -b 127.0.0.1 -p 8000 config.asgi:application
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""
    run(f"cat << 'EOF' > /etc/systemd/system/24-7-web.service\n{service_web}\nEOF")

    # Correct Systemd config for Bot Service
    service_bot = """[Unit]
Description=24/7-ishlar Telegram Bot Supervisor
After=network.target

[Service]
User=root
WorkingDirectory=/root/24-7-hizmat/backend
Environment="PATH=/root/24-7-hizmat/venv/bin:/usr/local/python3.10/bin:/usr/bin:/bin"
Environment="PYTHONPATH=/root/24-7-hizmat/backend:/root/24-7-hizmat/venv/lib/python3.10/site-packages"
ExecStart=/root/24-7-hizmat/venv/bin/python manage.py runbot
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
    run(f"cat << 'EOF' > /etc/systemd/system/24-7-bot.service\n{service_bot}\nEOF")

    run("systemctl daemon-reload")
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    import time
    time.sleep(3)

    out8000, _ = run("curl -I http://127.0.0.1:8000/")
    print("CURL 8000:", out8000.strip())

    out80, _ = run("curl -I http://127.0.0.1/")
    print("CURL 80:", out80.strip())

    client.close()

if __name__ == '__main__':
    fix_systemd()
