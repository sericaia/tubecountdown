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


form="""
<form method="post">
    What is your birthday?
    <br>
    <label>
    Day:
    <input type="text" name=day value="%(day)s">
    </label>
    <label>
    Month:
    <input type="text" name=month value="%(month)s">
    </label>
    <label>
    Year:
    <input type="text" name=year value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""



months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
month_abbvs = dict((m[:3].lower(), m) for m in months)
          
def valid_month(month):
    month = month.capitalize()
    if month :
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)
    return None

def test_valid_month():
    assert valid_month("january") == "January"
    assert valid_month("January") == "January"
    assert valid_month("") == None
    assert valid_month("Junk") == None

def valid_day(day):
    if day and day.isdigit():
        day=int(day)
        if (day>0 and day <= 31) :
            return day
    return None

def test_valid_day():
    
    assert valid_day('0') == None    
    assert valid_day('1') == 1
    assert valid_day('15') == 15
    assert valid_day('500') == None

def valid_year(year):
    if year and year.isdigit():
        year=int(year)
        if (year>1900 and year < 2020) :
            return year
    return None

def test_valid_year():
    
    assert valid_year('0') == None    
    assert valid_year('1') == None
    assert valid_year('1915') == 1915
    assert valid_year('2500') == None

def escape_html(s):
##    s= s.replace('&', "&amp;")
##    s= s.replace('>', "&gt;")
##    s= s.replace('<', "&lt;")
##    s= s.replace('"', "&quot;")
    s= cgi.escape(s, quote=True)
    return s
    
class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", day="", month="", year=""):
        self.response.out.write(form %{"error":error,
                                       "day":escape_html(day),
                                       "month":escape_html(month),
                                       "year":escape_html(year)})
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.write_form()
    
    def post(self):
        user_day = self.request.get('day')
        user_month = self.request.get('month')
        user_year = self.request.get('year')

        day= valid_day(user_day)
        month= valid_month(user_month)
        year= valid_year(user_year)

        if not (day and month and year):
            self.write_form("That doesn't look too valid to me", user_day, user_month, user_year)
        else:
            self.redirect("/thanks")
            
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totaly valid day!")

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/thanks', ThanksHandler)], debug=True)

