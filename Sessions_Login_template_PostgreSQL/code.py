# -*- coding: utf-8 -*-
"""
Author: Jorge A. Toro <jolthgs@gmail.com>

Session with DBStore - Web.py 0.37

Create Database "test1" and "tsessions" table with the following schema into PostgreSQL:

$ createdb test1
$ psql -d test1

create table tsessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);

create table users (
    id serial primary key,
    username varchar(10) UNIQUE NOT NULL,
    password varchar(10)
);

insert into users (username, password) values ('jolth','qwerty');

"""
import web

# DEBUG
web.config.debug = False

# URL's
urls = (
    "/", "login",
    "/dashboard", "dashboard",
    "/logout", "logout"
)

app = web.application(urls, locals())

# Sessions
db = web.database(dbn="postgres", db="test1", user="postgres", pw="qwerty")
store = web.session.DBStore(db, "tsessions") 
session = web.session.Session(app, store, initializer={"count": 0})

# Templates
render = web.template.render("templates", globals={"session": session})

# Decorador
def Session(url):
    def check(*args, **kwargs):
        """
            Decorador usado para verificar que 
            la sesión este activa.
        """
        try:
            if not session.loggedin:
                raise web.seeother('/') 
        except: raise web.seeother('/')
        return url(*args, **kwargs)
    return check

class login:
    def GET(self):
        """
            Página de Login
        """
        return render.login()

    def POST(self):
        """
            Comprueba si el usuario se puede logear
            y crea atributos para la sesión.
        """
        import sys
        inputData = web.input()

        check = db.query("select * from users where username=$username and password=$password",
                vars=inputData)

        if check:
            session.loggedin = True 
            session.username = inputData.username
            print >> sys.stderr, "Login Successful"
            raise web.seeother("/dashboard")
        else:
            print >> sys.stderr, "Login Failed"
            return render.login("usuario o contraseña inválida")

class dashboard:
    @Session
    def GET(self):
        session.count = session.count + 1
        return render.dashboard()

class logout:
    def GET(self):
        """
            Mata la sesión
        """
        session.kill()
        return 'Logout.....'


if __name__ == "__main__": app.run()
