"""
This python module defines the Server Class.
An instance of Server will generate the webpage and the dynamical content of a
list of catalog files or a database.

The webpage provides an easy interface to simple table explorations: column
selections, filters, sky search. It can display the table queries dynamically as
well as exporting them to different file formats (ASCII, CSV, FITS,
JSON) and also to SAMP servers.

This class handles different table input formats through the flexible Table
package.


TODO:
    * Internal Sky search (see LSD implementation)
    * Add interaction with databases: LSD, RemoteSQL, SQLite...
"""
import os
import inspect
#import sys
localpath = '/'.join(os.path.abspath(inspect.getfile(inspect.currentframe())).split('/')[:-1])
#sys.path.append(localpath + '/..')
import numpy as np

#Web backend
from .core.bottle import run, request, get, HTTPResponse, route, static_file

#File managements
from .eztables import AstroTable
from .eztables.astro import astrohelpers
from .eztables.backends import jsonbackend
from StringIO import StringIO
import uuid

#Local packages
from .config import __WEBSERVER__

__all__ = ['Server']


class Server(object):
    """
    An instance of Server will generate the webpage and the dynamical content
    of a list of catalog files or a database.

    The webpage provides an easy interface to simple table explorations: column
    selections, filters, sky search. It can display the table queries
    dynamically as well as exporting them to different file formats (ASCII,
    CSV, FITS, JSON) and also to SAMP servers.

    This class handles different table input formats through the flexible ezTable
    package (https://github/mfouesneau/eztable)

    Constructor arguments
    ---------------------

    table_list:  sequence
        list of sources starting with the protocol
        currently only `file:///` protocol is implemented
        e.g. ['file:///cats/demo.csv', 'file:///demo.fits']
        Note: any format that eztable handle is a valid file

    rooturl: str
        server address and port to listen to
        ``0.0.0.0`` to listens to all interfaces including the external one.
        e.g. 'localhost:8877'
        default value from config.__WEBSERVER__

    cache: bool
        if set, loads and keeps all the tables into memory
    """
    def __init__(self, table_list, rooturl=None, cache=True):
        """ Constructor
        arguments
        ---------

        table_list:  sequence
            list of sources starting with the protocol
            currently only `file:///` protocol is implemented
            e.g. ['file:///cats/demo.csv', 'file:///demo.fits']
            Note: any format that eztable handle is a valid file

        rooturl: str
            server address and port to listen to
            ``0.0.0.0`` to listens to all interfaces including the external one.
            e.g. 'localhost:8877'
            default value from config.__WEBSERVER__

        cache: bool
            if set, loads and keeps all the tables into memory
        """
        self.current_table = None
        self.table_list = table_list
        self.cache = {}
        self.rooturl = rooturl or __WEBSERVER__
        self.caching = cache
        self.catsJSON = self.makeJsonCatList()
        self.static_shares()

    def makeJsonCatList(self, *args, **kwargs):
        """
        Generates into self.catsJSON containing the list of accessible tables
        and some descriptions. It generates a JSON dumps of the dictionary that
        will be read by jQuery.
        """
        cat = {}
        cat = {}
        for k, fname in enumerate(self.table_list):
            protocol, f = fname.split(':///')
            if protocol.lower() == 'file':
                if fname not in self.cache:
                    t = AstroTable(f)
                else:
                    t = self.cache[fname]
                cat[fname] = dict(
                    id=fname,
                    name=t.header['NAME'] or f.split('/')[-1],
                    desc=t.header['COMMENT'] if 'COMMENT' in t.header.keys() else '',
                    nRows=t.nrows)
                if self.caching and fname not in self.cache:
                    print fname + ' to cache'
                    self.cache[fname] = t
                else:
                    del t
            else:
                print "Protocol %s not yet supported" % protocol
        f = StringIO()
        jsonbackend.json.dump( {'cats': cat}, f, indent=4)
        return f.getvalue()

    def getTable_fromCatName(self, catName):
        """
        Load a table from its catalog's name and protocol
        (load the catalog and keep it in memory in self.current_table)

        keywords
        --------
        catName: str
            catalog incl. protocol
            e.g.  'file:///cats/demo.csv'

        returns
        -------
        tab: AstroTable instance
            a Table of the catalog

        Note: Only file:/// supported yet. Soon lsd:/// or db:///
        """
        protocol, f = catName.split(':///')
        print catName + ' getTable'
        if catName not in self.cache:
            if protocol.lower() == 'file':
                self.current_table = tab = AstroTable(f)
                return tab
            else:
                print "Protocol %s not yet supported" % protocol
        else:
            return self.cache[catName]

    def getJsonColumnMetadata(self, catName):
        """
        Get column meta description from a catalog
        (load the catalog and keep it in memory in self.current_table)

        keywords
        --------
        catName: str
            catalog incl. protocol (e.g.  'file:///cats/demo.csv')

        returns
        -------
        stream: str
            json structure containing the metadata
        """
        tab = self.getTable_fromCatName(catName)
        bk = jsonbackend.jsonBackend()
        metadata = [ bk.writeColMeta(tab, k) for k in tab.keys() ]
        r = jsonbackend.json.dumps( dict( aaData=[  dk.values() for dk in metadata ] ), indent=4 )
        return r

    def select(self, catName, opts):
        """ Process the query of a catalog (submit pressed)

        keywords
        --------
        catName: str
            catalog incl. protocol (e.g.  'file:///cats/demo.csv')

        opts: dict
            request query arguments

        returns
        -------
        stream:  str or binary
            adapted response depending on the output format requested (webpage, fits, csv, ascii, json, SAMP...)

        Note: the box search is not implemented yet
        """
        #Default values in case of error
        mode = opts.get('mode', 'allsky' )
        fmt = opts.get('format', 'json' )
        filt = opts.get('filter', None )
        limit = opts.get('limit', None )
        cols = opts.get('col', None )
        if mode == 'allsky':
            pass

        if mode == 'box':
            pass
            #pos = opts.get('pos', None)
            #width = opts.get('width', None)
            #height = opts.get('height', None)

        zone = None
        if mode == 'zone':
            minRA = opts.get('minRA', None)
            maxRA = opts.get('maxRA', None)
            minDec = opts.get('minDec', None)
            maxDec = opts.get('maxDec', None)
            val = (minRA, maxRA, minDec, maxDec)
            if None not in val:
                zone = map(float, val)

        cone = None
        if mode == 'cone':
            pos = opts.get('pos', None)
            r = opts.get('r', None)
            if pos is not None:
                pos = pos.split(',')
                if (len(pos[0].split(':')) == 3):
                    pos[0] = np.asarray(astrohelpers.hms2deg(pos[0], delim=':'))
                elif (len(pos[0].split(' ')) == 3):
                    pos[0] = np.asarray(astrohelpers.hms2deg(pos[0], delim=' '))
                else:
                    pos[0] = float(pos[0])

                if (len(pos[1].split(':')) == 3):
                    pos[1] = np.asarray(astrohelpers.dms2deg(pos[1], delim=':'))
                elif (len(pos[1].split(' ')) == 3):
                    pos[1] = np.asarray(astrohelpers.dms2deg(pos[1], delim=' '))
                else:
                    pos[1] = float(pos[1])

            if r is not None:
                if 'mas' in r:
                    r = float(r[:-3]) * 1e-3 * 1. / 3600.
                elif 'arcsec' in r:
                    r = float(r[:-6]) * 1. / 3600.
                elif 'arcmin' in r:
                    r = float(r[:-6]) * 1. / 60.
                elif 'deg' in r:
                    r = float(r[:-3])

            if (pos is not None) & (r is not None):
                cone = (pos[0], pos[1], r)

        tab = self.getTable_fromCatName(catName)

        if cols is None:
            cols = ','.join(tab.keys())
        if filt is None:
            filt = None

        t = tab.selectWhere( cols.split(','), filt, cone=cone, zone=zone)

        if limit is not None:
            _l = min(t.nrows, int(limit))
            t.data = t[:_l]

        if (fmt != 'jsondt') & (fmt != 'votable') & (fmt != 'plot'):
            tmpfile = 'temp/' + str(uuid.uuid4())
            if fmt == 'fits':
                tmpfile += '.fits'
            elif fmt == 'csv':
                tmpfile += '.csv'
            elif fmt == 'tsv':
                tmpfile += '.txt'
            elif fmt == 'json':
                tmpfile += '.json'

            f = StringIO()
            t.write(f, fmt)
            return HTTPResponse(f.getvalue(),
                                header={'Content-Type': 'application/octet-stream',
                                        "content-disposition": "inline; filename='%s'" % tmpfile}
                                )
        elif fmt == 'votable':
            f = StringIO()
            t.write(f, 'fits')
            return f.getvalue()
        elif fmt == 'plot':
            pass
        else:
            f = StringIO()
            t.write(f, 'json', nan='null', inf='null')
            return f.getvalue()

    @get('/Plot')  # or @route('/login')
    def plot_submit(*args, **kwargs):
        pass
        #print request.query.items()

    def query_submit(self, *args, **kwargs):
        """
        Retrieve the query from the html arguments and forward to adapted
        functions.
        This function is called by the main loop of the webserver.

        Linked to route('/QueryCat')
        """
        catName = request.query.get('catName', None)

        #for k in request.query.keys():
            #print k, request.query[k]

        if 'getMeta' in request.query.keys():
            return self.getJsonColumnMetadata(catName)
        else:
            return self.select(catName, request.query)
        """
        if protocol.lower() == 'file':
            backend = cattools.FileBackend(catName)
        elif protocol.lower() == 'lsd':
            backend = cattools.LSDBackend('/home/morgan/lsd-test/', catName)
        backend.webserver_base_url = __WEBSERVER__
        """

    def run(self, reloader=True, **kwargs):
        """
        Start a server instance. This method blocks until the server terminates.

        keywords
        --------
        (any keywords of bottle.run)

        app: WSGI application or target string
            string must be supported by bottle (see bottle.py documentation)

        server: Server adapter
            See bottle documentation for valid names or `ServerAdapter` subclass.
            (default: `wsgiref`)

        host: str
            Server address to bind to. Pass ``0.0.0.0`` to listens on all
            interfaces including the external one. (default: 127.0.0.1)

        port: str
            Server port to bind to. Values below 1024 require root privileges. (default: 8080)

        reloader: bool
            Start auto-reloading server? (default: False)

        interval: int
            Auto-reloader interval in seconds (default: 1)

        quiet: bool
            Suppress output to stdout and stderr? (default: False)

        **kargs: extra options
            Options passed to the server adapter.
        """
        host, port = self.rooturl.split(':')
        run(host=host, port=port, reloader=reloader, **kwargs)

    def static_shares(self):
        """ defines the static Urls of this server instance """
        def index():
            with open('{0:s}/core/index.html'.format(localpath)) as f:
                return f.read()

        def serveCatsJSON():
            return self.catsJSON  # makeJsonCatList()

        def QueryCat(*args, **kwargs):
            return self.query_submit(*args, **kwargs)

        route('/')(route('/index.html')(index))
        route('/cats.json')(serveCatsJSON)
        get('/QueryCat')(QueryCat)  # or @route('/login')

        route('/styles/<filename>')( lambda filename: static_file(filename, root=localpath + '/styles/') )
        route('/img/<filename>')( lambda filename: static_file(filename, root=localpath + '/content/') )
        route('/templates/<filename>')( lambda filename: static_file(filename, root=localpath + '/templates/') )
        route('/content/<filename>')( lambda filename: static_file(filename, root=localpath + '/content/') )
        route('/styles/images/<filename>')( lambda filename: static_file(filename, root=localpath + '/styles/images/') )
        route('/scripts/<filename>')( lambda filename: static_file(filename, root=localpath + '/scripts/') )
        route('/cats/<filename>')( lambda filename: static_file(filename, root=localpath + '/cats/') )
        route('/temp/<filename>')( lambda filename: static_file(filename, root=localpath + '/temp/') )
