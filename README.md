# snap-http

![check](https://github.com/perfect5th/snap-http/actions/workflows/test.yml/badge.svg)

snap-http is a Python library used to interact with snapd's REST API, allowing you to
programmatically install and manage snaps in your Python applications. It has no dependencies
other than Python 3.8 or higher.

*N.B.: snap-http is in **very** early development, the API is currently unstable and is subject to
change.*

## Installation

You can install snap-http directly from here! I'm planning to publish it to PYPI as soon as I'm
done the test-suite (sorry I didn't do TDD, we can't all be perfect).

```bash
pip install git+https://github.com/Perfect5th/snap-http.git
```

## Usage

Take a look at the [api](https://github.com/Perfect5th/snap-http/blob/main/snap_http/api.py) module
to see what methods are available. Here's a couple examples:

### List installed snaps

```python3
>>> import snap_http
>>> response = snap_http.list()
>>> for snap in response.result:
...     print(snap["name"])
juju
snapd
core20
snapcraft
snap-store
<etc>
```

### Install a snap

Most actual changes to snaps happen asynchronously, so you need to check back on the change using
the change ID if you want to know the final result.

*N.B.: installation may require root permissions.*

```python3
>>> import snap_http
>>> response = snap_http.install("hello")
>>> response
SnapdResponse(type='async', status_code=202, status='Accepted', result=None, sources=None, change='1395')
>>> response = snap_http.check_change(response.change)
>>> response.result["status"]
'Done'
```
