# Ponto 8 - Desafio IPv6

## R1 — Cisco 1921

```
configure terminal
ipv6 unicast-routing
!
interface FastEthernet0/0/0
 ipv6 address 2001:690:1:1::1/64
!
interface Tunnel0
 description -> Tunel IPv6 para o R3
 ipv6 address 2001:690:1:FF::1/64
 tunnel source Loopback0
 tunnel destination 10.1.1.131
 tunnel mode ipv6ip
 no shutdown
!
ipv6 route 2001:690:1:2::/64 2001:690:1:FF::2
!
end
copy running-config startup-config
```

---

## R3 — Cisco 2911

```
configure terminal
ipv6 unicast-routing
!
interface GigabitEthernet0/2
 ipv6 address 2001:690:1:2::1/64
!
interface Tunnel0
 description -> Tunel IPv6 para o R1
 ipv6 address 2001:690:1:FF::2/64
 tunnel source Loopback0
 tunnel destination 10.1.1.129
 tunnel mode ipv6ip
 no shutdown
!
ipv6 route 2001:690:1:1::/64 2001:690:1:FF::1
!
end
copy running-config startup-config
```
