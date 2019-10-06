# discourse
## A Python wrapper of the Discourse API

[![Version](https://img.shields.io/pypi/v/discourse)](https://pypi.org/project/discourse/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This package allows Python developers to write software that makes use of the Discourse API. Functions available in the API are mirrored in this package as closely as possible, translating JSON responses to Python objects. You can find the current documentation for the Discourse API here:

[Discourse API Documentation](http://docs.discourse.org/)

### Installing

```
pip install discourse
```

### Quick Start

```python
import discourse

client = discourse.Client(
    host='http://127.0.0.1:3000/',
    api_username='discourse1',
    api_key='714552c6148e1617aeab526d0606184b94a80ec048fc09894ff1a72b740c5f19',
)

latest = client.get_latest_topics('default')

for topic in latest:
    print(topic.title)
```

Full documentation for this package is not yet available. One of the milestones is complete documentation coverage, including currently undocumented portions of the Discourse API. For now, I encourage you to read the source code and use the Discourse API docs, it should be fairly straightforward.

Pull requests welcome!
