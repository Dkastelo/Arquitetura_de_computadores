res       ww 0
op1       ww 3648413612
op2       ww 1017835715
c24       ww 16777216
c16       ww 65536
c8        ww 256
um        ww 1
a3        ww 0
a2        ww 0
a1        ww 0

inicio    ld op1 x
ex_a3     sub c24 x
          jn ex_a2
          mov x op1
          ld a3 x
          add um x
          mov x a3
          ld op1 x
          goto ex_a3

ex_a2     ld op1 x
ex_a2l    sub c16 x
          jn ex_a1
          mov x op1
          ld a2 x
          add um x
          mov x a2
          ld op1 x
          goto ex_a2l

ex_a1     ld op1 x
ex_a1l    sub c8 x
          jn ext_done
          mov x op1
          ld a1 x
          add um x
          mov x a1
          ld op1 x
          goto ex_a1l

ext_done  ld op2 x
m3        sub c24 x
          jn m2_init
          mov x op2
          ld res x
          add a3 x
          mov x res
          ld op2 x
          goto m3

m2_init   ld op2 x
m2        sub c16 x
          jn m1_init
          mov x op2
          ld res x
          add a2 x
          mov x res
          ld op2 x
          goto m2

m1_init   ld op2 x
m1        sub c8 x
          jn m0_init
          mov x op2
          ld res x
          add a1 x
          mov x res
          ld op2 x
          goto m1

m0_init   ld op2 x
          jz fim
m0        sub um x
          mov x op2
          ld res x
          add op1 x
          mov x res
          ld op2 x
          jz fim
          goto m0

fim       halt