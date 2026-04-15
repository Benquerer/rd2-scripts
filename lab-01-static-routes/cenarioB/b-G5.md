# Cenário B - Grupo 5

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
 ipv6 address 2001:690:2425:121B::1/64
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-A
 ipv6 address 2001:690:2425:1217::1/64
 ipv6 nd prefix 2001:690:2425:1217::/64 300 300
 ipv6 nd ra-interval 10
 no ipv6 nd suppress-ra
 no shutdown
 exit

! Rota para LAN C via RouterB_G5
ipv6 route 2001:690:2425:1219::/64 2001:690:2425:121B::2

! Rota default para grupo do meio
ipv6 route ::/0 2001:690:2425:121B::3

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
 ipv6 address 2001:690:2425:121B::2/64
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-C
 ipv6 address 2001:690:2425:1219::1/64
 no shutdown
 exit

! Rota para LAN A via RouterA_G5
ipv6 route 2001:690:2425:1217::/64 2001:690:2425:121B::1

! Rota default para grupo do meio
ipv6 route ::/0 2001:690:2425:121B::3

end
copy running-config startup-config
```