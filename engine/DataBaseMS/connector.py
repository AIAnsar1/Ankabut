import os

from abc import ABC, abstractmethod
from typing import Optional
from core.data import conf, logger
from core.exceptions import AnkabFilePathException, AnkabUndefinedMethod



class BaseConnector(ABC):
    
    
    def __init__(self):
        self.connector: Optional[object] = None
        self.cursor: Optional[object] = None
        self.hostname: Optional[str] = None
        self.port: Optional[int] = None
        self.user: Optional[str] = None
        self.password: Optional[str] = None
        self.db: Optional[str] = None
        
        
    def init_connection(self):
        self.user = conf.get("dbmsUser", "")
        self.password = conf.get("dbmsPass", "")
        self.hostname = conf.get("hostname")
        self.port = conf.get("port")
        self.db = conf.get("dbmsDb")
        
    def print_connection(self, dbms: str):
        if self.hostname and self.port:
            logger.info(f"[ ETA ]: Connection to {dbms} server '{self.hostname}:{self.port}' established")
            
    def print_closed(self, dbms: str):
        if self.hostname and self.port:
            logger.info(f"[ ETA ]: Connection to {dbms} server '{self.hostname}:{self.port}' closed")