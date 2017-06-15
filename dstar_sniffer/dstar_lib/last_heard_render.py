import jinja2
import os

def render(tpl_path, context):
	path, filename = os.path.split(tpl_path)
	return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename).render(context)

def render_last_heard_html(last_heard):
	return render('/etc/dstar_sniffer/last_heard.html', { 'last_heard' : last_heard })

