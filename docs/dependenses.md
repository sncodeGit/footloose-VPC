## footloose

#### Checking for KVM support

```
$ lscpu | grep Virtualization
Virtualization:      VT-x

$ lsmod | grep kvm
kvm_intel             200704  0
kvm                   593920  1 kvm_intel
```

#### Other host Requirements

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
