import os
import re
from string import letters

import webapp2
import jinja2

import urlparse


from validate import *

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

DEVELOPER_KEY = "AIzaSyCH9KdqfFSFeB65KOccUBM4gBor2lu0_DU"

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Counter(db.Model):
    title= db.StringProperty(required=True)
    description= db.TextProperty()
    user= db.StringProperty(required=True)
    url= db.StringProperty(required=True)
    created= db.DateTimeProperty(auto_now_add=True)
    rate = int
    
    

# pagina inicial com lista de cenas hot
class Index(BaseHandler):

    def get(self):
        query = db.GqlQuery("select * from Counter order by created desc")
        self.render("index.html", query=query)
	
    def post(self):
            stage_submit = escape_html(self.request.get("stage_submit"))
            if stage_submit:
                self.redirect('./counter/%s' %stage_submit)


# Stage 
class StageHandler(BaseHandler):
    def render_new_post(self, page, title="",
                        user="",
                        url="",
                        description="", counter=""):
        self.render(page,title=title,
                    user=user,
                    url=url,
                    description=description, counter=counter)
    def get(self, id_):
        query = db.GqlQuery("SELECT * FROM Counter where __key__ = KEY('Counter', %d)" %int(id_))
        url_data = urlparse.urlparse(query[0].url)
        query_src = urlparse.parse_qs(url_data.query)
        video = query_src["v"][0]
        self.render_new_post("stage.html", query[0].title, query[0].user, video, query[0].description, query[0])
        
# sitio para o user lancar um novo video
class NewStage(BaseHandler):
    def render_new_post(self, page, default_user="",
                        error_user="",
                        default_title="",
                        error_title="",
                        default_url="",
                        error_url="",
                        default_paypal="",
                        error_paypal="",
                        default_description="",
                        error_description=""):
        
        self.render(page, default_user=default_user,
                    error_user=error_user,
                    default_title=default_title,
                    error_title=error_title,
                    default_url=default_url,
                    error_url=error_url,
                    default_paypal=default_paypal,
                    error_paypal=error_paypal,
                    default_description=default_description,
                    error_description=error_description)
    
    def get(self):
        self.render_new_post("newpost.html")
    def post(self):
        title = escape_html(self.request.get("title"))
        user = escape_html(self.request.get("user"))
        url = escape_html(self.request.get("url"))
        paypal = escape_html(self.request.get("paypal"))
        description = escape_html(self.request.get("description"))

        
        
        if title and url and user:
            post = Counter( user=user, title=title, url=url, description=description, rate=0)
            post.put()
##            print post.key()
##            print post.key().id()

##title= db.StringProperty(required=True)
##    description= db.TextProperty()
##    user= db.StringProperty(required=True)
##    url= db.StringProperty(required=True)
##    govideo= db.LinkProperty()
##    created= db.DateTimeProperty(auto_now_add=True)
##    rate = int
##              
            self.redirect('./counter/%s' %post.key().id())
            
        else:
            default_user=""
            error_user=""
            default_title=""
            error_title=""
            default_url=""
            error_url=""
            default_paypal=""
            error_paypal=""
            default_description=""
            error_description=""                       
           
            if not title:
                error_title = "Title can't be empty."
            else:
                default_title = escape_html(title)
            if not user:
                error_user = "User can't be empty."
            else:
                default_user = escape_html(user)
                      
            if not url:
                error_url = "Title can't be empty."
            else:
                default_url = escape_html(url)
                        
                
            self.render_new_post("newpost.html", default_user,
                                 error_user,
                                 default_title,
                                 error_title,
                                 default_url,
                                 error_url,
                                 default_paypal,
                                 error_paypal,
                                 default_description,
                                 error_description)

app = webapp2.WSGIApplication([('/', Index),
                               ('/newpost', NewStage),
                               (r'/counter/(\d+)',StageHandler)],
                              debug=True)
