# -*- coding:utf-8 -*-
import web

urls = (
    "", "re",
    "/(.*)", "dashboard"
)

render = web.template.render("templates")

# Decorador
def Session(url):
    def check(*args, **kwargs):
        """
            Decorador usado para verificar que 
            la sesión este activa.
        """
        print "Verificate session"
        try:
            if not session.loggedin:
                raise web.seeother('/') 
        except: raise web.seeother('/')
        return url(*args, **kwargs)
    return check

class re:
    def GET(self): raise web.seeother('/')

class dashboard:
    #@Session
    def GET(self, path):
        # you can access the session information
        web.ctx.session.count += 1
        #return web.ctx.session.count
        return render.dashboard()


        #session.count = session.count + 1
        #return session.count
        #return render.dashboard()
        #return "adentro " + path

app_admin = web.application(urls, locals())
