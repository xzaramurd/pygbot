import cherrypy
from quotedb import QuoteDB

class Root(object):
    def __init__(self, db):
        self.db = db

    @cherrypy.expose
    def index(self):
        return "Hello, world!"

    @cherrypy.expose
    def logs(self, index = -1):
        db = QuoteDB(self.db)
        dates = db.get_dates()
        index = int(index)
        if index == -1:
            index += len(dates)
        if index >= len(dates) or index < 0:
            return None

        date = dates[index]
        types = ["text", "channel"]

        page = "<html><head><link rel='stylesheet' type='text/css' href='static/style.css'><script type='text/javascript' src='static/md5.min.js'></script><script type='text/javascript' src='static/Autolinker.min.js'></script><script type='text/javascript' src='static/logs.js'></script><title>Logs for {0}</title></head><body onload='logs_init()'>".format(date[0])
        quotes = db.get_logs(date[0]);
        for quote in quotes:
            ltype = types[int(quote[4])] if len(types) > int(quote[4]) else types[0]
            page += "<a name='{3}' href='#{3}' class='nodec' ><p class='small'><span class='entry' id='{1}'>[<span class='date'>{0}</span>] {1}: </span></a><span class='{4}'>{2}</span></p>".format(quote[1], quote[2], quote[3], quote[0], ltype)
        page += "<p>"
        if index > 0:
            page += "<a href=logs?index={0}>Previous |".format(index - 1)
        if index < len(dates) - 1:
            page += " <a href=logs?index={0}>Next".format(index + 1)
        page += "</p></html></body>"	
        return page
