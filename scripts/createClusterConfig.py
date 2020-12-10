# Все параметры обязательно должны передаваться!!!
# Если параметр не задан - передаем None
#
# createCluster.py \
# ClusterName NodeCount NodeName NodeImage CPULimit4Node MemoryLimit4Node DiskLimit4Container KernelImage

from jinja2 import Environment, FileSystemLoader
import sys

import config as cfg

template = 'cluster.j2'
j2_vars = {
    'ClusterName': sys.argv[1],
    'NodeCount': sys.argv[2],
    'NodeName': sys.argv[3],
    'NodeImage': sys.argv[4],
    'CPULimit': sys.argv[5],
    'MemoryLimit': sys.argv[6],
    'DiskLimit': sys.argv[7],
    'KernelImage': sys.argv[8],
}
env = Environment(loader=FileSystemLoader('%s/' % cfg.DIR_PATH['templates']))
j2_template = env.get_template(template)
config = j2_template.render(j2_vars=j2_vars)
with open('%s/%s.yaml' % (cfg.DIR_PATH['clusters_dir'], sys.argv[1]), 'w') as f:
    f.write(config)
