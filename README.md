## footloose-VPC (flvpc)

VPC by Footloose container Machines

## Dependences
--------------------
- KVM support (need the following output)
```
$ lscpu | grep Virtualization
Virtualization:      VT-x

$ lsmod | grep kvm
kvm_intel             200704  0
kvm                   593920  1 kvm_intel
```
- A host running Linux 4.14 or newer
- `sysctl net.ipv4.ip_forward=1`
- loaded kernel loop module:
  - If your kernel loads the loop module - `modprobe -v loop`
  - If the loop module is built in - `grep 'loop' /lib/modules/$(uname -r)/modules.builtin`
- Optional: `sysctl net.bridge.bridge-nf-call-iptables=0`
  - set to 0 to ignore Host iptables rules for bridges
  - set to 1 to apply Host iptables rules to bridges (common with container network policies)
  - requires kernel module `br_netfilter`
  - [libvirt reference](https://wiki.libvirt.org/page/Net.bridge.bridge-nf-call_and_sysctl.conf)
- One of the following CPUs:

| CPU   | Architecture     | Support level | Notes                                                                                                                                                                         |
|-------|------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Intel | x86_64           | Complete      | Requires <a href="https://en.wikipedia.org/wiki/X86_virtualization#Intel_virtualization_(VT-x)">VT-x</a>, most non-Atom 64-bit Intel CPUs since Pentium 4 should be supported |
| AMD   | x86_64           | Alpha         | Requires [AMD-V](https://en.wikipedia.org/wiki/X86_virtualization#AMD_virtualization_.28AMD-V.29), most AMD CPUs since the Athlon 64 "Orleans" should be supported            |
| ARM   | AArch64 (64-bit) | Alpha         | Requires GICv3, see [here](https://github.com/firecracker-microvm/firecracker/issues/1196)                                                                                    |


## Install on server
--------------------

#### Pre-requirements
1. Install Ansible in your own PC:   
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

#### Installation
1. `git clone https://github.com/sncodeGit/footloose-VPC.git`
2. `cd footloose-VPC/iac/ansible`
3. Change ip to your server and ssh-keys in **inventory.yml** (ansible_ssh_host variable) and optional add your ssh-key
4. `ansible-playbook -i inventory.yml -b main.yml`

## Usage
--------------------
Then you can go to port **5555** of your ip in the browser and administer your footloose clusters!

## Manual
--------------------

#### Users roles and namespaces
In flvpc there is such a thing as a namespace. Practically, the namespace is equal to the cluster. It's just that namespace is a more General entity. Users create a cluster in the namespace. User rights are assigned to the namespace. The name of the namespace matches the name of the cluster.   

There are three user roles in total:
- **superadmin**. On the server can be only one superadmin only. He can create the namespaces, other users and assign rights to namespaces to users.
- **namespace admin**. The namespace administrator is a user created by the superadmin. It can create, delete, and change cluster resources within the namespace. He can also access the inside of Ignite VMS by uploading him ssh key. He can also start and stop a cluster.
- **namespace user**. A regular user of a namespace cannot change cluster and non-space resources, create or delete a cluster. Otherwise, the rights are similar *namespace admin*

The same user (except for the *superadmin*) may have different rights in different namespaces.

#### SSH to virtual machines
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
--------------------

We are using this fork `https://github.com/sncodeGit/footloose`, `flvpc` branch (see releases) because v. 0.6.3 (latest ) by default have a problem with ssh to ignite backend

## Overcommitent
--------------------
Overcomitent is implemented via Ignite as follows: you can set as many resources as you want (more than there are on the host server), but they will be consumed in competition mode (the first person to "consume" them is the one who consumes them)

## IAC
--------------------
`/iac/ansible` - **Ansible** is used to install and configure: **Docker**, **Ignite**, **Fooloose**, **MySQL** (for web), **Flask** and other some python packages [see `/flask/grid`] (for web). The site code is also delivered to the server to `/usr/lib/footloose-vpc/configs`, and its launch is added to the startup via **systemd**
