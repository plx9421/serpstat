import io
import zipfile
import xmltodict


class ResponseBase():
    _content = None
    _raw = None

    def __init__(self, response):
        self._response = response

    @property
    def content(self):
        if self._response is not None:
            if self._content is None:
                self._content = ''

            try:
                if self._response.content:
                    if self._response.headers is not None:
                        contentType = self._response.headers.get('Content-Type', '')
                        if ('json' in contentType) or ('text/html' in contentType):
                            self._content = self._response.json()
                        elif 'application/zip' in contentType:
                            self._content = zipfile.ZipFile(io.BytesIO(self._response.content))
                        elif 'text/xml' in contentType:
                            self._content = xmltodict.parse(xml_input=self._response.content)
                        else:
                            self._content = self._response.content
            except:
                self._content = ''

        return self._content

    @property
    def status_code(self):
        if self._response is not None:
            return self._response.status_code

    @property
    def reason(self):
        if self._response is not None:
            return self._response.reason

    @property
    def raw(self):
        if self._response is not None:
            return self._response.content

    @property
    def header(self):
        if self._response is not None:
            return self._response.headers

    @property
    def fromXML(self):
        if self._response is not None:
            return xmltodict.parse(xml_input=self._response.content)
