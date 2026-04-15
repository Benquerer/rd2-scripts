# Cenário C - Grupo 3

### Router A
```ios
enable
configure terminal

hostname RouterA_G3
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

interface GigabitEthernet0/1
 description LAN-A
 ipv6 address 2001:690:2425:1314::1/64
 no shutdown
 exit

interface GigabitEthernet0/0
 description WAN-SWITCH-G3
 ip address 172.16.30.1 255.255.255.0
 no shutdown
 exit

! Túnel para RouterA_G1
interface Tunnel0
 description TUNEL-G3-G1
 ipv6 address 2001:690:2425:131A::1/64
 tunnel source GigabitEthernet0/0
 tunnel destination 172.16.30.3
 tunnel mode ipv6ip
 no shutdown
 exit

! Túnel para RouterB_G3
interface Tunnel1
 description TUNEL-G3A-G3B
 ipv6 address 2001:690:2425:131D::1/64
 tunnel source GigabitEthernet0/0
 tunnel destination 172.16.30.2
 tunnel mode ipv6ip
 no shutdown
 exit

! Rota para LAN C via Tunnel1
ipv6 route 2001:690:2425:1316::/64 2001:690:2425:131D::2

! Rota default para grupo do meio via Tunnel0
ipv6 route ::/0 2001:690:2425:131A::3

end
copy running-config startup-config
```
---

### Router B
```ios
enable
configure terminal

hostname RouterB_G3
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
 description WAN-SWITCH-G3
 ip address 172.16.30.2 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-C
 ipv6 address 2001:690:2425:1316::1/64
 no shutdown
 exit

! Túnel para RouterA_G3
interface Tunnel0
 description TUNEL-G3B-G3A
 ipv6 address 2001:690:2425:131D::2/64
 tunnel source GigabitEthernet0/0
 tunnel destination 172.16.30.1
 tunnel mode ipv6ip
 no shutdown
 exit

! Rota para LAN A via Tunnel0
ipv6 route 2001:690:2425:1314::/64 2001:690:2425:131D::1

! Rota default para grupo do meio via RouterA_G3
ipv6 route ::/0 2001:690:2425:131D::1

end
copy running-config startup-config
```