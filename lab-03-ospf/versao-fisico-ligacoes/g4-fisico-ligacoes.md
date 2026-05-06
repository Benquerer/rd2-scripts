# Lab 03 - Multi-area OSPFv2 - Grupo 04 (Físico + Ligações)

## Tabela de Endereçamento (Físico)

| Device | Interface | Endereço IP | Máscara | Área OSPF |
| ------ | --------- | ----------- | ------- | --------- |
| R1     | G0/0      | 172.16.40.2 | /30     | Area 41   |
| R1     | G0/1      | 10.10.40.1  | /30     | Area 41   |
| R2     | G0/0      | 172.16.40.1 | /30     | Area 41   |
| R2     | G0/1      | 172.16.41.1 | /30     | Area 42   |
| R2     | G0/2      | 10.0.0.4    | /28     | Area 0    |
| R3     | G0/0      | 172.16.41.2 | /30     | Area 42   |
| R3     | G0/1      | 10.10.44.1  | /24     | Area 42   |
| D1     | Fa0/5     | 10.10.40.2  | /30     | Area 41   |
| D1     | Fa0/23    | 10.10.41.1  | /24     | Area 41   |
| D2     | —         | —           | —       | L2 only   |
| PC0    | NIC       | 10.10.41.10 | /24     | —         |
| PC1    | NIC       | 10.10.44.10 | /24     | —         |

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

> **ABR**: R2 — liga Area 0 às Areas 41 e 42
> **Internal routers Area 41**: R1, D1
> **Internal routers Area 42**: R3
> **Switch L2**: D2 — transparente, sem IP, sem OSPF

#### Nota — Áreas por grupo:

> Cada grupo usa 2 áreas: X1 (stub) e X2 (totally stub), onde X é o número do grupo.
> A Area 0 é partilhada por todos os grupos via switch L2 central (10.0.0.0/28).
> Total: 12 áreas de grupo + Area 0.

#### Nota — Router-IDs únicos por grupo:

> Para evitar conflitos de router-ID no domínio OSPF partilhado, seguimos a seguinte lógica:
>
> - **1º octeto** — número do grupo (1-6)
> - **2º octeto** — número do router (R1=1, R2=2, R3=3)
> - **3º octeto** — igual ao 2º (preenchimento)
> - **4º octeto** — 1 para routers, 2 para switches L3 (D1)

| Router | Router-ID |
| ------ | --------- |
| R1     | 4.1.1.1   |
| R2     | 4.2.2.1   |
| R3     | 4.3.3.1   |
| D1     | 4.1.1.2   |

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
 description R1 - Area 41 p/ R2
 ip address 172.16.40.2 255.255.255.252
 no shutdown
 exit
int g0/1
 description R1 - Area 41 p/ D1
 ip address 10.10.40.1 255.255.255.252
 no shutdown
 exit
router ospf 123
router-id 4.1.1.1
auto-cost reference-bandwidth 1000
network 172.16.40.0 0.0.0.3 area 41
network 10.10.40.0 0.0.0.3 area 41
area 41 stub
end

show ip interface brief

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
 description R2 - Area 41 p/ R1
 ip address 172.16.40.1 255.255.255.252
 no shutdown
 exit
int g0/1
 description R2 - Area 42 p/ R3
 ip address 172.16.41.1 255.255.255.252
 no shutdown
 exit
int g0/2
 description R2 - Backbone inter-grupos
 ip address 10.0.0.4 255.255.255.240
 no shutdown
 exit
router ospf 123
router-id 4.2.2.1
auto-cost reference-bandwidth 1000
network 172.16.40.0 0.0.0.3 area 41
network 172.16.41.0 0.0.0.3 area 42
network 10.0.0.0 0.0.0.15 area 0
area 41 stub
area 42 stub no-summary
end

show ip interface brief

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
 description R3 - Area 42 p/ R2
 ip address 172.16.41.2 255.255.255.252
 no shutdown
 exit
int g0/1
 description R3 - Area 42 p/ D2/PC1
 ip address 10.10.44.1 255.255.255.0
 no shutdown
 exit
router ospf 123
router-id 4.3.3.1
auto-cost reference-bandwidth 1000
network 172.16.41.0 0.0.0.3 area 42
network 10.10.44.0 0.0.0.255 area 42
area 42 stub
end

show ip interface brief

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
int Fa0/5
 description D1 - Area 41 p/ R1
 no switchport
 ip address 10.10.40.2 255.255.255.252
 no shutdown
 exit
int Fa0/23
 description D1 - LAN Area 41 p/ PC0
 no switchport
 ip address 10.10.41.1 255.255.255.0
 no shutdown
 exit
router ospf 123
router-id 4.1.1.2
auto-cost reference-bandwidth 1000
network 10.10.40.0 0.0.0.3 area 41
network 10.10.41.0 0.0.0.255 area 41
area 41 stub
end

show ip interface brief

show ip ospf neighbor

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
end

copy running-config startup-config
```

---

### PC0

```
IP: 10.10.41.10/24
Gateway: 10.10.41.1
```

### PC1

```
IP: 10.10.44.10/24
Gateway: 10.10.44.1
```
