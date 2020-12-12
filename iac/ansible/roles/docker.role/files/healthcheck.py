#!/usr/bin/env python3
import docker
base_url='unix://var/run/docker.sock'
d = docker.DockerClient(base_url=base_url)
for container in d.containers.list(all):
     if 'Health' in  container.attrs['State'] :   
         if (container.attrs['State']['Health']['Status'] == 'unhealthy') :
             #print (container.attrs['State']['Health']['Status'], container.short_id, 'reboot')
             container.restart()