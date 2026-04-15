# Cenário B - Grupo 3

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
 ipv6 address 2001:690:2425:1214::1/64
 ipv6 nd prefix 2001:690:2425:1214::/64 300 300
 ipv6 nd ra-interval 10
 no ipv6 nd suppress-ra
 no shutdown
 exit

interface GigabitEthernet0/0
 description WAN-SWITCH-G3
 ipv6 address 2001:690:2425:121A::1/64
 no shutdown
 exit

! Rota para LAN C via RouterB_G3
ipv6 route 2001:690:2425:1216::/64 2001:690:2425:121A::2

! Rota default para grupo do meio
ipv6 route ::/0 2001:690:2425:121A::3

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
 ipv6 address 2001:690:2425:121A::2/64
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-C
 ipv6 address 2001:690:2425:1216::1/64
 no shutdown
 exit

! Rota para LAN A via RouterA_G3
ipv6 route 2001:690:2425:1214::/64 2001:690:2425:121A::1

! Rota default para grupo do meio
ipv6 route ::/0 2001:690:2425:121A::3

end
copy running-config startup-config
```