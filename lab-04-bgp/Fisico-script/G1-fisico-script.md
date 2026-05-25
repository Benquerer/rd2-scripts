# Lab 04 — BGP em Multihomed (parte 1)
**Grupo 1 | AS 301 | G=11 | Redes de Dados II | 2025-2026**

> Versão com interface de gestão G0/2 para automação via script.

---

## Plano de Endereçamento

### Loopbacks
| Router | Interface | IP | Máscara |
|--------|-----------|-----|---------|
| R1 | Loopback0 | 10.11.1.1 | /32 |
| R2 | Loopback0 | 10.11.2.2 | /32 |
| R3 | Loopback0 | 10.11.3.3 | /32 |

### Ligações Internas
| Ligação | Rede | Router | Interface | IP |
|---------|------|--------|-----------|-----|
| R1 — R3 | 10.11.13.0/30 | R1 | G0/1 | 10.11.13.1 |
| R1 — R3 | 10.11.13.0/30 | R3 | G0/0 | 10.11.13.2 |
| R2 — R3 | 10.11.23.0/30 | R2 | G0/1 | 10.11.23.1 |
| R2 — R3 | 10.11.23.0/30 | R3 | G0/1 | 10.11.23.2 |

### Ligações Externas
| Ligação | Rede | Router | Interface | IP |
|---------|------|--------|-----------|-----|
| R1 — AS100 | 172.100.100.0/24 | R1 | G0/0 | 172.100.100.11 |
| R2 — AS200 | 172.200.200.0/24 | R2 | G0/0 | 172.200.200.11 |

### Gestão (G0/2)
| Router | Interface | IP | Máscara |
|--------|-----------|-----|---------|
| R1 | G0/2 | 192.168.0.11 | /24 |
| R2 | G0/2 | 192.168.0.12 | /24 |
| R3 | G0/2 | 192.168.0.13 | /24 |

---

## FASE 1 — Config mínima (aplicar manualmente via consola)

### R1
```ios
configure terminal
interface GigabitEthernet0/2
 ip address 192.168.0.11 255.255.255.0
 no shutdown
ip domain-name lab.local
crypto key generate rsa modulus 1024
ip ssh version 2
username admin privilege 15 secret class
line vty 0 15
 login local
 transport input ssh
end
copy running-config startup-config
```

### R2
```ios
configure terminal
interface GigabitEthernet0/2
 ip address 192.168.0.12 255.255.255.0
 no shutdown
ip domain-name lab.local
crypto key generate rsa modulus 1024
ip ssh version 2
username admin privilege 15 secret class
line vty 0 15
 login local
 transport input ssh
end
copy running-config startup-config
```

### R3
```ios
configure terminal
interface GigabitEthernet0/2
 ip address 192.168.0.13 255.255.255.0
 no shutdown
ip domain-name lab.local
crypto key generate rsa modulus 1024
ip ssh version 2
username admin privilege 15 secret class
line vty 0 15
 login local
 transport input ssh
end
copy running-config startup-config
```

---

## FASE 2 — Config completa (aplicada pelo script)

### R1
```ios
configure terminal
hostname R1
no ip domain-lookup
enable secret class
banner motd #Acesso autorizado apenas.#
line console 0
 password class
 login
line vty 0 15
 password class
 login
service password-encryption

interface Loopback0
 ip address 10.11.1.1 255.255.255.255

interface GigabitEthernet0/0
 ip address 172.100.100.11 255.255.255.0
 no shutdown

interface GigabitEthernet0/1
 ip address 10.11.13.1 255.255.255.252
 no shutdown

ip route 10.11.0.0 255.255.0.0 Null0

ip access-list standard FILTER-BGP
 deny 110.110.0.0 0.0.255.255
 permit any

route-map BGP-TO-OSPF permit 10
 match ip address FILTER-BGP

route-map SET-LOCAL-PREF permit 10
 set local-preference 200

router ospf 1
 router-id 10.11.1.1
 auto-cost reference-bandwidth 1000
 network 10.11.1.1 0.0.0.0 area 0
 network 10.11.13.0 0.0.0.3 area 0
 redistribute bgp 301 subnets route-map BGP-TO-OSPF
 redistribute connected subnets

router bgp 301
 bgp router-id 10.11.1.1
 neighbor 10.11.2.2 remote-as 301
 neighbor 10.11.2.2 update-source Loopback0
 neighbor 10.11.2.2 next-hop-self
 neighbor 172.100.100.100 remote-as 100
 neighbor 172.100.100.100 route-map SET-LOCAL-PREF in
 network 10.11.0.0 mask 255.255.0.0
 maximum-paths 2

end
copy running-config startup-config
```

