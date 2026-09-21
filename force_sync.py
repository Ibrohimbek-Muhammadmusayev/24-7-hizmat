import paramiko

def force_pull_and_sync():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('185.196.215.231', username='root', password='IB@12345678ib', timeout=20)
    
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

    run("cd /root/24-7-hizmat && git fetch --all && git reset --hard origin/main")
    run("/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py migrate --noinput")
    run("/usr/local/python3.10/bin/python3.10 /root/24-7-hizmat/backend/manage.py collectstatic --noinput")
    run("chmod -R 755 /root/24-7-hizmat")
    run("systemctl restart 24-7-web")
    run("systemctl restart 24-7-bot")
    run("systemctl restart nginx")

    # Test download-backup endpoint
    out_backup, _ = run("curl -I http://127.0.0.1/api/accounts/download-backup/")
    print("BACKUP ENDPOINT STATUS:", out_backup.strip())

    client.close()

if __name__ == '__main__':
    force_pull_and_sync()
