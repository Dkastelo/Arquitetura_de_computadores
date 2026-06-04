result ww 0
a      ww 5
b      ww 4
one    ww 1
temp   ww 0

start  mov x temp   
       sub x temp
       
       add x b
       jz end
       
       sub x one
       mov x b
       
       mov x temp   
       sub x temp
       
       add x result 
       add x a
       mov x result
       
       goto start

end    halt