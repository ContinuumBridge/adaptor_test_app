#!/usr/bin/env python
# adaptor_test_app_a.py
"""
Copyright (c) 2014 ContinuumBridge Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
ModuleName = "adaptor_test_app" 

import sys
import os.path
import time
import logging
from cbcommslib import CbApp
from cbconfig import *

class App(CbApp):
    def __init__(self, argv):
        logging.basicConfig(filename=CB_LOGFILE,level=CB_LOGGING_LEVEL,format='%(asctime)s %(message)s')
        self.appClass = "control"
        self.state = "stopped"
        # Super-class init must be called
        CbApp.__init__(self, argv)

    def setState(self, action):
        self.state = action
        msg = {"id": self.id,
               "status": "state",
               "state": self.state}
        self.sendManagerMessage(msg)

    def onAdaptorService(self, message):
        #logging.debug("%s onadaptorService, message: %s", ModuleName, message)
        s = []
        for p in message["service"]:
            logging.info("%s %s characteristic: %s", ModuleName, self.id, str(p["characteristic"]))
            s.append({"characteristic": p["characteristic"], "interval": 0})
        req = {"id": self.id,
               "request": "service",
               "service": s,
              }
        self.sendMessage(req, message["id"])
        logging.debug("%s onadaptorservice, req: %s", ModuleName, req)

    def onAdaptorData(self, message):
        #logging.debug("%s %s message: %s", ModuleName, self.id, str(message))
        logging.info("%s %s characteristic: %s", ModuleName, self.id, str(message["characteristic"]))
        logging.info("%s %s data: %s", ModuleName, self.id, str(message["data"]))

    def onConfigureMessage(self, config):
        #logging.debug("%s onConfigureMessage, config: %s", ModuleName, config)
        self.setState("starting")

if __name__ == '__main__':
    App(sys.argv)
