# Cenário C - Grupo 5

### Router A
```ios
enable
configure terminal

hostname RouterA_G5
no ip domain-lookup
enable secret class
banner motd #Acesso restrito a pessoal autorizado!#
line console 0
 password class
 login
 exit
line vty 0 4
 password class
 login
 exit

ipv6 unicast-routing

interface GigabitEthernet0/0
 description WAN-SWITCH-G5
 ip address 172.16.50.1 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-A
 ipv6 address 2001:690:2425:1317::1/64
 no shutdown
 exit

! Túnel para RouterB_G1
interface Tunnel0
 description TUNEL-G5-G1
 ipv6 address 2001:690:2425:131B::1/64
 tunnel source GigabitEthernet0/0
 tunnel destination 172.16.50.3
 tunnel mode ipv6ip
 no shutdown
 exit

! Túnel para RouterB_G5
interface Tunnel1
 description TUNEL-G5A-G5B
 ipv6 address 2001:690:2425:131E::1/64
 tunnel source GigabitEthernet0/0
 tunnel destination 172.16.50.2
 tunnel mode ipv6ip
 no shutdown
 exit

! Rota para LAN C via Tunnel1
ipv6 route 2001:690:2425:1319::/64 2001:690:2425:131E::2

! Rota default para grupo do meio via Tunnel0
ipv6 route ::/0 2001:690:2425:131B::3

end
copy running-config startup-config
```
---

### Router B
```ios
enable
configure terminal

hostname RouterB_G5
no ip domain-lookup
enable secret class
banner motd #Acesso restrito a pessoal autorizado!#
line console 0
 password class
 login
 exit
line vty 0 4
 password class
 login
 exit

ipv6 unicast-routing

interface GigabitEthernet0/0
 description WAN-SWITCH-G5
 ip address 172.16.50.2 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-C
 ipv6 address 2001:690:2425:1319::1/64
 no shutdown
 exit

! Túnel para RouterA_G5
interface Tunnel0
 description TUNEL-G5B-G5A
 ipv6 address 2001:690:2425:131E::2/64
 tunnel source GigabitEthernet0/0
 tunnel destination 172.16.50.1
 tunnel mode ipv6ip
 no shutdown
 exit

! Rota para LAN A via Tunnel0
ipv6 route 2001:690:2425:1317::/64 2001:690:2425:131E::1

! Rota default para grupo do meio via RouterA_G5
ipv6 route ::/0 2001:690:2425:131E::1

end
copy running-config startup-config
```