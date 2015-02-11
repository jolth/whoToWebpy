# -*- coding:utf-8 -*-
import web

urls = (
    "", "re",
    "/", "dashboard"
)

render = web.template.render("templates")

# Decorador
def Session(url):
    def check(*args, **kwargs):
        """
            Decorador usado para verificar que 
            la sesión este activa.
        """
        print "Verify....", web.ctx.homepath
        try:
            if not web.ctx.session.loggedin:
                pass
                #raise web.seeother(web.ctx.homedomain) 
        except: raise web.seeother(web.ctx.homedomain)
        return url(*args, **kwargs)
    return check

class re:
    def GET(self): raise web.seeother('/')

class dashboard:
    @Session
    def GET(self):
        # you can access the session information
        web.ctx.session.count += 1
        return render.dashboard()


app_admin = web.application(urls, locals())
