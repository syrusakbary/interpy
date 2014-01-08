#!/usr/bin/env python
from __future__ import with_statement
import codecs, encodings

from .tokenizer import interpy_tokenize, interpy_untokenize
from .utils import StringIO

def interpy_transform(stream):
    try:
        output = interpy_untokenize(interpy_tokenize(stream.readline))
    except Exception as ex:
        raise ex
    return output.encode("utf-8")

def interpy_transform_string(text):
    stream = StringIO(text)
    return interpy_transform(stream)

def search_function(encoding):
    if encoding != 'interpy': return None
    # Assume utf8 encoding
    from encodings import utf_8
    utf8 = encodings.search_function('utf8')

    def interpy_decode(input, errors='strict'):
        if isinstance(input, memoryview):
            input = input.tobytes().decode("utf-8")
        return utf8.decode(interpy_transform_string(input), errors)

    class InterpyIncrementalDecoder(utf_8.IncrementalDecoder):
        def decode(self, input, final=False):
            self.buffer += input
            if final:
                buff = self.buffer
                self.buffer = ''
                return super(InterpyIncrementalDecoder, self).decode(
                    interpy_transform_string(buff), final=True)

    class InterpyStreamReader(utf_8.StreamReader):
        def __init__(self, *args, **kwargs):
            codecs.StreamReader.__init__(self, *args, **kwargs)
            self.stream = StringIO(interpy_transform(self.stream))


    return codecs.CodecInfo(
        name = 'interpy',
        encode = utf8.encode,
        decode = interpy_decode,
        incrementalencoder = utf8.incrementalencoder,
        incrementaldecoder = InterpyIncrementalDecoder,
        streamreader = InterpyStreamReader,
        streamwriter = utf8.streamwriter)

codecs.register(search_function)
