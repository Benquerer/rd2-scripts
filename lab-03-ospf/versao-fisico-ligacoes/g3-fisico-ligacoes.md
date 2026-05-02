# Lab 03 - Multi-area OSPFv2 - Grupo 03 (Físico + Ligações)

## Tabela de Endereçamento (Físico)

| Device | Interface | Endereço IP     | Máscara | Área OSPF |
| ------ | --------- | --------------- | ------- | --------- |
| R1     | G0/0      | 172.16.30.2     | /30     | Area 0    |
| R1     | G0/1      | 10.10.30.1      | /30     | Area 1    |
| R2     | Lo0       | 209.165.200.225 | /27     | Area 0    |
| R2     | G0/0      | 172.16.30.1     | /30     | Area 0    |
| R2     | G0/1      | 172.16.31.1     | /30     | Area 0    |
| R2     | G0/2      | 10.0.0.3        | /28     | Area 0    |
| R3     | G0/0      | 172.16.31.2     | /30     | Area 0    |
| R3     | G0/1      | 10.10.34.1      | /30     | Area 2    |
| D1     | G1/0/5    | 10.10.30.2      | /30     | Area 1    |
| D1     | G1/0/23   | 10.10.31.1      | /24     | Area 1    |
| D2     | G1/0/11   | 10.10.34.2      | /30     | Area 2    |
| D2     | G1/0/23   | 10.10.35.1      | /24     | Area 2    |
| PC1    | NIC       | 10.10.31.10     | /24     | —         |
| PC3    | NIC       | 10.10.35.10     | /24     | —         |

## Tabela de Backbone Inter-grupos

| Grupo | IP Backbone | Interface |
| ----- | ----------- | --------- |
| 1     | 10.0.0.1    | R2 G0/2   |
| 2     | 10.0.0.2    | R2 G0/2   |
| 3     | 10.0.0.3    | R2 G0/2   |
| 4     | 10.0.0.4    | R2 G0/2   |
| 5     | 10.0.0.5    | R2 G0/2   |
| 6     | 10.0.0.6    | R2 G0/2   |

> Rede backbone: 10.0.0.0/28 — /28 escolhido para flexibilidade (10 IPs livres para expansão)

#### Roles OSPF:

> **ABR** (Area Border Router): R1, R3 — ligam áreas regulares à Area 0
> **ASBR** (Autonomous System Boundary Router): R2 — liga à rede externa (Internet)
> **Internal routers**: R2 (Area 0), D1 (Area 1), D2 (Area 2)
> **Backbone routers**: R1, R2, R3 — todos têm interfaces na Area 0

#### Nota — Router-IDs únicos por grupo:

> Num domínio OSPF multi-grupo, todos os routers partilham o mesmo processo OSPF (123) e a mesma Area 0 via backbone 10.0.0.0/28. Para evitar conflitos de router-ID, o primeiro octeto identifica o grupo (1-6). Exemplo: R2 do grupo 1 = 1.2.2.1, R2 do grupo 2 = 2.2.2.1, etc.

| Router | Router-ID |
| ------ | --------- |
| R1     | 3.1.1.1   |
| R2     | 3.2.2.1   |
| R3     | 3.3.3.1   |
| D1     | 3.1.1.2   |
| D2     | 3.3.3.2   |

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
 ip address 172.16.30.2 255.255.255.252
 no shutdown
 exit
int g0/1
 description R1 - Area 1 p/ D1
 ip address 10.10.30.1 255.255.255.252
 no shutdown
 exit
end
show ip interface brief
conf t
router ospf 123
router-id 3.1.1.1
auto-cost reference-bandwidth 1000
network 172.16.30.0 0.0.0.3 area 0
network 10.10.30.0 0.0.0.3 area 1
area 1 stub
end
show ip ospf neighbor
copy running-config startup-config
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
 ip address 172.16.30.1 255.255.255.252
 no shutdown
 exit
int g0/1
 description R2 - Area 0 p/ R3
 ip address 172.16.31.1 255.255.255.252
 no shutdown
 exit
int g0/2
 description R2 - Backbone inter-grupos
 ip address 10.0.0.3 255.255.255.240
 no shutdown
 exit
int Loopback0
 description R2 - Internet
 ip address 209.165.200.225 255.255.255.224
 no shutdown
 exit
end
show ip interface brief
conf t
router ospf 123
router-id 3.2.2.1
auto-cost reference-bandwidth 1000
network 172.16.30.0 0.0.0.3 area 0
network 172.16.31.0 0.0.0.3 area 0
network 10.0.0.0 0.0.0.15 area 0
! Loopback a simular Internet - retirar se ligar a outro grupo
network 209.165.200.224 0.0.0.31 area 0
! Retirar se nao houver rota default real (ligacao a outro grupo)
default-information originate always
end
show ip ospf neighbor
copy running-config startup-config
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
 ip address 172.16.31.2 255.255.255.252
 no shutdown
 exit
int g0/1
 description R3 - Area 2 p/ D2
 ip address 10.10.34.1 255.255.255.252
 no shutdown
 exit
end
show ip interface brief
conf t
router ospf 123
router-id 3.3.3.1
auto-cost reference-bandwidth 1000
network 172.16.31.0 0.0.0.3 area 0
network 10.10.34.0 0.0.0.3 area 2
area 2 stub no-summary
end
show ip ospf neighbor
copy running-config startup-config
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
int g1/0/5
 description D1 - Area 1 p/ R1
 no switchport
 ip address 10.10.30.2 255.255.255.252
 no shutdown
 exit
int g1/0/23
 description D1 - LAN Area 1 p/ PC1
 no switchport
 ip address 10.10.31.1 255.255.255.0
 no shutdown
 exit
end
show ip interface brief
conf t
router ospf 123
router-id 3.1.1.2
auto-cost reference-bandwidth 1000
network 10.10.30.0 0.0.0.3 area 1
network 10.10.31.0 0.0.0.255 area 1
area 1 stub
end
show ip protocols
show ip ospf interface brief
copy running-config startup-config
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
 ip address 10.10.34.2 255.255.255.252
 no shutdown
 exit
int g1/0/23
 description D2 - LAN Area 2 p/ PC3
 no switchport
 ip address 10.10.35.1 255.255.255.0
 no shutdown
 exit
end
show ip interface brief
conf t
router ospf 123
router-id 3.3.3.2
auto-cost reference-bandwidth 1000
network 10.10.34.0 0.0.0.3 area 2
network 10.10.35.0 0.0.0.255 area 2
area 2 stub
end
show ip protocols
show ip ospf interface brief
copy running-config startup-config
```

---

### PC1

```
IP: 10.10.31.10/24
Gateway: 10.10.31.1
```

### PC3

```
IP: 10.10.35.10/24
Gateway: 10.10.35.1
```
