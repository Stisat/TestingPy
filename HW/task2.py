import string
import subprocess


def sub(command: str, text: str):
    res = subprocess.run(str(command), shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = res.stdout.split('\n')
    output = ''
    for i in out:
        output += str(i)
    a = output.translate(str.maketrans('', '', string.punctuation))
    if str(text) in a and not res.returncode:
        return True
    else:
        return False


print(sub('cat /etc/os-release', 'jammy'))