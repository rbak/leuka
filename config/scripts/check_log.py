def do(**kwargs):
    bashCommand = "".join(['ssh ', kwargs['hostname'], ' tail -n 100 ', kwargs['log']])
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    if 'Error' in output:
        print output
        return False
    else:
        print 'No errors found in log '+kwargs['log']
        return True
