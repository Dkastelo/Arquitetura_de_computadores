res       ww 0
op1       ww 3648413612
lixo      ww 0
c24       ww 16777216
c16       ww 65536
c8        ww 256
um        ww 1
v0        ww 0
v1        ww 0
v2        ww 0

inicio    ld op1 x
ex_v0     sub c24 x
          jn ex_v1
          mov x op1
          ld v0 x
          add um x
          mov x v0
          ld op1 x
          goto ex_v0

ex_v1     ld op1 x
ex_v1l    sub c16 x
          jn ex_v2
          mov x op1
          ld v1 x
          add um x
          mov x v1
          ld op1 x
          goto ex_v1l

ex_v2     ld op1 x
ex_v2l    sub c8 x
          jn c01
          mov x op1
          ld v2 x
          add um x
          mov x v2
          ld op1 x
          goto ex_v2l

c01       ld v0 x
          sub v1 x
          jn c12
          ld v0 x
          mov x res
          ld v1 x
          mov x v0
          ld res x
          mov x v1
c12       ld v1 x
          sub v2 x
          jn c23
          ld v1 x
          mov x res
          ld v2 x
          mov x v1
          ld res x
          mov x v2
c23       ld v2 x
          sub op1 x
          jn c01b
          ld v2 x
          mov x res
          ld op1 x
          mov x v2
          ld res x
          mov x op1
c01b      ld v0 x
          sub v1 x
          jn c12b
          ld v0 x
          mov x res
          ld v1 x
          mov x v0
          ld res x
          mov x v1
c12b      ld v1 x
          sub v2 x
          jn c01c
          ld v1 x
          mov x res
          ld v2 x
          mov x v1
          ld res x
          mov x v2
c01c      ld v0 x
          sub v1 x
          jn junta
          ld v0 x
          mov x res
          ld v1 x
          mov x v0
          ld res x
          mov x v1

junta     ld op1 x
          mov x res
r_v2      ld v2 x
          jz r_v1
          sub um x
          mov x v2
          ld res x
          add c8 x
          mov x res
          goto r_v2
r_v1      ld v1 x
          jz r_v0
          sub um x
          mov x v1
          ld res x
          add c16 x
          mov x res
          goto r_v1
r_v0      ld v0 x
          jz fim
          sub um x
          mov x v0
          ld res x
          add c24 x
          mov x res
          goto r_v0
fim       halt