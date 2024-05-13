import subprocess
import json

def get():
    try:
        batch_file_path = './src/shell/hot.sh'
        result = subprocess.run(batch_file_path, capture_output=True, text=True, check=True)
        stdout = result.stdout
        outputs = stdout.split('\n')
        result = json.loads(outputs[-1])
        data = result['data']
        return data[0]['data'][:10]
    except subprocess.CalledProcessError as e:
        print('Error:', e)
        return False