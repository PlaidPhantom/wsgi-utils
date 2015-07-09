from gzip import GzipFile, compress
from io import BytesIO
 
from bottle import request, response
 
def gzip_encode(func):
    def wrapper(*args, **kargs):
 
        if "gzip" in request.get_header("Accept-Encoding") and response.get_header("Content-Encoding", None) is None:
            response.set_header("Content-Encoding", "gzip")
 
            iterator = iter(func(*args, **kargs))
 
            stream = BytesIO()
            compressor = GzipFile(fileobj = stream, mode = "wb")
 
            for data in iterator:
                compressor.write(data.encode('UTF-8'))
 
            compressor.close()
 
            return stream.getvalue()
        else:
            return func(*args, **kargs)
 
    return wrapper
