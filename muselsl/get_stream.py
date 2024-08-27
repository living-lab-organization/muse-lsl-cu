import subprocess

name = 'MuseS-7A18'

command = ''.join(['muselsl stream -n ', name, ' -p -c -g'])
subprocess.call(command)