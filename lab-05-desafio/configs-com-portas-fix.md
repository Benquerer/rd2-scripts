# RDII – TL5 (Desafio) | PL-TA | Grupo 1 — Configurações 

**AS60101 · base 10.1.1.0/24 · agregado 10.1.1.0/24**

## Cablagem (conforme indicado)
| Ligação | Lado A | Lado B | Rede |
|---|---|---|---|
| R1–AS100 (eBGP) | R1 **Gi0/0** (172.17.1.1) | AS100-R **Gi0/0** (172.17.1.2) | 172.17.1.0/30 |
| R3–AS200 (eBGP) | R3 **Gi0/0** (172.21.1.1) | AS200-R **Gi0/0** (172.21.1.2) | 172.21.1.0/30 |
| R1–R2 | R1 **Gi0/1** (10.1.1.1) | R2 **Fa0/0** (10.1.1.2) | 10.1.1.0/30 |
| R2–R3 | R2 **Fa0/1** (10.1.1.5) | R3 **Gi0/1** (10.1.1.6) | 10.1.1.4/30 |
| Área 1 (direto) | R1 **Fa0/0/0** (10.1.1.17) | PC-A1 (10.1.1.18) | 10.1.1.16/28 |
| R1–R4-RIP | R1 **Fa0/0/1** (10.1.1.49) | R4-RIP **Fa0/0** (10.1.1.50) | 10.1.1.48/30 |
| LAN RIP | R4-RIP **Fa0/1** (10.1.1.65) | PC-RIP (10.1.1.66) | 10.1.1.64/28 |
| Área 2 (direto) | R3 **Gi0/2** (10.1.1.33) | PC-A2 (10.1.1.34) | 10.1.1.32/28 |
| ~~R1–R3~~ | — | — | 10.1.1.8/30 **(livre, não usada)** |

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
interface GigabitEthernet0/0
 description -> AS100-R (eBGP)
 ip address 172.17.1.1 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 description -> R2
 ip address 10.1.1.1 255.255.255.252
 no shutdown
!
interface FastEthernet0/0/0
 description -> PC-A1 (LAN Area 1)
 ip address 10.1.1.17 255.255.255.240
 no shutdown
!
interface FastEthernet0/0/1
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
 passive-interface FastEthernet0/0/0
 redistribute rip subnets metric 20 metric-type 2
!
! ===== RIP (so ativo para R4-RIP) =====
router rip
 version 2
 no auto-summary
 network 10.0.0.0
 passive-interface default
 no passive-interface FastEthernet0/0/1
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
 default-information originate
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
interface GigabitEthernet0/0
 description -> AS200-R (eBGP)
 ip address 172.21.1.1 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 description -> R2
 ip address 10.1.1.6 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/2
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
 passive-interface GigabitEthernet0/2
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

## R4-RIP — Cisco 1841 (só RIP, **sem** OSPF)

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

## PCs (ligação direta ao router)
| PC | Liga a | IP | Máscara | Gateway |
|---|---|---|---|---|
| PC-A1 | R1 Fa0/0/0 | 10.1.1.18 | 255.255.255.240 | 10.1.1.17 |
| PC-A2 | R3 Gi0/2 | 10.1.1.34 | 255.255.255.240 | 10.1.1.33 |
| PC-RIP | R4-RIP Fa0/1 | 10.1.1.66 | 255.255.255.240 | 10.1.1.65 |

---

## Routers externos (referência)

**AS100-R (AS100):**
```
hostname AS100-R
interface Loopback0
 ip address 100.1.1.1 255.255.255.0
interface GigabitEthernet0/0
 description -> R1
 ip address 172.17.1.2 255.255.255.252
 no shutdown
interface GigabitEthernet0/1
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
interface GigabitEthernet0/0
 description -> R3
 ip address 172.21.1.2 255.255.255.252
 no shutdown
interface GigabitEthernet0/1
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
interface Serial0/1/0
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
interface Serial0/0/0
 description -> R1
 ip address 10.1.1.10 255.255.255.252
 no shutdown
!
router ospf 123
 network 10.1.1.8 0.0.0.3 area 0
```

---

## Validação
```
show ip interface brief
show ip ospf neighbor        ! R1<->R2 e R2<->R3 em FULL
show ip route ospf
show ip route rip            ! no R4-RIP
show ip bgp summary          ! AS100, AS200 e iBGP UP
show ip bgp
show ip route 0.0.0.0        ! no R2, antes/depois do shutdown de Fa0/0
```
Testes: `PC-RIP → PC-A2`, `PC-RIP → 100.1.1.1`, `PC-RIP → 200.1.1.1`, `PC-A1 → PC-A2`.
