import paramiko

def install_direct():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected...")

    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('ascii', errors='ignore')
        err = stderr.read().decode('ascii', errors='ignore')
        print(f"\n[RUN] {cmd}")
        if out:
            print("[OUT]", out[:300])
        if err:
            print("[ERR]", err[:300])
        return out, err

    run("/usr/local/python3.10/bin/pip3.10 install django djangorestframework djangorestframework-simplejwt django-cors-headers channels daphne python-telegram-bot requests pillow python-dotenv gunicorn")
    run("/usr/local/python3.10/bin/python3.10 -c 'import django; print(\"DJANGO INSTALLED AT:\", django.__file__)'")

    # Update systemd to use /usr/local/python3.10
    service_web = """[Unit]
Description=24/7-ishlar Django Web Server (Daphne / ASGI)
After=network.target

[Service]
User=root
WorkingDirectory=/root/24-7-hizmat/backend
Environment="PATH=/usr/local/python3.10/bin:/usr/bin:/bin"
ExecStart=/usr/local/python3.10/bin/daphne -b 127.0.0.1 -p 8000 config.asgi:application
Restart=always
RestartSec=3

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
Environment="PATH=/usr/local/python3.10/bin:/usr/bin:/bin"
ExecStart=/usr/local/python3.10/bin/python3.10 manage.py runbot
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
    run(f"cat << 'EOF' > /etc/systemd/system/24-7-bot.service\n{service_bot}\nEOF")

    run("/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py migrate")
    run("/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py collectstatic --noinput")

    run("systemctl daemon-reload")
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    import time
    time.sleep(3)

    run("curl -I http://127.0.0.1:8000/")
    run("curl -I http://127.0.0.1/")

    client.close()

if __name__ == '__main__':
    install_direct()
