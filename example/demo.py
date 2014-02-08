import webbrowser
from eztap import Server


if __name__ == '__main__':
    table_list = ['file:///cats/m83.mf2012.csv',
                  'file:///cats/PhatCl.v1.fits',
                  'file:///cats/Kang2012.tab1.fits',
                  'file:///cats/tab.profiles1d.king_res.fits'
                  ]
    root_url   = 'localhost:8877'
    server = Server(table_list, rooturl=root_url)
    webbrowser.open('http://' + root_url, new=2, autoraise=True)
    server.run(reloader=True)
