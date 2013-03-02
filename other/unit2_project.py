#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi # allows escaping!
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_username(username):
    return USER_RE.match(username)
def valid_password(username):
    return PASS_RE.match(username)
def valid_email(username):
    return EMAIL_RE.match(username)

form="""
<form method="post">
    <textarea name="text">%(default)s</textarea>
    <br>
    <input type="submit">
</form>
"""


def escape_html(s):
##    s= s.replace('&', "&amp;")
##    s= s.replace('>', "&gt;")
##    s= s.replace('<', "&lt;")
##    s= s.replace('"', "&quot;")
    s= cgi.escape(s, quote=True)
    return s
def rot13(s):
    character_list=list()
    for c in s:
        if (c>='A' and c<='Z'):
            character_list.append(chr(((ord(c)-65)+13)%26+65))
        elif (c>='a' and c<='z'):
            character_list.append(chr(((ord(c)-97)+13)%26+97))
        else:
            character_list.append(c)
    s="".join(character_list)
    return s
    
class MainHandler(webapp2.RequestHandler):
    def write_form(self, text=""):
        self.response.out.write(form %{"default": text})
    def get(self):
        self.write_form()
    
    def post(self):
        user_text = self.request.get('text')
        
        text= escape_html(rot13(user_text))

        self.write_form(text)

signup_form = """
<h1>Signup</h1>
<form method="post">
	<label>
	Username
		<input type="text" name="username" value="%(fodasse)s">
		<div style="color: red">%(error_user)s</div>
	</label>
	<br>
	<label>
	Password
		<input type="password" name="password">
		<div style="color: red">%(error_pass)s</div>
	</label>
	<br>
	<label>
	Verify Password
		<input type="password" name="verify">
		<div style="color: red">%(error_match)s</div>
	</label>
	<br>
	<label>
	Email (optional)
		<input type="text" name="email" value="%(fodete)s">
		<div style="color: red">%(error_email)s</div>
	</label>
		<input type="submit">
</form>
"""
        
class SignupHandler(webapp2.RequestHandler):
    def write_form(self, error_user="", error_pass="", error_match="", error_email="", default_u="", default_e="" ):
        self.response.out.write(signup_form %{"error_user": error_user, "error_pass": error_pass,
                                       "error_match": error_match,
                                       "error_email": error_email,
                                       "fodasse": default_u, "fodete": default_e})
    def get(self):
        self.write_form()
    
    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')
        bool_u=valid_username(user_username)
        bool_p=valid_password(user_password)
        bool_v=valid_password(user_verify)
        bool_e=valid_email(user_email)
        if (bool_u and bool_p and ((not user_email)or bool_e)):
            if (user_password is user_verify)or(user_password==user_verify):
                self.redirect("/welcome?username="+escape_html(user_username))
            else:
                self.write_form("", "", "Your passwords didn't match.","",escape_html(user_username), escape_html(user_email))
        elif not bool_u:
            if not bool_p:
                if not ((not user_email)or bool_e):
                    self.write_form("That's not a valid username.", "That wasn't a valid password.", "","Your e-mail is invalid",escape_html(user_username), escape_html(user_email))
                else:
                    self.write_form("That's not a valid username.", "That wasn't a valid password.", "","",escape_html(user_username), escape_html(user_email))
            elif not(user_password is user_verify or(user_password==user_verify)):
                if not ((not user_email)or bool_e):
                    self.write_form("That's not a valid username.", "", "Your passwords didn't match.","Your e-mail is invalid",escape_html(user_username), escape_html(user_email))
                else:
                    self.write_form("That's not a valid username.", "", "Your passwords didn't match.","",escape_html(user_username), escape_html(user_email))
            else:
                self.write_form("That's not a valid username.", "", "","",escape_html(user_username), escape_html(user_email))
        else:
            if not bool_p:
                if not ((not user_email)or bool_e):
                    self.write_form("", "That wasn't a valid password.", "","Your e-mail is invalid",escape_html(user_username), escape_html(user_email))
                else:
                    self.write_form("", "That wasn't a valid password.", "","",escape_html(user_username), escape_html(user_email))
            elif not(user_password is user_verify or(user_password==user_verify)):
                if not ((not user_email)or bool_e):
                    self.write_form("", "", "Your passwords didn't match.","Your e-mail is invalid",escape_html(user_username), escape_html(user_email)) 
                else:
                    self.write_form("", "", "Your passwords didn't match.","",escape_html(user_username), escape_html(user_email))
            else:
                self.write_form("That's not a valid username.", "", "","",escape_html(user_username), escape_html(user_email))
                

        

class WelcomeHandler(webapp2.RequestHandler):
    
    def get(self):
        user_username = self.request.get('username')
        self.response.out.write("Welcome, %s!" %user_username)
    
    

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/signup', SignupHandler),
                               ('/welcome', WelcomeHandler)], debug=True)

