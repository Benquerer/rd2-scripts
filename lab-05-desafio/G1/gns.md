# Trab. Laboratorial #5 (Desafio) | Grupo 1 - Turma A (**AS60101**)

## Ligações Fisicas
| Ligação | Lado A | Lado B | Rede |
|---|---|---|---|
| R1 <-> AS100 | R1: **G0/0** | AS100: **G0/0** | 172.17.1.0 /30 |
| R3 <-> AS200 | R3: **G0/0** | AS200: **G0/0** | 172.21.1.0 /30 |
| R1 <-> R2 | R1: **G0/1** | R2: **Fa0/0** | 10.1.1.0 /30 |
| R2 <-> R3 | R2: **Fa0/1** | R3: **G0/1** | 10.1.1.4 /30 |
| R1 <-> R4-RIP | R1: **Fa0/0/1** | R4-RIP: **Fa0/0** | 10.1.1.48 /30 |
| R1 <-> R3 | R1: **Serial0/1/0** | R3: **Serial0/0/0** | 10.1.1.8 /30 |
| AS100 <-> AS200 | AS100: **G0/1** | AS200: **G0/1** | 172.25.1.0 /30 |
| **PCs** | | | |
| Área 1 (direto) | R1: **Fa0/0/0** | PC-A1 | 10.1.1.16 /28 |
| Área 2 (direto) | R3: **G0/2** | PC-A2 | 10.1.1.32 /28 |
| RIP | R4-RIP: **Fa0/1** | PC-RIP | 10.1.1.64 /28 |


## Endereçamento
| Interface | Endereço | Máscara 
|---|---|---|
|**R1**|||
| G0/0 | 172.17.1.1 | 255.255.255.252 |
| G0/1 | 10.1.1.1 | 255.255.255.252 |
| Fe0/0/0 | 10.1.1.17 | 255.255.255.240 |
| Fe0/0/1 | 10.1.1.49 | 255.255.255.252 |
| Serial0/1/0 | 10.1.1.9 | 255.255.255.252 |

---

| Interface | Endereço | Máscara
|---|---|---|
|**R2**|||
| Fe0/0 | 10.1.1.2 | 255.255.255.252 |
| Fe0/1 | 10.1.1.5 | 255.255.255.252 |

---

| Interface | Endereço | Máscara |
|---|---|---|
|**R3**|||
| G0/0 | 172.21.1.1 | 255.255.255.252 |
| G0/1 | 10.1.1.6 | 255.255.255.252 |
| G0/2 | 10.1.1.33 | 255.255.255.240 |
| Serial0/0/0 | 10.1.1.10 | 255.255.255.252 |

---

| Interface | Endereço | Máscara
|---|---|---|
|**R4**|||
| Fe0/0 | 10.1.1.50 | 255.255.255.252 |
| Fe0/1 | 10.1.1.65 | 255.255.255.240 |

---

| Interface | Endereço | Máscara |
|---|---|---|
|**AS100**||||
| G0/0 | 172.17.1.2 | 255.255.255.252 |
| G0/1 | 172.25.1.1 | 255.255.255.252 |

---

| Interface | Endereço | Máscara |
|---|---|---|
|**AS200**|||
| G0/0 | 172.21.1.2 | 255.255.255.252 |
| G0/1 | 172.25.1.2 | 255.255.255.252 |

---

| Interface | Endereço | Máscara | Gateway |
|---|---|---|---|
| **PC_Area1** | 10.1.1.18 | 255.255.255.240 | 10.1.1.17 |
| **PC_Area2** | 10.1.1.34 | 255.255.255.240 | 10.1.1.33 |
| **PC_RIP** | 10.1.1.66 | 255.255.255.240 | 10.1.1.65 |

---

## R1 — Cisco 1921

```
enable
configure terminal
!
hostname R1
no ip domain-lookup
service password-encryption
enable secret class
banner motd #Acesso restrito - RDII TL5 - PL-TA Grupo 1#
!
line console 0
 password cisco
 login
 logging synchronous
line vty 0 4
 password cisco
 login
!
interface Loopback0
 ip address 10.1.1.129 255.255.255.255
!
interface fa0/0
 description -> AS100-R (eBGP)
 ip address 172.17.1.1 255.255.255.252
 no shutdown
!
interface fa0/1
 description -> R2
 ip address 10.1.1.1 255.255.255.252
 no shutdown
!
interface s0/0
 description -> PC-A1 (LAN Area 1)
 ip address 10.1.1.17 255.255.255.240
 no shutdown
!
interface fa1/0
 description -> R4-RIP (zona RIP)
 ip address 10.1.1.49 255.255.255.252
 no shutdown
!
! ===== OSPF (ABR Area 0/1 + ASBR) =====
router ospf 123
 router-id 10.1.1.129
 network 10.1.1.0 0.0.0.3 area 0
 network 10.1.1.129 0.0.0.0 area 0
 network 10.1.1.16 0.0.0.15 area 1
 passive-interface s0/0
 redistribute rip subnets metric 20 metric-type 2
 default-information originate always
!
! ===== RIP (so ativo para R4-RIP) =====
router rip
 version 2
 no auto-summary
 network 10.0.0.0
 passive-interface default
 no passive-interface fa1/0
 redistribute ospf 123 metric 5
 default-information originate
!
! ===== BGP (eBGP AS100 + iBGP R3) =====
ip route 10.1.1.0 255.255.255.0 Null0
!
router bgp 60101
 bgp router-id 10.1.1.129
 network 10.1.1.0 mask 255.255.255.0
 neighbor 172.17.1.2 remote-as 100
 neighbor 10.1.1.131 remote-as 60101
 neighbor 10.1.1.131 update-source Loopback0
 neighbor 10.1.1.131 next-hop-self
!
end
copy running-config startup-config
```

