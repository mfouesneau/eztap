#ezTAP -- an easy Table access protocol webservice in python

This python module mainly defines a Server class in `server.py`.
An instance of Server will generate the webpage and the dynamical content of a list of catalog files or a database.

The webpage provides an easy interface to simple table explorations: column selections, filters, sky search. It can display the table queries dynamically as well as exporting them to different file formats (ASCII, CSV, FITS, JSON) and also to SAMP servers.

This webpage is also VO compatible and as such, direct VO compliant queries from any VO tool is supposed to work.

This class handles different table input formats through the flexible ezTable package (https://github.com/mfouesneau/eztable)


TODO:
    * Add interaction with databases: LSD, RemoteSQL, SQLite...


##Example usage
```python

import webbrowser
from eztap import Server

#list the catalogs to serve
table_list = ['file:///cats/m83.mf2012.csv',
	      'file:///cats/Kang2012.tab1.fits', ]

#configure the service
root_url   = 'localhost:8080'

#make a server instance
server = Server(table_list, rooturl=root_url)

#Open the webpage in the browser
webbrowser.open('http://' + root_url, new=2, autoraise=True)

#run
server.run()
```
