from portmgr import command_list, bcolors
import subprocess

def func(action):
    directory = action['directory']
    relative = action['relative']
    
    p = subprocess.Popen(["docker-compose", "ps"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()
    
    if p.returncode == 0:
      start = False
      lines = [x for x in out.decode('utf8').split('\n') if x]
      containers = []
      for line in lines:
        if start:
          parts = line.split(' ')
          containers.append(parts[0])
        elif line.startswith("----"):
          start = True
      
      index = 0
      if len(containers) == 0:
        print("No containers found!")
        return 1
      elif len(containers) > 1:
        # ask..
        print("Choose container:")
        valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")
                                 
        index = 1
      container_id = containers[index]
      print("Attaching to " + container_id)
      subprocess.call(["docker", "exec", "-it", container_id, "bash"])

    # res = subprocess.call(["docker-compose", "logs", "--follow", "--tail=200"])

    # if res != 0:
        # print("Error showing logs for " + relative + "!\n")

    return 0

command_list['a'] = {
    'hlp': 'Attach to process',
    'ord': 'nrm',
    'fnc': func
}
