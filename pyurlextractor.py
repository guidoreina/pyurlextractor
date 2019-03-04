#!/usr/bin/env python3

from sys import exit
import json
import urllib.request
import urllib.parse
from hyperlink_finder import HyperlinkFinder
from hyperlink import Hyperlink


########################################
########################################
##                                    ##
## Constants.                         ##
##                                    ##
########################################
########################################

# Name of the configuration file.
CONFIG_FILE = "config.json"

# Timeout for the HTTP requests (in seconds).
TIMEOUT = 5


########################################
########################################
##                                    ##
## main.                              ##
##                                    ##
########################################
########################################

# Load configuration file.
try:
  with open(CONFIG_FILE) as f:
    entries = json.load(f)
except Exception as e:
  print("Error loading configuration file '",
        CONFIG_FILE,
        "' (error: '",
        e,
        "').",
        sep = "")

  sys.exit(1)

# For each entry...
for entry in entries:
  # Sanity check.
  if ("name" in entry) and \
     ("url" in entry) and \
     ("hyperlinks" in entry):
    # Save name of the entry.
    name = entry["name"]

    # Save entry's URL.
    main_url = entry["url"]

    # URL to visit next.
    next_url = main_url

    # Save hyperlinks.
    hyperlinks = entry["hyperlinks"]

    # For each hyperlink to be found...
    for idx in range(len(hyperlinks)):
      hyperlink = hyperlinks[idx]

      # Sanity check.
      if ("criterion" in hyperlink) and \
         ("data" in hyperlink) and \
         ((hyperlink["criterion"] == "data_in_anchor_matches_re") or \
          (hyperlink["criterion"] == "hyperlink_matches_re")):
        # Make HTTP request.
        try:
          with urllib.request.urlopen(next_url) as f:
            content = f.read().decode('utf-8')
        except Exception as e:
          print("Error opening URL '",
                next_url,
                "' (error: '",
                e,
                "').",
                sep = "")

          break

        if hyperlink["criterion"] == "data_in_anchor_matches_re":
          criterion = Hyperlink.MatchCriterion.DATA_IN_ANCHOR_MATCHES_RE
        else:
          criterion = Hyperlink.MatchCriterion.HYPERLINK_MATCHES_RE

        hyperlink_finder = HyperlinkFinder(Hyperlink(criterion,
                                                     hyperlink["data"]))

        # Parse HTML.
        hyperlink_finder.feed(content)

        # If at least one hyperlink has been found...
        if len(hyperlink_finder.urls) > 0:
          # If not the last hyperlink...
          if idx + 1 < len(hyperlinks):
            tmpurl = hyperlink_finder.urls[0][1]

            # Absolute URL?
            if (tmpurl.startswith("http://")) or \
               (tmpurl.startswith("https://")):
              next_url = tmpurl
            else:
              next_url = urllib.parse.urljoin(next_url, tmpurl)
          else:
            print("Name: '", name, "':", sep = "")

            for data, url in hyperlink_finder.urls:
              if (not url.startswith("http://")) and \
                 (not url.startswith("https://")):
                url = urllib.parse.urljoin(next_url, url)

              print("  Data: '", data, "'", sep = "")
              print("    URL: '", url, "'.", sep = "")
        else:
          print("No hyperlinks found for URL '", url, "'.")
          break
