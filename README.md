# Arquitetura_de_computadores
Trabalho da cadeira de Arquitetura de computadores. O trabalho consiste em fazer um assembler, processador e memória virtuais em python o mais otimizado possível para a realização de questões disponibilizadas em sala no menor tempo de ciclos possível.

## Quais os comandos do assembler?  

  1. 'ww' para reservar um espaço de 4 bytes para uma variável

    nome_variável ww valor

  \
  2. 'add' para adição de um valor de um registrador com o valor de uma variável;

    add registrador, variável

  \
  3. 'sub' para subtrair o valor de um registrador com o valor de uma variável;

    sub registrador, variável

  \
  4. 'ld' para carregar o valor de uma variável em um registrador;

    ld registrador, variável

  \
  5. 'mov' para mover o valor de um registrador para um variável;

    mov registrador, variável

  \
  6. 'goto' para saltar para uma linha específica com uma determinada label;

    goto destino

  \
  7. 'jz' para saltar para uma linha específica com uma determinada label se a última operação matemática tiver sido 0, caso contrário, vai pra próxima linha;

    jz destino

  \
  8. 'jn' para saltar para uma linha específica com uma determinada label se a última operação matemática tiver resultado negativo, caso contrário, vai pra próxima linha;

    jn destino

  \
  9. 'halt' para finalizar o código.

    halt


## Como usar o simulador de ciclos?
  No seu terminal, vá para a pasta que contém os arquivos. E siga as instruções.
  1. Para criar o .bin com o seu arquivo codigo.asm em assembly, rode

    python3 assembler_diego.py

  O programa vai pedir o arquivo .asm e o nome do arquivo de destino. Caso você não informe o nome do arquivo de destino, o programa da o nome padrão 'out.bin'
  
  2. Para traduzir o codigo.bin:

    python3 simulator.py 
    
  O programa vai pedir o nome do arquivo .bin e logo em seguida printar o o número de ciclos utilizados e o resultado final do programa

## Como usar o computadorv0.py?
No seu terminal, vá para a pasta que contém os arquivos. E siga as instruções.
  1. Para ver o valor das words 0, 1, 2 e 3 antes e depois do processamento, além do número de ciclos de acordo com o clock.py, escreva no terminal:

    python3 computadorv0.py arquivo.bin

  O computador irá imprimir no terminal o valor das words antes e depois, além do número de passos
