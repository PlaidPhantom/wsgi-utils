# wsgi-utils
Various useful WSGI-related tools


## gz_middleware.py

A WSGI middleware layer that GZips responses when the client indicates it supports GZip.
Content type detection is pretty dumb right now: it will try to compress anything in the
"text/" or "application/" MIME type namespaces right now, with some obvious exceptions I
pulled off of Wikipedia.

## gz_attribute.py

This is a Bottle-specific decorator that can be added to routes to cause their contents to
be GZipped.  It has no MIME detection, so only use it on routes that will actually
benefit from compression.
