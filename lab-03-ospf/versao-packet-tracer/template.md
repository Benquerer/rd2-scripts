# Lab 03 - Multi-area OSPFv2 - Grupo \_\_

## Tabela de Endereçamento

| Device | Interface | Endereço IP | Máscara | Área OSPF |
| ------ | --------- | ----------- | ------- | --------- |
| R1     | G0/0      | \_\_\_      | /30     | Area 0    |
| R1     | G0/1      | \_\_\_      | /30     | Area 1    |
| R2     | Lo0       | \_\_\_      | /27     | Area 0    |
| R2     | G0/0      | \_\_\_      | /30     | Area 0    |
| R2     | G0/1      | \_\_\_      | /30     | Area 0    |
| R3     | G0/0      | \_\_\_      | /30     | Area 0    |
| R3     | G0/1      | \_\_\_      | /30     | Area 2    |
| D1     | G1/0/11   | \_\_\_      | /30     | Area 1    |
| D1     | G1/0/23   | \_\_\_      | /24     | Area 1    |
| D2     | G1/0/11   | \_\_\_      | /30     | Area 2    |
| D2     | G1/0/23   | \_\_\_      | /24     | Area 2    |
| PC1    | NIC       | \_\_\_      | /24     | —         |
| PC3    | NIC       | \_\_\_      | /24     | —         |

---

## Configurações

### R1

```ios
enable
conf t
hostname R1
no ip domain-lookup
enable secret class
banner motd #Acesso autorizado apenas.#
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 15
 password cisco
 login
 exit
service password-encryption
int g0/0
 description R1 - Area 0 p/ R2
 ip address ___.___.___.___  255.255.255.252
 no shutdown
 exit
int g0/1
 description R1 - Area 1 p/ D1
 ip address ___.___.___.___  255.255.255.252
 no shutdown
 exit
end
show ip interface brief
copy running-config startup-config

conf t
router ospf 123
router-id 1.1.1.1
auto-cost reference-bandwidth 1000
network ___.___.___.___ 0.0.0.3 area 0
network ___.___.___.___ 0.0.0.3 area 1
area 1 stub
end
show ip ospf neighbor
```

---

### R2

```ios
enable
conf t
hostname R2
no ip domain-lookup
enable secret class
banner motd #Acesso autorizado apenas.#
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 15
 password cisco
 login
 exit
service password-encryption
int g0/0
 description R2 - Area 0 p/ R1
 ip address ___.___.___.___  255.255.255.252
 no shutdown
 exit
int g0/1
 description R2 - Area 0 p/ R3
 ip address ___.___.___.___  255.255.255.252
 no shutdown
 exit
int Loopback0
 description R2 - Internet
 ip address ___.___.___.___  255.255.255.224
 no shutdown
 exit
end
show ip interface brief
copy running-config startup-config

conf t
router ospf 123
router-id 2.2.2.1
auto-cost reference-bandwidth 1000
network ___.___.___.___ 0.0.0.3 area 0
network ___.___.___.___ 0.0.0.3 area 0
end
show ip ospf neighbor
```

---

### R3

```ios
enable
conf t
hostname R3
no ip domain-lookup
enable secret class
banner motd #Acesso autorizado apenas.#
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 15
 password cisco
 login
 exit
service password-encryption
int g0/0
 description R3 - Area 0 p/ R2
 ip address ___.___.___.___  255.255.255.252
 no shutdown
 exit
int g0/1
 description R3 - Area 2 p/ D2
 ip address ___.___.___.___  255.255.255.252
 no shutdown
 exit
end
show ip interface brief
copy running-config startup-config

conf t
router ospf 123
router-id 3.3.3.1
auto-cost reference-bandwidth 1000
network ___.___.___.___ 0.0.0.3 area 0
network ___.___.___.___ 0.0.0.3 area 2
area 2 stub no-summary
end
show ip ospf neighbor
```

---

### D1

```ios
enable
conf t
hostname D1
no ip domain-lookup
enable secret class
banner motd #Acesso autorizado apenas.#
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 15
 password cisco
 login
 exit
service password-encryption
ip routing
int g1/0/11
 description D1 - Area 1 p/ R1
 no switchport
 ip address ___.___.___.___  255.255.255.252
 no shutdown
 exit
int g1/0/23
 description D1 - LAN Area 1 p/ PC1
 no switchport
 ip address ___.___.___.___  255.255.255.0
 no shutdown
 exit
end
show ip interface brief
copy running-config startup-config

conf t
router ospf 123
router-id 1.1.1.2
auto-cost reference-bandwidth 1000
network ___.___.___.___ 0.0.0.3 area 1
network ___.___.___.___ 0.0.0.255 area 1
area 1 stub
end
show ip protocols
show ip ospf interface brief
```

---

### D2

```ios
enable
conf t
hostname D2
no ip domain-lookup
enable secret class
banner motd #Acesso autorizado apenas.#
line console 0
 password cisco
 login
 logging synchronous
 exit
line vty 0 15
 password cisco
 login
 exit
service password-encryption
ip routing
int g1/0/11
 description D2 - Area 2 p/ R3
 no switchport
 ip address ___.___.___.___  255.255.255.252
 no shutdown
 exit
int g1/0/23
 description D2 - LAN Area 2 p/ PC3
 no switchport
 ip address ___.___.___.___  255.255.255.0
 no shutdown
 exit
end
show ip interface brief
copy running-config startup-config

conf t
router ospf 123
router-id 3.3.3.2
auto-cost reference-bandwidth 1000
network ___.___.___.___ 0.0.0.3 area 2
network ___.___.___.___ 0.0.0.255 area 2
area 2 stub
end
show ip protocols
show ip ospf interface brief
```

---

### PC1

```
IP: /24
Gateway:
```

### PC3

```
IP: /24
Gateway:
```
