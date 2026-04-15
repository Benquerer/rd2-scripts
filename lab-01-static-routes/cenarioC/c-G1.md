# Cenário C - Grupo 1

### Router A
```ios
enable
configure terminal

hostname RouterA_G1
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
 description WAN-G1
 ip address 172.16.10.1 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-A
 ipv6 address 2001:690:2425:1311::1/64
 no shutdown
 exit

interface GigabitEthernet0/2
 description WAN-SWITCH-G3
 ip address 172.16.30.3 255.255.255.0
 no shutdown
 exit

! Túnel para RouterA_G3
interface Tunnel0
 description TUNEL-G1-G3
 ipv6 address 2001:690:2425:131A::3/64
 tunnel source GigabitEthernet0/2
 tunnel destination 172.16.30.1
 tunnel mode ipv6ip
 no shutdown
 exit

! Túnel para RouterB_G1
interface Tunnel1
 description TUNEL-G1A-G1B
 ipv6 address 2001:690:2425:131C::1/64
 tunnel source GigabitEthernet0/0
 tunnel destination 172.16.10.2
 tunnel mode ipv6ip
 no shutdown
 exit

! Rota para LAN C G1 via Tunnel1
ipv6 route 2001:690:2425:1313::/64 2001:690:2425:131C::2

! Rotas para redes G3 via Tunnel0
ipv6 route 2001:690:2425:1314::/64 2001:690:2425:131A::1
ipv6 route 2001:690:2425:1316::/64 2001:690:2425:131A::1

! Rotas para redes G5 via Tunnel1
ipv6 route 2001:690:2425:1317::/64 2001:690:2425:131C::2
ipv6 route 2001:690:2425:1319::/64 2001:690:2425:131C::2

end
copy running-config startup-config
```
---

### Router B
```ios
enable
configure terminal

hostname RouterB_G1
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
 description WAN-G1
 ip address 172.16.10.2 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-C
 ipv6 address 2001:690:2425:1313::1/64
 no shutdown
 exit

interface GigabitEthernet0/2
 description WAN-SWITCH-G5
 ip address 172.16.50.3 255.255.255.0
 no shutdown
 exit

! Túnel para RouterA_G1
interface Tunnel0
 description TUNEL-G1B-G1A
 ipv6 address 2001:690:2425:131C::2/64
 tunnel source GigabitEthernet0/0
 tunnel destination 172.16.10.1
 tunnel mode ipv6ip
 no shutdown
 exit

! Túnel para RouterA_G5
interface Tunnel1
 description TUNEL-G1-G5
 ipv6 address 2001:690:2425:131B::3/64
 tunnel source GigabitEthernet0/2
 tunnel destination 172.16.50.1
 tunnel mode ipv6ip
 no shutdown
 exit

! Rota para LAN A G1 via Tunnel0
ipv6 route 2001:690:2425:1311::/64 2001:690:2425:131C::1

! Rotas para redes G3 via Tunnel0
ipv6 route 2001:690:2425:1314::/64 2001:690:2425:131C::1
ipv6 route 2001:690:2425:1316::/64 2001:690:2425:131C::1

! Rotas para redes G5 via Tunnel1
ipv6 route 2001:690:2425:1317::/64 2001:690:2425:131B::1
ipv6 route 2001:690:2425:1319::/64 2001:690:2425:131B::1

end
copy running-config startup-config
```