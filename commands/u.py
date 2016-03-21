from portmgr import command_list, bcolors
import subprocess

def func(action):
    directory = action['directory']
    relative = action['relative']

    p = subprocess.Popen(["docker-compose", "up", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()

    print(out.decode("UTF-8"))

    # if p.returncode == 0:
    #    print('Created container in ' + relative)
    #else:
    if p.returncode != 0:
        print("Error creating " + relative + "!")
        print(bcolors.FAIL + err.decode("UTF-8") + bcolors.ENDC)

    return 0

command_list['u'] = {
    'hlp': 'Create container',
    'ord': 'nrm',
    'fnc': func
}
