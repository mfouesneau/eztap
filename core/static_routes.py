""" Define static routes for the server """
from bottle import route, static_file


@route('/styles/<filename>')
def server_static(filename):
    return static_file(filename, root='./styles/')


@route('/img/<filename>')
def server_static(filename):
    return static_file(filename, root='./content/')


@route('/templates/<filename>')
def server_static(filename):
    return static_file(filename, root='./templates/')


@route('/content/<filename>')
def server_static(filename):
    return static_file(filename, root='./content/')


@route('/styles/images/<filename>')
def server_static(filename):
    return static_file(filename, root='./styles/images/')


@route('/scripts/<filename>')
def server_static(filename):
    return static_file(filename, root='./scripts/')


@route('/cats/<filename>')
def server_static(filename):
    return static_file(filename, root='./cats/')


@route('/temp/<filename>')
def server_static(filename):
    return static_file(filename, root='./temp/')
