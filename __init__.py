"""
This python module mainly defines a Server Class.
An instance of Server will generate the webpage and the dynamical content of a
list of catalog files or eventually a database.

The webpage provides an easy interface to simple table explorations: column
selections, filters, sky search. It can display the table queries dynamically
as well as exporting them to different file formats (ASCII, CSV, FITS, JSON)
and also to SAMP servers (this webpage only implements a SAMP client).

This class handles different table input formats through the flexible ezTable
package. (https://github.com/mfouesneau/eztables)


TODO:
    * Internal Sky search (see LSD implementation)
    * Add interaction with databases: LSD, RemoteSQL, SQLite...
    * Add flexibility to makeJsonCatList:
            make it requestable stream from the javascript
            maybe store it in the object
    * Box selection is not implemented yet
"""
from .config import __author__, __version__
from .server import Server
