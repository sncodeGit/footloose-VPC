## footloose

#### Checking for KVM support

```
$ lscpu | grep Virtualization
Virtualization:      VT-x

$ lsmod | grep kvm
kvm_intel             200704  0
kvm                   593920  1 kvm_intel
```
