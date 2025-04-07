import threading

from core.enums import CustomLogging, TimeoutState
from core.data import logger






def timeout(func, args=None, Kwargs=None, duration=1, default=None):
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None
            self.timeout_state = None
            
        def run(self):
            try:
                self.result = func(*(args or ()), **(Kwargs or {}))
                self.timeout_state = TimeoutState.NORMAL
            except Exception as ex:
                logger.log(CustomLogging.TRAFFIC_IN, ex)
                self.result = default
                self.timeout_state = TimeoutState.EXCEPTION
        
    thread = InterruptableThread()
    thread.start()
    thread.join(duration)
    
    if thread.is_alive():
        return default, TimeoutState.TIMEOUT
    else:
        return thread.result, thread.timeout_state