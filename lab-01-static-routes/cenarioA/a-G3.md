# Cenário A - Grupo 3

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

interface GigabitEthernet0/1
 description LAN-A
 ip address 192.168.30.1 255.255.255.128
 no shutdown
 exit

interface GigabitEthernet0/0
 description WAN
 ip address 172.16.30.1 255.255.255.0
 no shutdown
 exit

! Rota sumária para LAN C via RouterB_G3
ip route 192.168.30.0 255.255.254.0 172.16.30.2

! Rota default para grupo do meio
ip route 0.0.0.0 0.0.0.0 172.16.30.3

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

interface GigabitEthernet0/0
 description WAN
 ip address 172.16.30.2 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-C
 ip address 192.168.31.1 255.255.255.0
 no shutdown
 exit

! Rota sumária para LAN A via RouterA_G3
ip route 192.168.30.0 255.255.254.0 172.16.30.1

! Rota default para grupo do meio
ip route 0.0.0.0 0.0.0.0 172.16.30.3

end
copy running-config startup-config
```