import paramiko
import os
import sys

# Configuration
HOSTNAME = "123.56.121.200"
USERNAME = "suwenkui"
PASSWORD = "Qjjbmt@1"
REMOTE_DIR = "/home/suwenkui/woody_deploy"  # Deploy to user's home dir

def deploy():
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"🔌 Connecting to {HOSTNAME}...")
        client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
        print("✅ Connected!")

        # Create remote directory
        print(f"📂 Creating remote directory: {REMOTE_DIR}...")
        stdin, stdout, stderr = client.exec_command(f"mkdir -p {REMOTE_DIR}")
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            print(f"Error creating directory: {stderr.read().decode()}")
            return

        # Upload files
        sftp = client.open_sftp()
        files_to_upload = ["woody-app.tar", "docker-compose.yml"]
        
        for file in files_to_upload:
            if not os.path.exists(file):
                print(f"❌ Local file not found: {file}")
                return
            
            remote_path = f"{REMOTE_DIR}/{file}"
            print(f"⬆️ Uploading {file} to {remote_path}...")
            # Use callback to show progress if needed, but for simplicity just upload
            sftp.put(file, remote_path)
            print(f"✅ {file} uploaded.")
        
        sftp.close()

        # Execute Docker commands
        commands = [
            f"cd {REMOTE_DIR}",
            "echo '🐳 Loading Docker images...'",
            "docker load -i woody-app.tar",
            "echo '🚀 Starting services...'",
            "docker-compose up -d --remove-orphans",
            "echo '🧹 Pruning unused images...'",
            "docker image prune -f"
        ]
        
        full_command = " && ".join(commands)
        
        print("⚙️ Executing remote commands...")
        stdin, stdout, stderr = client.exec_command(full_command)
        
        # Stream output
        for line in stdout:
            print(f"[REMOTE] {line.strip()}")
            
        for line in stderr:
            print(f"[REMOTE ERROR] {line.strip()}")
            
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("✅ Deployment completed successfully!")
        else:
            print("❌ Deployment failed with errors.")

        client.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    deploy()
