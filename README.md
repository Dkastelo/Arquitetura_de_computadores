# Arquitetura_de_computadores
Trabalho da cadeira de Arquitetura de computadores. O trabalho consiste em fazer um assembler, processador e memória virtuais em python o mais otimizado possível para a realização de questões disponibilizadas em sala no menor tempo de ciclos possível.
## Quais os comandos do assembler?
  1. 'add' para adição;
  2. 'sub' para subtração;
  3. 'mov' para mover de um registrador para o outro;
  4. 'goto' para ir para uma linha específica;
  5. 'jz' para jump if zero;
  6. 'halt' para finalizar o código .

## Como usar?
  No seu terminal, vá para a pasta que contém os arquivos. E siga as instruções:
  1. Para criar o .bin com o seu arquivo codigo.asm em assembly, rode

    python3 assembler_diego.py

  O programa vai pedir o arquivo .asm e o nome do arquivo de destino. Caso você não informar o nome do arquivo de destino, o programa da o nome padrão 'out.bin'
  3. Para traduzir o codigo.bin, rode

    pytohn3 processor.py codigo.bin 
  Vai ser printado no terminal o resultado e o número de ciclos
