import paramiko

def sync_vps():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    print("Connected to VPS...")

    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('ascii', errors='ignore')
        err = stderr.read().decode('ascii', errors='ignore')
        print(f"[RUN] {cmd}")
        if out:
            print("[OUT]", out[:300])
        if err:
            print("[ERR]", err[:300])
        return out, err

    # Pull latest updates from GitHub
    run("cd /root/24-7-hizmat && git pull origin main")

    # Collectstatic
    run("/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py collectstatic --noinput")

    # Fix permissions
    run("chmod -R 755 /root/24-7-hizmat")

    # Restart Services
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    print("\n--- VPS SYNC FINISHED! ---")
    client.close()

if __name__ == '__main__':
    sync_vps()
