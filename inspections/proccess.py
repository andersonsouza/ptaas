from subprocess import Popen
import subprocess
import threading
from datetime import datetime


class ProcessManager(object):
    
    __POOL = {}
    
    @staticmethod
    def run(key, command, callback=None, *args, **kwargs):
        def do(command, callback, args, kwargs):
            print('[%s] Execution of "%s" started.' % (datetime.now().strftime('%d/%b/%Y %H:%M:%S'), command))
            process = Popen(command.split(' '), stdout=subprocess.PIPE, *args, **kwargs)
            process.wait()
            print('[%s] Execution of "%s" ended.' % (datetime.now().strftime('%d/%b/%Y %H:%M:%S'), command))
            callback(process)
        thread = threading.Thread(target=do, args=(command, callback, args, kwargs))
        ProcessManager.__POOL.update({key: thread})
        thread.start()
        return thread
        
    @staticmethod
    def get(key):
        return ProcessManager.__POOL.get(key)
        
    @staticmethod
    def kill(key):
        if ProcessManager.__POOL.get(key):
            ProcessManager.__POOL.get(key).kill()
        return ProcessManager.pop(key)
    
    @staticmethod
    def pop(key):
        return ProcessManager.__POOL.pop(key)
