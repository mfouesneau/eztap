import sys, os, inspect
localpath = '/'.join(os.path.abspath(inspect.getfile(inspect.currentframe())).split('/')[:-1])
sys.path.append(localpath+'/..')
from mytap.table import Table
import mytables
from collections import OrderedDict
import jsontools
import uuid
import os, sys
import numpy as np
from StringIO import StringIO

ctypes = {      "s" : "string",
		"s#": "string",
		"b" : "integer",
		"h" : "short",
		"i" : "integer",
		"l" : "long",
		"c" : "char",
		"f" : "float",
		"d" : "double",
		"D" : "complex" }

class Backend(object):
	def __init__(self, *args, **kwargs):
		pass
	def getMeta(self, *args, **kwargs):
		""" Return the meta data of the catalog:
			cols and descriptions
		"""
		pass
	def getData(self, *args, **kwargs):
		""" Return the data from the catalog """
		pass
		
class FileBackend(Backend):
	def __init__(self, catName, *args, **kwargs):
		self.t = Table(catName)
		self.webserver_base_url = None

	def keys(self):
		return self.t.keys()

	def getColMeta(self, col):
		""" return the meta data for a given column """
		col_meta_names = [u'name', u'datatype', u'format', u'unit', u'ucd', u'description'] 
		d = OrderedDict()
		for k in col_meta_names:
			if k == u'ucd':
				d[k] = ''
			elif k == u'datatype':
				d[k] = ctypes[col.header['dtype'].char]
			elif k == u'format':
				d[k] = col.header[k] or '%' + '%s' % col.dtype.char
			elif k == u'description':
				d[k] = col.header[k] 
			else:
				d[k] = col.header[k]
		return d

	def getMeta(self):
		""" Return the meta data """
		col_meta_names = [u'name', u'datatype', u'format', u'unit', u'description'] 

		metadata = [ self.getColMeta(self.t[k]) for k in self.keys() ]
		return dict( aaData= [[ dk[k] for k in col_meta_names ] for dk in metadata ] )

	def getData(self, t, N=None):
		""" Return the data """
		if N is None:
			N = t.nrows
		else:
			N = min(t.nrows, int(N))
		d = OrderedDict()
		d['metadata'] = [ self.getColMeta(t[k]) for k in t.keys() ]
		d['data']     = [t[tk].tolist() for tk in range(N)]
		return dict( d )

	def select(self, opts):
		mode   = opts.get('mode'  , 'allsky')
		fmt    = opts.get('format', 'json'  )
		filt   = opts.get('filter', None    )
		limit  = opts.get('limit' , None    )
		cols   = opts.get('col'   , None    )
		if mode=='allsky':
			pass
		if mode=='box':
			pos    = opts.get('pos'   , None)
			width  = opts.get('width' , None)
			height = opts.get('height', None)
		if mode=='Zone':
			minRA  = opts.get('minRA' , None)
			maxRA  = opts.get('maxRA' , None)
			minDec = opts.get('minDec', None)
			maxDec = opts.get('maxDec', None)
		if mode=='cone':
			pos    = opts.get('pos'   , None)
			r      = opts.get('r'     , None)
		
		if not (cols is None):
			if filt is None:
				t = self.t.extract(fields=cols.split(','))
			else:
				t = self.t.selectWhere(filt, fields=cols.split(','))
		elif not (filt is None):
			t = self.t.selectWhere(filt)
		else:
			t = self.t

		if not limit is None:
			_l = min(t.nrows, int(limit))
		else:
			_l = t.nrows
		t = t.extract( range(int(_l)) )
		tmpfile = 'temp/'+str(uuid.uuid4())
		
		if (fmt != 'jsondt') & (fmt != 'votable'):


			if fmt == 'fits':
				tmpfile += '.fits'
			if fmt == 'csv':
				tmpfile += '.csv'
			if fmt == 'tsv':
				tmpfile += '.txt'

			t.write(tmpfile)
			return '<iframe width="1" height="1" frameborder="" src="http://%s/%s"></iframe>' % (self.webserver_base_url, tmpfile)
		elif fmt == 'votable':
			tmpfile += '.fits'
			t.write(tmpfile)
			r = open(tmpfile).read()
			os.remove(tmpfile)
			return r
			#tmpfile = StringIO()
			#t.write(tmpfile, 'fits')
			#return tmpfile.buff.read()
		else:
			return jsontools.dumps( self.getData(t, limit), nan = 'null', inf = 'null')
