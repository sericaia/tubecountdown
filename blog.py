import os
import re
from string import letters

import webapp2
import jinja2

from validate import *

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Post(db.Model):
    subject= db.StringProperty(required=True)
    content= db.TextProperty()
    created= db.DateTimeProperty(auto_now_add=True)
    


class Index(BaseHandler):

    def get(self):
        query = db.GqlQuery("select * from Post order by created desc")
        self.render("index.html", query=query)

class PostHandler(BaseHandler):
    def render_new_post(self, page, subject="",
                        content="",
                        creation=""):
        self.render(page, subject=subject,
                    content=content,
                    creation=creation)
    def get(self, id_):
        query = db.GqlQuery("SELECT * FROM Post where __key__ = KEY('Post', %d)" %int(id_))
        self.render_new_post("permalink.html", query[0].subject, query[0].content, query[0].created)
        

class NewPost(BaseHandler):
    def render_new_post(self, page, default_subject="",
                        error_subject="",
                        default_content="",
                        error_content=""):
        self.render(page, default_subject=default_subject,
                    error_subject=error_subject,
                    default_content=default_content,
                    error_content=error_content)
    
    def get(self):
        self.render_new_post("newpost.html")
    def post(self):
        subject = escape_html(self.request.get("subject"))
        content = escape_html(self.request.get("content"))

        if subject and content:
            post = Post(subject=subject, content=content)
            post.put()
##            print post.key()
##            print post.key().id()
            self.redirect('./%s' %post.key().id())
            
        else:
            error_subject=""
            error_content=""
            default_subject=""
            default_content=""
            if not subject:
                error_subject = "Subject can't be empty."
            else:
                default_subject = escape_html(subject)
            if not content:
                error_content = "Content can't be empty."
            else:
                default_content = escape_html(content)
                
            self.render_new_post("newpost.html", default_subject, error_subject, default_content, error_content)

app = webapp2.WSGIApplication([('/blog', Index),
                               ('/blog/newpost', NewPost),
                               (r'/blog/(\d+)',PostHandler)],
                              debug=True)
