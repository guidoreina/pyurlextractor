#!/usr/bin/env python3

from enum import Enum
import re

class Hyperlink:
  class MatchCriterion(Enum):
    DATA_IN_ANCHOR_MATCHES_RE = 1
    HYPERLINK_MATCHES_RE = 2

  def __init__(self, criterion, pattern):
    """ Constructor. """
    self.criterion = criterion
    self.re = re.compile(pattern)

  def match(self, string):
    if self.re.match(string):
      return True
    else:
      return False
