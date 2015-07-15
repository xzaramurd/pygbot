#!/usr/bin/python3
# vim: set fileencoding=utf-8

import irc.bot
import random
import signal
import re
from quotedb import QuoteDB

bot = None

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, db, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.db = db
        irc.client.ServerConnection.buffer_class.errors = 'replace'

    def on_nicknameinuse(self, c, e):
        print("Nickname in use")
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        print("Connected to server")
        c.join(self.channel)

    def on_join(self, c, e):
        print("join:", e.source.nick)
        if e.source.nick != c.get_nickname():
            self.db.log(e.source.nick, "has joined")

    def on_part(self, c, e):
        print("part:", e.source.nick)
        if e.source.nick != c.get_nickname():
            self.db.log(e.source.nick, "has left")

    def on_quit(self, c, e):
        print("quit:", e.source.nick)
        if e.source.nick != c.get_nickname():
            self.db.log(e.source.nick, "has left")

    def on_privmsg(self, c, e):
        a = e.arguments[0].strip()
        print("private", a)
        if len(a) > 1 and a[0] == '!':
            self.do_command(e, a[1:])
        else:
            self.do_command(e, a)

    def on_pubmsg(self, c, e):
        a = e.arguments[0].strip()
        if a[0] == '!':
            print("public", a)
            self.do_command(e, a[1:], private=False)
        else:
            nick = e.source.nick
            print(nick)

            # correct any mishaps
            if re.compile(ur'libr[ăa]ri[eai]', re.UNICODE).search(a.lower()):
                c = self.connection
                c.privmsg(self.channel, nick + ": " + u'BI-BLI-O-TE-CA!')

            self.db.log(nick, a)
            return

    def do_command(self, e, cmd, private=True):
        nick = e.source.nick
        c = self.connection

        cmd = cmd.split()
        if len(cmd) == 0:
            c.notice(nick, "Not understood")
            return
        if cmd[0] == "roll":
            rolls = str(nick) + " rolls " 

            if len(cmd) >= 2:
                for roll in cmd[1:]:
                    v = roll.split('d')
                    if len(v) == 1:
                        n = 1
                    else:
                        try:
                            n = int(v[0])
                        except ValueError:
                            n = 1
                    try:
                        d = int(v[-1])
                    except ValueError:
                        d = 2
                    n = max(min(n, 10), 1)
                    d = max(min(d, 10000), 2)
                    rolls += str(n) + "d" + str(d) + " : "
                    results = [random.randint(1, d) for i in range(n)];
                    rolls += str(results) + " = " + str(sum(results))  + "; "
                    if len(rolls) >= 256:
                        if private:
                            c.privmsg(nick, rolls)
                        else:
                            c.privmsg(self.channel, rolls)
                        rolls = ""
            else:
                rolls += str(1) + "d" + str(6) + " = "
                rolls += str([random.randint(1, 6)]) + "; "
            if private:
                c.privmsg(nick, rolls)
            else:
                c.privmsg(self.channel, rolls)
        elif cmd[0] == "grab":
            if len(cmd) >= 3:
                try:
                    self.db.save_quote(nick = cmd[1], index = (int(cmd[2]) - 1))
                except ValueError:
                    c.notice(nick, "Not a number: " + cmd[2])
            elif len(cmd) == 2:
                self.db.save_quote(nick = cmd[1])
            else:
                self.db.save_quote()
        elif cmd[0] == "quote":
            quote = None
            if len(cmd) >= 2:
                quote = self.db.get_random(nick=cmd[1])
            else:
                quote = self.db.get_random()
            if quote:
                msg = quote[0] + " said '" + quote[1] + "'"
                if private:
                    c.privmsg(nick, msg)
                else:
                    c.privmsg(self.channel, msg)
        else:
            self.print_help(c, nick)

    def print_help(self, c, nick):
        c.notice(nick, "Py Grabber Bot v0.2: github.com/xzaramurd/pygbot")
        c.notice(nick, "!help prints help")
        c.notice(nick, "!roll [[xd]y]... rools x dice with y faces, default 1d6")
        c.notice(nick, "!grab [user [index]] saves a line to quotes")
        c.notice(nick, "!quote [user] produces a random quote")


def sighandler(signum, frame):
    if bot != None:
        bot.stop()
    exit()

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: " + sys.argv[0] + " <server[:port]> <channel> <nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = "#" + sys.argv[2]
    nickname = sys.argv[3]


    db = QuoteDB(sys.argv[2] + '.db')
    bot = TestBot(db, channel, nickname, server, port)
    signal.signal(signal.SIGINT, sighandler)
    bot.start()

if __name__ == "__main__":
    main()
