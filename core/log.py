import logging, re, sys

from .enums import CustomLogging



logging.addLevelName(CustomLogging.PAYLOAD, "PAYLOAD") # Logger The Request Payload
logging.addLevelName(CustomLogging.TRAFFIC_OUT, "TRAFFIC OUT") # Logger Outgoing Traffic
logging.addLevelName(CustomLogging.TRAFFIC_IN, "TRAFFIC IN") # Logger Incoming Traffic 
Logger = logging.getLogger("Ankabut") # Creating a Ankabut Global Logger
LoggerHandler = None


# Setting Up a log handler 
# This code tires to import log handler (ColorizingStreamHandler)
# if it is not present, logging will be standart (via StreamHandler)
try:
    from pkg.ansistrm.ansistrm import ColorizingStreamHandler

    # Custom Color Logger Class 
    
    class _ColorizingStreamHandler(ColorizingStreamHandler):
        """_summary_
            This class inherits from ColorizingStreamHandler and ovverides the colorize() method
            which is responsible for coloring logs  
            
            what does it do?
            
            defines the color for the logging level (e.g. Payload is blue Traffic Out is purple)
            Defines which parts of the message should be highlighted in color (e.g. [12:34:56] is the time, [#1] is the request counter).
            Clears the message from unnecessary ANSI codes if the terminal does not support colors.

        Args:
            ColorizingStreamHandler (_type_): _description_
        """
        def colorize(self, message, levelno, force=False):
            if levelno in self.level_map and (self.is_tty or force):
                bg, fg, bold = self.level_map[levelno]
                params = []
                
                if bg in self.color_map:
                    params.append(str(self.color_map[bg] + 40))
                    
                if fg in self.color_map:
                    params.append(str(self.color_map[fg] + 30))
                    
                if bold:
                    params.append('1')
                
                if params and message:
                    match = re.search(r"\A(\s+)", message)
                    prefix = match.group(1) if match else ""
                    message = message[len(prefix)]
                    match = re.search(r"\[([A-Z ]+)\]", message) # Logger Level
                    
                    if match:
                        level = match.group(1)
                        
                        if message.startswith(self.bold):
                            message = message.replace(self.bold, "")
                            reset = self.reset + self.bold
                            params.append('1')
                        else:
                            reset = self.reset
                        message = message.replace(level, ''.join((self.csi, ':'.join(params), 'm', level, reset)), 1)
                        match = re.search(r"\A\s*\[([\d:]+)\]", message) # Time
                        
                        if match:
                            time = match.group(1)
                            message = message.replace(time, ''.join((self.csi, str(self.color_map["cyan"] + 30), 'm', time, self._reset(message))), 1)
                        match = re.search(r"\A\s*\[([\d:]+)\]", message) # Counter
                        
                        if match:
                            counter = match.group(1)
                            message = message.replace(counter, ''.join((self.csi, str(self.color_map["yellow"] + 30), 'm', counter, self._reset(message))), 1)
                            
                        if level != "PAYLOAD":
                            
                            if any(_ in message for _ in ("Parsed DBMS Error Message",)):
                                match = re.search(r": '(.+)'", message)
                                
                                if match:
                                    string = match.group(1)
                                    message = message.replace("'%s'" % string, "'%s'" % ''.join((self.csi, str(self.color_map["white"] + 30), 'm', string, self._reset(message))), 1) 
                                else:
                                    match = re.search(r"\bresumed: '(.+\.\.\.)", message)
                                    
                                    if match:
                                        string = match.group(1)
                                        message = message.replace("'%s'" % string, "'%s'" % ''.join((self.csi, str(self.color_map["white"] + 30), 'm', string, self._reset(message))), 1)
                                    else:
                                        for match in re.finditer(r"[^\w]'([^']+)'", message): # Single Quoted
                                            string = match.group(1)
                                            message = message.replace("'%s'" % string, "'%s'" % ''.join((self.csi, str(self.color_map["white"] + 30), 'm', string, self._reset(message))), 1)
                    else:
                        message = ''.join((self.csi, ':'.join(params), 'm', message, self.reset))
                        
                    if prefix:
                        message = "%s%s" % (prefix, message)      
                    message = message.replace("%s]" % self.bold, "]%s" % self.bold)  # Dirty Patch
                    
            return message
    disableColor = False
    
    for argument in sys.argv:
        if "disable-col" in argument:
            disableColor = True
            break
        if disableColor:
            LoggerHandler = logging.StreamHandler(sys.stdout)
        else:
            LoggerHandler = _ColorizingStreamHandler(sys.stdout)
            LoggerHandler.level_map[logging.getLevelName("PAYLOAD")] = (None, "cyan", False)
            LoggerHandler.level_map[logging.getLevelName("TRAFFIC OUT")] = (None, "magentia", False)
            LoggerHandler.level_map[logging.getLevelName("TRAFFIC IN")] = ("magentia", None, False)
    
except ImportError:
    LoggerHandler = logging.StreamHandler(sys.stdout)

Formatter = logging.Formatter("r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
LoggerHandler.setFormatter(Formatter)
Logger.addHandler(LoggerHandler)
Logger.setLevel(logging.INFO)
