saida      ww 0
entrada1   ww 17
entrada2   ww 0

cand       ww 0
D          ww 0
temp       ww 0
Sum        ww 0
zero       ww 0
one        ww 1
two        ww 2


inicio              ld x, entrada1
                     jz not_prime   
                     sub x, one
                     jz not_prime    
 
                      ld x, two
                      mov D, x

check_prime         ld x, entrada1
                    sub x, D
                    jz is_prime     

                    ld x, entrada1
                    mov temp, x

mod_loop_1
                    ld x, temp
                    sub x, D
                    jz not_prime    
                    jn next_d_1
                    mov temp, x
                    goto mod_loop_1

next_d_1            ld x, D
                    add x, one
                    mov D, x
                    goto check_prime

is_prime            ld x, entrada1
                    add x, one
                    mov cand, x    
                    ld x, zero
                    mov Sum, x
                    ld x, one
                    mov D, x

sum_divs_loop       ld x, cand
                    sub x, D
                    jz end_prog     

                    ld x, cand
                    mov temp, x

mod_loop_2          ld x, temp
                    sub x, D
                    jz is_divisor
                    jn not_divisor
                    mov temp, x
                     goto mod_loop_2

is_divisor          ld x, Sum
                    add x, D
                    mov Sum, x

not_divisor         ld x, D
                    add x, one
                    mov D, x
                    goto sum_divs_loop


not_prime           ld x, entrada1
                    add x, one
                    mov cand, x     

check_cand          ld x, two
                    mov D, x

test_cand_prime     ld x, cand
                    sub x, D
                    jz found_next_prime

                    ld x, cand
                    mov temp, x

mod_loop_3          ld x, temp
                    sub x, D
                    jz cand_failed      
                    jn cand_next_d
                    mov temp, x
                    goto mod_loop_3

cand_next_d         ld x, D
                    add x, one
                    mov D, x
                    goto test_cand_prime

cand_failed         ld x, cand
                    add x, one
                    mov cand, x         
                    goto check_cand

found_next_prime    ld x, cand
                    mov Sum, x

end_prog            ld x, Sum
                    mov saida, x
                    halt
