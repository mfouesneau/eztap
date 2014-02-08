import json
from json.encoder import *

class Encoder(json.JSONEncoder):

   float_specials = dict( nan = 'NaN', inf = 'Infinity', neginf = '-Infinity')

   def set_float_specials(self, nan = None, inf = None):
	""" Set how to parse special values """
	if not (nan is None):
		self.float_specials['nan'] = str(nan)
	if not (inf is None):
		self.float_specials['inf'] = str(inf)
		self.float_specials['neginf'] = '-'+str(inf)

   def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
	_one_shot = False
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = encode_basestring_ascii
        else:
            _encoder = encode_basestring
        if self.encoding != 'utf-8':
            def _encoder(o, _orig_encoder=_encoder, _encoding=self.encoding):
                if isinstance(o, str):
                    o = o.decode(_encoding)
                return _orig_encoder(o)

        def floatstr(o, allow_nan=self.allow_nan,
                _repr=FLOAT_REPR, _inf=INFINITY, _neginf=-INFINITY):
            # Check for specials.  Note that this type of test is processor
            # and/or platform-specific, so do tests which don't depend on the
            # internals.

            if o != o:
                text = self.float_specials['nan']
            elif o == _inf:
                text = self.float_specials['inf']
            elif o == _neginf:
                text = self.float_specials['neginf']
            else:
                return _repr(o)

            if not allow_nan:
                raise ValueError( "Out of range float values are not JSON compliant: " + repr(o))

            return text

        if (_one_shot and c_make_encoder is not None
                and self.indent is None and not self.sort_keys):
            _iterencode = c_make_encoder(
                markers, self.default, _encoder, self.indent,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, self.allow_nan)
        else:
            _iterencode = json.encoder._make_iterencode(
                markers, self.default, _encoder, self.indent, floatstr,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, _one_shot)
        return _iterencode(o, 0)

def dumps(obj, nan=None, inf=None):
	enc = Encoder()
	enc.set_float_specials(nan=nan, inf=inf)
	return enc.encode(obj)
	
