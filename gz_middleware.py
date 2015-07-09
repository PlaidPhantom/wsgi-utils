from gzip import GzipFile, compress
from io import BytesIO

def is_valid_content_type(contentType):
    return (contentType.startswith("text/") or (contentType.startswith("application/"))
             and contentType not in ("application/zip", "application/gzip", "application/octet-stream",
                                     "application/ogg", "application/x-7z-compressed", "application/x-rar-compressed"))


class GzMiddleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if "gzip" not in environ["HTTP_ACCEPT_ENCODING"]:
            return self.app(environ, start_response)

        app = { 'status': None, 'headers': None, 'exc_info': None }

        def process_response(status, headers, exc_info = None):
            (app['status'], app['headers'], app['exc_info']) = (status, headers, exc_info)


        content = self.app(environ, process_response)

        contentEncodingHeader = None
        contentTypeHeader = None
        contentLengthHeader = None

        for header in app['headers']:
            if header[0] == 'Content-Encoding':
                contentEncodingHeader = header
            elif header[0] == 'Content-Type':
                contentTypeHeader = header
            elif header[0] == 'Content-Length':
                contentLengthHeader = header

        if contentEncodingHeader is not None or not is_valid_content_type(contentTypeHeader[1])):
            start_response(app['status'], app['headers'], app['exc_info'])
            return content;

        stream = BytesIO()
        compressor = GzipFile(fileobj = stream, mode = "wb")

        for data in content:
            compressor.write(data)

        compressor.close()

        response = stream.getvalue()

        app['headers'].remove(contentLengthHeader)
        app['headers'].append(('Content-Length', str(len(response))))
        app['headers'].append(('Content-Encoding', 'gzip'))

        start_response(app['status'], app['headers'], app['exc_info'])
        return (response,)
