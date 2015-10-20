#!/usr/bin/python3
import cherrypy
from app import Root
from quotedb import QuoteDB
import sys

db = sys.argv[1]
app = cherrypy.tree.mount(Root(db), '/logs/')

if __name__=='__main__':

    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 7999,
    })

    # Run the application using CherryPy's HTTP Web Server
    cherrypy.quickstart(Root(db))
