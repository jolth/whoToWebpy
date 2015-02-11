# -*- coding: utf-8 -*-
"""
Session with DBStore

Create Database "test1" and "tsessions" table with the following schema:

$ createdb test1
$ psql -d test1

create table tsessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);

"""
import web

web.config.debug = False

urls = (
    "/count", "count",
    "/reset", "reset"
)

app = web.application(urls, locals())

db = web.database(dbn="postgres", db="test1", user="postgres", pw="p0HWU4kA")
store = web.session.DBStore(db, 'tsessions') 

session = web.session.Session(app, store, initializer={'count': 0})

class count:
    def GET(self):
        session.count = session.count + 1
        return str(session.count)

class reset:
    def GET(self):
        session.kill()
        return ""


if __name__ == "__main__": app.run()
