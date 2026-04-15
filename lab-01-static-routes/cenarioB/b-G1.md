# Cenário B - Grupo 1

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
 description WAN
 ipv6 address 2001:690:2425:1212::1/64
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-A
 ipv6 address 2001:690:2425:1211::1/64
 ipv6 nd prefix 2001:690:2425:1211::/64 300 300
 ipv6 nd ra-interval 10
 no ipv6 nd suppress-ra
 no shutdown
 exit

interface GigabitEthernet0/2
 description WAN-SWITCH-G3
 ipv6 address 2001:690:2425:121A::3/64
 no shutdown
 exit

! Rotas para LANs do proprio grupo via RouterB_G1
ipv6 route 2001:690:2425:1213::/64 2001:690:2425:1212::2

! Rotas para redes G3
ipv6 route 2001:690:2425:1214::/64 2001:690:2425:121A::1
ipv6 route 2001:690:2425:1216::/64 2001:690:2425:121A::1

! Rotas para redes G5 via RouterB_G1
ipv6 route 2001:690:2425:1217::/64 2001:690:2425:1212::2
ipv6 route 2001:690:2425:1219::/64 2001:690:2425:1212::2

! WAN de trânsito G5
ipv6 route 2001:690:2425:121B::/64 2001:690:2425:1212::2

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
 description WAN
 ipv6 address 2001:690:2425:1212::2/64
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-C
 ipv6 address 2001:690:2425:1213::1/64
 no shutdown
 exit

interface GigabitEthernet0/2
 description WAN-SWITCH-G5
 ipv6 address 2001:690:2425:121B::3/64
 no shutdown
 exit

! Rotas para LANs do proprio grupo via RouterA_G1
ipv6 route 2001:690:2425:1211::/64 2001:690:2425:1212::1

! Rotas para redes G3 via RouterA_G1
ipv6 route 2001:690:2425:1214::/64 2001:690:2425:1212::1
ipv6 route 2001:690:2425:1216::/64 2001:690:2425:1212::1

! Rotas para redes G5
ipv6 route 2001:690:2425:1217::/64 2001:690:2425:121B::1
ipv6 route 2001:690:2425:1219::/64 2001:690:2425:121B::1

! WAN de trânsito G3
ipv6 route 2001:690:2425:121A::/64 2001:690:2425:1212::1

end
copy running-config startup-config
```