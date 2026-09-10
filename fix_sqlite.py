import paramiko
import time

def fix_sqlite():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected to VPS...")

    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('ascii', errors='ignore')
        err = stderr.read().decode('ascii', errors='ignore')
        print(f"\n[RUN] {cmd}")
        if out:
            print("[OUT]", out[:200])
        if err:
            print("[ERR]", err[:200])
        return out, err

    # 1. Install pysqlite3-binary into python3.10
    run("/usr/local/python3.10/bin/pip3.10 install pysqlite3-binary")

    # 2. Inject pysqlite3 override at top of config/settings.py
    run("python3 -c \"path='/root/24-7-hizmat/backend/config/settings.py'; content=open(path).read(); prefix='__import__(\\'pysqlite3\\')\\nimport sys\\nsys.modules[\\'sqlite3\\'] = sys.modules.pop(\\'pysqlite3\\')\\n'; open(path,'w').write(prefix + content)\"")

    # 3. Test manage.py runbot import and version
    run("/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py migrate")

    # 4. Restart Services
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    time.sleep(3)
    out_web, _ = run("systemctl status 24-7-web --no-pager")
    out_bot, _ = run("systemctl status 24-7-bot --no-pager")
    print("WEB STATUS:", "active (running)" in out_web)
    print("BOT STATUS:", "active (running)" in out_bot)

    out_curl, _ = run("curl -I http://127.0.0.1:8000/")
    print("PORT 8000:", out_curl.strip())

    client.close()

if __name__ == '__main__':
    fix_sqlite()
