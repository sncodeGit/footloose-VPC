# footloose-VPC (flvpc)

VPC by Footloose container Machines

### Task

Создать приватное облако используя https://github.com/weaveworks/footloose ignite и overcommitment по ресурсам ( с административным интерфейсом регистрации и выделения прав пользователей, и пользовательским интерфейсом загрузки образа контейнера)

## Install
1. Install Ansible in your own PC:   
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
2. `git clone git@github.com:sncodeGit/footloose_vpc.git`
3. `cd footloose-VPC/iac/ansible`
4. Change ip to your server and ssh-keys in **inventory.yml** (ansible_ssh_host variable)
5. `ansible-playbook -i inventory.yml -b main.yml`

## Usage
Then you can go to port **5555** of your ip in the browser and administer your footloose clusters!

## Users roles and namespaces
In flvpc there is such a thing as a namespace. Practically, the namespace is equal to the cluster. It's just that namespace is a more General entity. Users create a cluster in the namespace. User rights are assigned to the namespace. The name of the namespace matches the name of the cluster.   

There are three user roles in total:
- **superadmin**. On the server can be only one superadmin only. He can create the namespaces, other users and assign rights to namespaces to users.
- **namespace admin**. The namespace administrator is a user created by the superadmin. It can create, delete, and change cluster resources within the namespace. He can also access the inside of Ignite VMS by uploading him ssh key. He can also start and stop a cluster.
- **namespace user**. A regular user of a namespace cannot change cluster and non-space resources, create or delete a cluster. Otherwise, the rights are similar *namespace admin*

The same user (except for the *superadmin*) may have different rights in different namespaces.

## SSH to virtual machines
When creating a VM, you can set the host port to be forwarded as the SSH port of the VM. By connecting via ssh to this host port (after downloading the ssh key via the panel), you will get inside the corresponding VM.

The specified host port will be the port to be forwarded for the first node of the footloose cluster. for the remaining nodes, the following hosts will be taken in order.

Then you can connect to the node using the main host as a jumpHost (for each user, a different linux user will be created on the host). You can enable the following in `.ssh/config`:
```
Host NAME
        HostName 127.0.0.1
        Port NODE_PORT
        ProxyJump USER@HOST_IP
        User root
```
Then use
```
ssh NAME
```

## Footloose version

We are using this fork `https://github.com/sncodeGit/footloose` because v. 0.6.3 by default have a problem with ssh to ignite backend

## Overcommitent
Overcomitent is implemented via Ignite as follows: you can set as many resources as you want (more than there are on the host server), but they will be consumed in competition mode (the first person to "consume" them is the one who consumes them)

## IAC
`/iac/ansible` - **Ansible** is used to install and configure: **Docker**, **Ignite**, **Fooloose**, **MySQL** (for web), **Flask** and other some python packages [see `/flask/grid`] (for web). The site code is also delivered to the server to `/usr/lib/footloose-vpc/configs`, and its launch is added to the startup via **systemd**
