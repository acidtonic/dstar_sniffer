import jinja2
import os

def render(tpl_path, context):
	path, filename = os.path.split(tpl_path)
	return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename).render(context)

def render_last_heard_html(last_heard):
	sorted_last_heard = {}
	for cs in sorted(last_heard, key=lambda name: last_heard[name]['time'], reverse=True):
		sorted_last_heard[cs] = last_heard[cs]
	return render('/etc/dstar_sniffer/last_heard.html', { 'last_heard' : sorted_last_heard })

