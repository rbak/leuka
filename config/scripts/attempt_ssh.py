def run(**kwargs):
    bashCommand = "".join(['ssh -vv ubuntu@', kwargs['node'].name])
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    return False
    # if 'Error' in output:
    #     print output
    #     return False
    # else:
    #     print 'No errors found in log '+kwargs['log']
    #     return True
