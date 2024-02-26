import subprocess


def sub(command: str, text: str):
    res = subprocess.run(str(command), shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = res.stdout.split('\n')
    if str(text) in out and not res.returncode:
        return True
    else:
        return False


print(sub('cat /etc/os-release', 'VERSION_CODENAME=jammy'))
