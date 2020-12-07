I would like to build a Twitter clone with an html front-end and a Flask back-end, probably hosted on Heroku.  Users will be able to access a html website where they can view previously-posted tweets and post new tweets.  Previously-posted tweets will be stored in json format.  I may have user provide inputs through the html page and/or provide inputs through the terminal.

I'll use json to allow data to persist across Twitter sessions.  I'll use flask for the back-end and to help build a simple API for the front-end to interact with.  I'll use requests to POST and GET from the back-end to populate the front-end.  I'll have a main method for my server and a str method for my Tweet class, both being magic methods.
- One non-trivial first-party module (modules that come built-in with python)
  - I'm planning to use json.  Maybe argparse as well.
- Two non-trivial third-party modules (modules that need to be installed) 
  - I'm planning to use flask and requests.