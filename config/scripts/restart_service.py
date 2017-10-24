def do(**kwargs):
    bashCommand = "".join(['ssh ', kwargs['hostname'], ' sudo service ', kwargs['service'], ' restart'])
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    print kwargs['service']+' restarted on '+kwargs['hostname']
