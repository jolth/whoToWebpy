# -*- coding: utf-8 -*-
"""
Author: Jorge A. Toro <jolthgs@gmail.com>

Session with Sub-App and DBStore - Web.py 0.37

Create Database "test1" and "tsessions" table with the following schema into PostgreSQL:

$ createdb test1
$ psql -d test1

create table tsessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);

create table privileges (
        id SERIAL,
        name VARCHAR(50) NOT NULL UNIQUE,
        PRIMARY KEY (id)
);

create table users (
    id serial primary key,
    username varchar(10) UNIQUE NOT NULL,
    password varchar(10),
    privilege_id INTEGER NOT NULL
);

ALTER TABLE users ADD CONSTRAINT privilege_id_fk FOREIGN KEY (privilege_id) 
REFERENCES privileges(id) MATCH FULL ON UPDATE CASCADE ON DELETE SET NULL;

insert into privileges (name) values ('admin');
insert into users (username, password, privilege_id) values ('jolth','qwerty', 1);

"""
import web
import admin # Import Sub-App

# DEBUG
web.config.debug = False

# URL's
urls = (
    "/", "login",
    "/dashboard", "dashboard",
    "/logout", "logout",
    "/admin", admin.app_admin # Admin Application
)

app = web.application(urls, locals())

# Sessions
db = web.database(dbn="postgres", db="test1", user="postgres", pw="qwerty")
store = web.session.DBStore(db, "tsessions") 
session = web.session.Session(app, store, initializer={"count": 0})

# Templates
render = web.template.render("templates", globals={"session": session})

# processor (web.loadhook)
def session_hook():
    """
        Permite compartir la sesión a la 
        Sub-App.
    """
    web.ctx.session = session
    web.template.Template.globals['session'] = session # sessions avaible in template

app.add_processor(web.loadhook(session_hook))


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
            raise web.seeother("/admin") # call sub-app admin dashboard
        else:
            print >> sys.stderr, "Login Failed"
            return render.login("usuario o contraseña inválida")

class logout:
    def GET(self):
        """
            Mata la sesión
        """
        #session.loggedin = False
        session.kill()
        return 'Logout.....'


if __name__ == "__main__": app.run()
