pyurlextractor
==============
Python script to extract URLs which match a configurable criterion.

At the moment there are two criteria:

* `data_in_anchor_matches_re`: the data in the anchor matches the regular expression.
* `hyperlink_matches_re`: the hyperlink matches the regular expression.

The configuration is read from the JSON file `config.json`, which has the following format:

```
[
  {
    "name":"<name>",
    "url":"<url>",
    "hyperlinks":[
      {
        "criterion":"<criterion>",
        "data":"<data>"
      },
      {
        "criterion":"<criterion>",
        "data":"<data>"
      },
      ...
      {
        "criterion":"<criterion>",
        "data":"<data>"
      }
    ]
  },
  {
    "name":"<name>",
    "url":"<url>",
    "hyperlinks":[
      {
        "criterion":"<criterion>",
        "data":"<data>"
      }
    ]
  },
  ...
  {
    "name":"<name>",
    "url":"<url>",
    "hyperlinks":[
      {
        "criterion":"<criterion>",
        "data":"<data>"
      }
    ]
  }
]
```

```
<criterion> ::= "data_in_anchor_matches_re" | "hyperlink_matches_re"
```

Example file: `config.json`.