try:
	import lsd
	class LSDBackend(Backend):
		def __init__(self, LSDROOT, tablename):
			self.db = lsd.DB(LSDROOT)
			self.dbtablename = tablename
			self.webserver_base_url = None
			self.dbtable = self.db.table(self.dbtablename)
		
		def keys(self):
			return [k for k in self.dtype.names if k[0]!= '_']

		@property
		def dtype(self):
			return self.dbtable.dtype

		@property
		def nrows(self):
			return self.dbtable._nrows

		def getColsMeta(self, cols):
			""" return the meta data for a given set of columns """
			col_meta_names = [u'name', u'datatype', u'format', u'unit', u'ucd', u'description'] 
			meta = []
			for kn, kf in self.dtype.descr:
				if (kn in cols) or cols is None :
					d = OrderedDict()
					d['name']        = kn
					d['datatype']    = kf[1:]
					d['format']      = '%'+'%s' %kf[1]
					d['unit']        = ''
					d['ucd']         = ''
					d['description'] = ''
					meta.append(d)
			return meta

		def getData(self, r, cols):
			if cols is None:
				return dict( metadata = self.getColsMeta(self.keys()), data = r)
			else:
				return dict( metadata = self.getColsMeta(cols.split(',')), data = r)


		def getMeta(self):
			""" Return the meta data """
			col_meta_names = [u'name', u'datatype', u'format', u'unit', u'description'] 
			dt = self.dtype
			metadata = [(k[0], k[1][1:], '%'+'%s' %k[1][1], '', '') for k in
					dt.descr if k[0][0] != '_']
			return dict( aaData=metadata )

		def select(self, opts):
			mode   = opts.get('mode'  , 'allsky')
			fmt    = opts.get('format', 'json'  )
			filt   = opts.get('filter', None    )
			#TODO free the limit
			limit  = opts.get('limit' , 10      )
			cols   = opts.get('col'   , None    )
			bt = lsd.bounds.intervalset((-np.inf, np.inf))
			if mode == 'allsky':
				bounds = None
			elif mode == 'box':
				pos    = opts.get('pos'   , None)
				width  = opts.get('width' , None)
				height = opts.get('height', None)
				bound  = None 
			elif mode=='zone':
				minRA  = float(opts.get('minRA' , None))
				maxRA  = float(opts.get('maxRA' , None))
				minDec = float(opts.get('minDec', None))
				maxDec = float(opts.get('maxDec', None))
				bs = lsd.bounds.rectangle(minRA, minDec, maxRA, maxDec)
				bounds = [bs, bt]
			elif mode=='cone':
				pos    = opts.get('pos'   , None)
				r      = float(opts.get('r'     , None))
				#TODO r must be in degrees
				bs = lsd.bounds.beam(pos[0], pos[1], r) 
				bounds = [bs, bt]
			print mode
		
			query_string = 'select '
			
			if (cols is None):
				query_string += '*'
			else:
				query_string += cols 
			query_string += ' from %s ' % self.dbtablename
			if not (filt is None):
				query_string += ' where %s ' % filt

			q = self.db.query(query_string)

			if not limit is None:
				_l = min(self.nrows, int(limit))
			else:
				_l = self.nrows

			print bounds
			it = q.iterate(bounds=bounds)
			r = [ it.next().tolist() for k in range(_l) ]

			tmpfile = 'temp/'+str(uuid.uuid4())
			
			if (fmt != 'jsondt') & (fmt != 'votable'):
				t = Table(np.rec.fromrecords(r, names=cols or self.keys())) 
				if fmt == 'fits':
					tmpfile += '.fits'
				if fmt == 'csv':
					tmpfile += '.csv'
				if fmt == 'tsv':
					tmpfile += '.txt'

				t.write(tmpfile)
				return '<iframe width="1" height="1" frameborder="" src="http://%s/%s"></iframe>' % (self.webserver_base_url, tmpfile)
			elif fmt == 'votable':
				t = Table(np.rec.fromrecords(r, names=cols or self.keys())) 
				tmpfile = StringIO()
				t.write(tmpfile, 'fits')
				return tmpfile.buff.read()
			else:
				return jsontools.dumps( self.getData(r, cols), nan = 'null', inf = 'null')
except:
	pass
