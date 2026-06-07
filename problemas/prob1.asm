saida      ww 0
entrada1   ww 55
entrada2   ww 0

Sum        ww 0
D          ww 0
N_work     ww 0
temp       ww 0
quociente  ww 0
zero       ww 0
one        ww 1
two        ww 2

inicio     ld x, entrada1
           jz fim_prog  
           jn fim_prog    
           mov temp, x     

loop_par   ld x, temp
           sub x, two      
           jz eh_par       
           jn eh_impar     
           mov temp, x    
           goto loop_par

eh_impar   ld x, zero
           mov Sum, x
           ld x, one
           mov D, x       

loop_odd   ld x, entrada1
           sub x, D
           jz fim_prog    

           ld x, entrada1
           mov temp, x     

mod_im_loop ld x, temp
           sub x, D
           jz eh_div_impar 
           jn nao_div_impar
           mov temp, x
           goto mod_im_loop

eh_div_impar ld x, Sum
           add x, D
           mov Sum, x     

nao_div_impar ld x, D
           add x, one
           mov D, x       
           goto loop_odd

eh_par     ld x, zero
           mov Sum, x
           ld x, entrada1
           mov N_work, x  
           ld x, two
           mov D, x       

tentar_div_par 
           ld x, N_work
           sub x, one
           jz fim_prog

           ld x, N_work
           mov temp, x
           ld x, zero
           mov quociente, x

div_par_loop ld x, temp
           sub x, D
           jz exata_par   
           jn falhou_par 
           
           mov temp, x
           ld x, quociente
           add x, one
           mov quociente, x 
           goto div_par_loop

exata_par  ld x, quociente
           add x, one
           mov N_work, x 

           ld x, Sum
           add x, D
           mov Sum, x   
           goto tentar_div_par

falhou_par ld x, D
           add x, one
           mov D, x     
           goto tentar_div_par

fim_prog   ld x, Sum
           mov saida, x
           halt