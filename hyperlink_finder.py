#!/usr/bin/env python3

import urllib.request
from html.parser import HTMLParser
from hyperlink import Hyperlink

class HyperlinkFinder(HTMLParser):
  def __init__(self, hyperlink):
    """ Constructor. """

    # Class constructor of the base class.
    HTMLParser.__init__(self)

    # Save hyperlink.
    self.hyperlink = hyperlink

    self.inside_hyperlink = False

    self.data = ""
    self.url = ""

    self.urls = []

  def handle_starttag(self, tag, attrs):
    # Hyperlink?
    if tag == "a":
      # Search "href" attribute.
      for attr in attrs:
        if attr[0] == "href":
          if (self.hyperlink.criterion ==
              Hyperlink.MatchCriterion.DATA_IN_ANCHOR_MATCHES_RE) or \
              (self.hyperlink.match(attr[1])):
            # Save URL.
            self.url = attr[1]

            self.inside_hyperlink = True

            break

  def handle_endtag(self, tag):
    # If we are inside a hyperlink...
    if self.inside_hyperlink:
      self.inside_hyperlink = False

  def handle_data(self, data):
    # If we are inside a hyperlink...
    if self.inside_hyperlink:
      # Strip data.
      data = data.strip()

      if (self.hyperlink.criterion ==
          Hyperlink.MatchCriterion.HYPERLINK_MATCHES_RE) or \
         (self.hyperlink.match(data)):
        if not self.has_url():
          # Add pair (data, URL).
          self.urls.append((data, self.url))

  def has_url(self):
    for _, url in self.urls:
      if url == self.url:
        return True

    return False
