# footloose-VPC
VPC by Footloose container Machines

### Task

Создать приватное облако используя https://github.com/weaveworks/footloose ignite и overcommitment по ресурсам ( с административным интерфейсом регистрации и выделения прав пользователей, и пользовательским интерфейсом загрузки образа контейнера)

### DelMe

Для экспериментов создан виртуальный сервер `selfmade-vpc-jason`:   
IP - 188.68.219.26

**Using Ubuntu 18.04**

## Install
1. Install Ansible in your own PC:   
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
2. `git clone git@github.com:sncodeGit/footloose-VPC.git`
3. `cd footloose-VPC/iac/ansible`
4. Change ip to your server ip in **inventory.yml** (ansible_ssh_host variable)
5. `ansible-playbook -i inventory.yml -b main.yml`