---

## R2 — Cisco 1841

```
enable
configure terminal
!
hostname R2
no ip domain-lookup
service password-encryption
enable secret class
banner motd #Acesso restrito - RDII TL5 - PL-TA Grupo 1#
!
line console 0
 password cisco
 login
 logging synchronous
line vty 0 4
 password cisco
 login
!
interface Loopback0
 ip address 10.1.1.130 255.255.255.255
!
interface FastEthernet0/0
 description -> R1
 ip address 10.1.1.2 255.255.255.252
 no shutdown
!
interface FastEthernet0/1
 description -> R3
 ip address 10.1.1.5 255.255.255.252
 no shutdown
!
! ===== OSPF (interno backbone) =====
router ospf 123
 router-id 10.1.1.130
 network 10.1.1.0 0.0.0.3 area 0
 network 10.1.1.4 0.0.0.3 area 0
 network 10.1.1.130 0.0.0.0 area 0
!
! ===== Rotas por defeito (Tarefa 4) =====
ip route 0.0.0.0 0.0.0.0 FastEthernet0/0 10.1.1.1
ip route 0.0.0.0 0.0.0.0 FastEthernet0/1 10.1.1.6 200
!
end
copy running-config startup-config
```

---

## R3 — Cisco 2911

```
enable
configure terminal
!
hostname R3
no ip domain-lookup
service password-encryption
enable secret class
banner motd #Acesso restrito - RDII TL5 - PL-TA Grupo 1#
!
line console 0
 password cisco
 login
 logging synchronous
line vty 0 4
 password cisco
 login
!
interface Loopback0
 ip address 10.1.1.131 255.255.255.255
!
interface fa0/0
 description -> AS200-R (eBGP)
 ip address 172.21.1.1 255.255.255.252
 no shutdown
!
interface fa0/1
 description -> R2
 ip address 10.1.1.6 255.255.255.252
 no shutdown
!
interface fa1/0
 description -> PC-A2 (LAN Area 2)
 ip address 10.1.1.33 255.255.255.240
 no shutdown
!
! ===== OSPF (ABR Area 0/2) =====
router ospf 123
 router-id 10.1.1.131
 network 10.1.1.4 0.0.0.3 area 0
 network 10.1.1.131 0.0.0.0 area 0
 network 10.1.1.32 0.0.0.15 area 2
 passive-interface fa1/0
 default-information originate always
!
! ===== BGP (eBGP AS200 + iBGP R1) =====
ip route 10.1.1.0 255.255.255.0 Null0
!
router bgp 60101
 bgp router-id 10.1.1.131
 network 10.1.1.0 mask 255.255.255.0
 neighbor 172.21.1.2 remote-as 200
 neighbor 10.1.1.129 remote-as 60101
 neighbor 10.1.1.129 update-source Loopback0
 neighbor 10.1.1.129 next-hop-self
!
end
copy running-config startup-config
```

---

## R4-RIP — Cisco 1841 (Zona OSPF)

```
enable
configure terminal
!
hostname R4-RIP
no ip domain-lookup
service password-encryption
enable secret class
banner motd #Acesso restrito - RDII TL5 - PL-TA Grupo 1 - Zona RIP#
!
line console 0
 password cisco
 login
 logging synchronous
line vty 0 4
 password cisco
 login
!
interface Loopback0
 ip address 10.1.1.132 255.255.255.255
!
interface FastEthernet0/0
 description -> R1
 ip address 10.1.1.50 255.255.255.252
 no shutdown
!
interface FastEthernet0/1
 description -> PC-RIP (LAN RIP)
 ip address 10.1.1.65 255.255.255.240
 no shutdown
!
! ===== RIPv2 =====
router rip
 version 2
 no auto-summary
 network 10.0.0.0
!
end
copy running-config startup-config
```

---

## Routers externos (referência)

**AS100-R (AS100):**
```
conft
hostname AS100-R
interface Loopback0
 ip address 100.1.1.1 255.255.255.0
interface fa0/0
 description -> R1
 ip address 172.17.1.2 255.255.255.252
 no shutdown
interface fa0/1
 description -> AS200-R
 ip address 172.25.1.1 255.255.255.252
 no shutdown
!
router bgp 100
 network 100.1.1.0 mask 255.255.255.0
 neighbor 172.17.1.1 remote-as 60101
 neighbor 172.25.1.2 remote-as 200
```

**AS200-R (AS200):**
```
hostname AS200-R
interface Loopback0
 ip address 200.1.1.1 255.255.255.0
interface fa0/0
 description -> R3
 ip address 172.21.1.2 255.255.255.252
 no shutdown
interface fa0/1
 description -> AS100-R
 ip address 172.25.1.2 255.255.255.252
 no shutdown
!
router bgp 200
 network 200.1.1.0 mask 255.255.255.0
 neighbor 172.21.1.1 remote-as 60101
 neighbor 172.25.1.1 remote-as 100
```

---

## (FIX Fail-over) ligação R1–R3 por serial

**R1** (adicionar):
```
interface s0/1
 description -> R3
 ip address 10.1.1.9 255.255.255.252
 clock rate 128000
 no shutdown
!
router ospf 123
 network 10.1.1.8 0.0.0.3 area 0
```
**R3** (adicionar):
```
interface s0/1
 description -> R1
 ip address 10.1.1.10 255.255.255.252
 no shutdown
!
router ospf 123
 network 10.1.1.8 0.0.0.3 area 0
```
