import sqlite3

class QuoteDB:
    def __init__ (self, dbname):
        self.conn = sqlite3.connect(dbname)
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS log (id integer primary key, timestamp datetime DEFAULT CURRENT_TIMESTAMP, user text, quote text)")
        c.execute("CREATE TABLE IF NOT EXISTS quotes (id integer primary key, log_id integer)")
        self.conn.commit()
    
    def log(self, nick, quote):
        c = self.conn.cursor()
        c.execute("INSERT INTO log (user, quote) VALUES (?, ?)", (nick, quote))
        self.conn.commit()

    def get_random(self, nick = None):
        c = self.conn.cursor()
        if nick:
            c.execute("SELECT log.user, log.quote FROM log, quotes WHERE log.user = ? AND log.id = quotes.log_id ORDER BY RANDOM() LIMIT 1", (nick, ));
        else:
            c.execute("SELECT log.user, log.quote FROM log, quotes WHERE log.id = quotes.log_id ORDER BY RANDOM() LIMIT 1");
        return c.fetchone()

    def get_log(self, nick = None, index = 0):
        c = self.conn.cursor()
        if nick:
            c.execute("SELECT user, quote FROM log WHERE user = ? ORDER BY id DESC LIMIT 1 OFFSET ?", (nick, index));
        else:
            c.execute("SELECT user, quote FROM log ORDER BY id DESC LIMIT 1 OFFSET ?", (index, ));
        return c.fetchone()
    
    def save_quote(self, nick = None, index = 0):
        c = self.conn.cursor()
        if nick:
            c.execute("INSERT INTO quotes (log_id) SELECT id FROM log WHERE user = ? ORDER BY id DESC LIMIT 1 OFFSET ?", (nick, index));
        else:
            c.execute("INSERT INTO quotes (log_id) SELECT id FROM log ORDER BY id DESC LIMIT 1 OFFSET ?", (index, ));
        self.conn.commit()

    def get_logs(self, date = 'now'):
        c = self.conn.cursor()
        c.execute("SELECT id, timestamp, user, quote FROM log WHERE timestamp >= datetime(?) and timestamp < datetime(?, '+1 day') ORDER BY timestamp ASC", (date, date))
        return c.fetchall()

    def get_dates(self):
        c = self.conn.cursor()
        c.execute("SELECT date(timestamp) as dates FROM log GROUP BY dates")
        return c.fetchall()
