from jinja2 import Environment, FileSystemLoader
import sys

# Import config.py
with open('/etc/footloose-vpc/footloose-vpc.conf') as f:
    config_path = f.read().split('\n')[0]
sys.path.insert(0, config_path)
import config as cfg

# Import modules
import html

def print_j2_template(template, j2_vars):
    html.print_html()
    env = Environment(loader=FileSystemLoader('%s/' % cfg.DIR_PATH['templates']))
    j2_html = env.get_template(template)
    rendered_html = j2_html.render(j2_vars=j2_vars)
    print(rendered_html)
