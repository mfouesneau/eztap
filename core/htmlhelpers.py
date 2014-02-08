""" Some helpers for html code generation """

def html_bf(txt):
	return '<b>%s</b>' % txt
def html_h1(txt):
	return '\n<h1>%s</h1>\n' % txt
def html_h2(txt):
	return '\n<h2>%s</h2>\n' % txt
def html_h3(txt):
	return '\n<h3>%s</h3>\n' % txt
def html_h4(txt):
	return '\n<h4>%s</h4>\n' % txt
def html_h5(txt):
	return '\n<h5>%s</h5>\n' % txt
def html_body(txt):
	return '\n<body>\n%s\n</body>\n' % txt
def html_p(txt):
	return '\n<p>\n%s\n</p>\n' % txt
def html_pre(txt):
	return '\n<pre>\n%s\n</pre>\n' % txt
def html_em(txt):
	return '<em>%s</em>' % txt
def html_strong(txt):
	return '<strong>%s</strong>' % txt
def html_code(txt):
	return '\n<code>\n%s\n</code>\n' % txt
def html_b(txt):
	return '<b>%s</b>' % txt
def html_it(txt):
	return '<i>%s</i>' % txt
def html_link(url, txt):
	return '\n<a href="%s">%s</a>\n' % (url, txt)
def html_url(*args, **kwargs):
	return html_link(*args, **kwargs)
def html_image(url, txt, other='', link=True):
	if link:
		return '\n<a href="%s">\n<img %s src="%s" alt="%s">\n</a>\n' %(url,other, url,txt)
	else:
		return '\n<img %s src="%s" alt="%s">\n' %(other, url,txt)
def html_br():
	return '<br>\n'
def html_div(txt, other=""):
	return '\n<div %s>\n %s \n</div>' % (other, txt)

def html_list(lst, prop=''):
	txt = '<ul %s>\n' % prop
	for k in lst:
		txt += '<li>'+k+'</li>\n'
	txt += '</ul>\n'
	return txt 

def page_template(f):
	""" decorator """
	def wrapper(*args, **kwargs):

		txt = """
		<html>\n
		<head>\n
		  <link rel="Stylesheet" type="text/css" href="styles/jquery-ui-1.8.13.custom.css" />\n
		  <link rel="Stylesheet" type="text/css" href="styles/cdxmatch.css" />\n
		  <title>PHATDB</title>\n
		  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n
		  <script type="text/javascript" src="scripts/jquery-1.6.1.min.js" ></script>
		  <script type="text/javascript" src="scripts/jquery-ui-1.8.13.custom.min.js"></script>
		   <script type="text/javascript" src="scripts/jquery.dataTables.min.js"></script>
		  <script type="text/javascript" src="scripts/samp.js"></script>
		  <script type="text/javascript" src="scripts/catfs.js"></script>
		</head>\n
		<body>\n
		"""
		txt += f(*args, **kwargs)
		txt += "\n</body>\n</html>"
		return txt
	return wrapper

def block(content, title, id='infoFieldSet', prop='style="display: block;"'):

	#txt = 	"""<fieldset id="%s", class="infFieldSet"> \n""" %id
	txt = 	"""<fieldset id="%s"> \n""" %id
	txt += "<legend> %s </legend>\n" % title
	txt += content
	txt += """ \n</fieldset>\n """ 
	txt = html_div( txt, prop)
	return txt

def form(content, prop=''):
	return '\n<form %s>\n %s \n</form>\n' % (prop, content)
