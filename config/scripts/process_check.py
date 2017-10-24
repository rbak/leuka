def do(**kwargs):
    bashCommand = "".join(['ssh ', kwargs['hostname'], ' sudo service ', kwargs['service'], ' status'])
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    if 'start/running' in output:
        return False
    else:
        print kwargs['service'], 'is not running'
        return True