### R2
```ios
configure terminal
hostname R2
no ip domain-lookup
enable secret class
banner motd #Acesso autorizado apenas.#
line console 0
 password class
 login
line vty 0 15
 password class
 login
service password-encryption

interface Loopback0
 ip address 10.11.2.2 255.255.255.255

interface GigabitEthernet0/0
 ip address 172.200.200.11 255.255.255.0
 no shutdown

interface GigabitEthernet0/1
 ip address 10.11.23.1 255.255.255.252
 no shutdown

ip route 10.11.0.0 255.255.0.0 Null0

ip access-list standard FILTER-BGP
 deny 110.110.0.0 0.0.255.255
 permit any

route-map BGP-TO-OSPF permit 10
 match ip address FILTER-BGP

route-map SET-LOCAL-PREF-LOW permit 10
 set local-preference 50

route-map AS-PATH-PREPEND permit 10
 set as-path prepend 301 301

router ospf 1
 router-id 10.11.2.2
 auto-cost reference-bandwidth 1000
 network 10.11.2.2 0.0.0.0 area 0
 network 10.11.23.0 0.0.0.3 area 0
 redistribute bgp 301 subnets route-map BGP-TO-OSPF
 redistribute connected subnets

router bgp 301
 bgp router-id 10.11.2.2
 neighbor 10.11.1.1 remote-as 301
 neighbor 10.11.1.1 update-source Loopback0
 neighbor 10.11.1.1 next-hop-self
 neighbor 172.200.200.100 remote-as 200
 neighbor 172.200.200.100 route-map SET-LOCAL-PREF-LOW in
 neighbor 172.200.200.100 route-map AS-PATH-PREPEND out
 network 10.11.0.0 mask 255.255.0.0
 maximum-paths 2

end
copy running-config startup-config
```

### R3
```ios
configure terminal
hostname R3
no ip domain-lookup
enable secret class
banner motd #Acesso autorizado apenas.#
line console 0
 password class
 login
line vty 0 15
 password class
 login
service password-encryption

interface Loopback0
 ip address 10.11.3.3 255.255.255.255

interface GigabitEthernet0/0
 ip address 10.11.13.2 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 ip address 10.11.23.2 255.255.255.252
 no shutdown

router ospf 1
 router-id 10.11.3.3
 auto-cost reference-bandwidth 1000
 network 10.11.3.3 0.0.0.0 area 0
 network 10.11.13.0 0.0.0.3 area 0
 network 10.11.23.0 0.0.0.3 area 0

end
copy running-config startup-config
```

---

## FASE 1 — AS100 e AS200 (aplicar manualmente via consola)

### AS100
```ios
configure terminal
interface GigabitEthernet0/2
 ip address 192.168.0.100 255.255.255.0
 no shutdown
ip domain-name lab.local
crypto key generate rsa modulus 1024
ip ssh version 2
username admin privilege 15 secret class
line vty 0 15
 login local
 transport input ssh
end
copy running-config startup-config
```

### AS200
```ios
configure terminal
interface GigabitEthernet0/2
 ip address 192.168.0.200 255.255.255.0
 no shutdown
ip domain-name lab.local
crypto key generate rsa modulus 1024
ip ssh version 2
username admin privilege 15 secret class
line vty 0 15
 login local
 transport input ssh
end
copy running-config startup-config
```

---

## FASE 2 — AS100 e AS200 (aplicada pelo script)

### AS100
```ios
configure terminal
hostname AS100
no ip domain-lookup

interface Loopback0
 ip address 100.100.11.1 255.255.255.240

interface Loopback1
 ip address 100.100.11.17 255.255.255.240

interface GigabitEthernet0/0
 ip address 172.100.100.100 255.255.255.0
 no shutdown

interface GigabitEthernet0/1
 ip address 192.168.2.1 255.255.255.252
 no shutdown

router bgp 100
 bgp router-id 100.100.100.100
 neighbor 172.100.100.11 remote-as 301
 neighbor 172.100.100.12 remote-as 302
 neighbor 172.100.100.13 remote-as 303
 neighbor 172.100.100.14 remote-as 304
 neighbor 172.100.100.15 remote-as 305
 neighbor 172.100.100.16 remote-as 306
 neighbor 192.168.2.2 remote-as 200
 network 100.100.11.0 mask 255.255.255.240
 network 100.100.11.16 mask 255.255.255.240

end
copy running-config startup-config
```

### AS200
```ios
configure terminal
hostname AS200
no ip domain-lookup

interface Loopback0
 ip address 200.200.11.1 255.255.255.240

interface Loopback1
 ip address 200.200.11.17 255.255.255.240

interface GigabitEthernet0/0
 ip address 172.200.200.100 255.255.255.0
 no shutdown

interface GigabitEthernet0/1
 ip address 192.168.2.2 255.255.255.252
 no shutdown

router bgp 200
 bgp router-id 200.200.200.200
 neighbor 172.200.200.11 remote-as 301
 neighbor 172.200.200.12 remote-as 302
 neighbor 172.200.200.13 remote-as 303
 neighbor 172.200.200.14 remote-as 304
 neighbor 172.200.200.15 remote-as 305
 neighbor 172.200.200.16 remote-as 306
 neighbor 192.168.2.1 remote-as 100
 network 200.200.11.0 mask 255.255.255.240
 network 200.200.11.16 mask 255.255.255.240

end
copy running-config startup-config
```
