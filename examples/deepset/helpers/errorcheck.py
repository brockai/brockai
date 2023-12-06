import subprocess

def elasticsearch_health():
    curl_command = ["curl", "-X", "GET", "http://localhost:9201/_cat/healthm"]
    
    try:
        process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # stdout, stderr = process.communicate()

        if process.returncode == 0:
            # print(stdout.decode("utf-8"))
            return True
        else:
            # print(f"Error: {stderr.decode('utf-8')}")
            return False

    except FileNotFoundError:
        print("cURL command not found or subprocess module not available.")
        return False
      
    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        return False
