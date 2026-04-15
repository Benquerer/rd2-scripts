# Cenário A - Grupo 1

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

interface GigabitEthernet0/0
 description WAN
 ip address 172.16.10.1 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-A
 ip address 192.168.10.1 255.255.255.128
 no shutdown
 exit

interface GigabitEthernet0/2
 description WAN-SWITCH-G3
 ip address 172.16.30.3 255.255.255.0
 no shutdown
 exit

! Rota sumária para LANs do proprio grupo via RouterB_G1
ip route 192.168.10.0 255.255.254.0 172.16.10.2

! Rota sumária para redes G3
ip route 192.168.30.0 255.255.254.0 172.16.30.2

! Rota sumária para redes G5 via RouterB_G1
ip route 192.168.50.0 255.255.254.0 172.16.10.2

! WANs de trânsito

ip route 172.16.50.0 255.255.255.0 172.16.10.2

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

interface GigabitEthernet0/0
 description WAN
 ip address 172.16.10.2 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/1
 description LAN-C
 ip address 192.168.11.1 255.255.255.0
 no shutdown
 exit

interface GigabitEthernet0/2
 description WAN-SWITCH-G5
 ip address 172.16.50.3 255.255.255.0
 no shutdown
 exit

! Rota sumária para LANs do proprio grupo via RouterA_G1
ip route 192.168.10.0 255.255.254.0 172.16.10.1

! Rota sumária para redes G3 via RouterA_G1
ip route 192.168.30.0 255.255.254.0 172.16.10.1

! Rota sumária para redes G5
ip route 192.168.50.0 255.255.254.0 172.16.50.2

! WANs de trânsito
ip route 172.16.30.0 255.255.255.0 172.16.10.1


end
copy running-config startup-config
```