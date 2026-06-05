import memory
from array import array

MPC = 0
MIR = 0

MAR = 0
MDR = 0
PC = -1
MBR = 0
X = 0
Y = 0
H = 0

N = 0
Z = 1

BUS_A = 0
BUS_B = 0
BUS_C = 0

firmware = array('L',[0]) * 512

#0: INIT
firmware[0] = 0b000000000_100_00110101_001000_001_001 

#1: X = mem[address] (NOVA INSTRUÇÃO DE LOAD) -> Opcode 0x01
firmware[1] = 0b000011101_000_00110101_101000_001_001
firmware[29] = 0b000011110_000_00010100_100000_010_010
firmware[30] = 0b011001000_000_00010100_000100_000_000

#2: X = X + mem[address]
firmware[2] = 0b000000011_000_00110101_101000_001_001
firmware[3] = 0b000000100_000_00010100_100000_010_010
firmware[4] = 0b000000101_000_00010100_000001_000_000
firmware[5] = 0b011001000_000_00111100_000100_000_011     

#6: memory[address] = X
firmware[6] = 0b000000111_000_00110101_101000_001_001
firmware[7] = 0b000001000_000_00010100_100000_000_010
firmware[8] = 0b011001000_000_00010100_010000_100_011

#9: GOTO address
firmware[9]  = 0b000001010_000_00110101_001000_001_001
firmware[10] = 0b000000000_100_00010100_001000_001_010

#11: IF X == 0 GOTO address
firmware[11] =  0b000001100_001_00010100_000000_000_011
firmware[12] = 0b011001000_000_00110101_001000_000_001
firmware[268] = 0b000001001_000_00000000_000000_000_000

#13: X = X - mem[address]
firmware[13] = 0b000001110_000_00110101_101000_001_001
firmware[14] = 0b000001111_000_00010100_100000_010_010
firmware[15] = 0b000010000_000_00010100_000001_000_000
firmware[16] = 0b011001000_000_00111111_000100_000_011

#17: IF X < 0 GOTO address (jn)
firmware[17] = 0b000010010_010_00010100_000000_000_011
firmware[18] = 0b011001000_000_00110101_001000_000_001
firmware[274] = 0b000001001_000_00000000_000000_000_000

#20: X = X * mem[address] (mul)
firmware[20] = 0b000010101_000_00110101_101000_001_001
firmware[21] = 0b000010110_000_00010100_100000_010_010
firmware[22] = 0b000010111_000_00010100_000001_000_000
firmware[23] = 0b011001000_000_00100000_000100_000_011

#25: X = X % mem[address] (mod)
firmware[25] = 0b000011010_000_00110101_101000_001_001
firmware[26] = 0b000011011_000_00010100_100000_010_010
firmware[27] = 0b000011100_000_00010100_000001_000_000
firmware[28] = 0b011001000_000_00100001_000100_000_011

#255: HALT
firmware[255] = 0b00000000000000000000000000000000

firmware[200] = 0b000000000_100_00110101_001000_001_001

def read_regs(reg_num):
   global MDR, PC, MBR, X, Y, H, BUS_A, BUS_B
   
   BUS_A = H
   if reg_num == 0:
      BUS_B = MDR
   elif reg_num == 1:
      BUS_B = PC
   elif reg_num == 2:
      BUS_B = MBR
   elif reg_num == 3:
      BUS_B = X
   elif reg_num == 4:
      BUS_B = Y
   else:
      BUS_B = 0

def write_regs(reg_bits):
   global MAR, MDR, PC, X, Y, H, BUS_C
   
   if reg_bits & 0b100000: MAR = BUS_C
   if reg_bits & 0b010000: MDR = BUS_C
   if reg_bits & 0b001000: PC = BUS_C
   if reg_bits & 0b000100: X = BUS_C
   if reg_bits & 0b000010: Y = BUS_C
   if reg_bits & 0b000001: H = BUS_C

def alu(control_bits):
   global N, Z, BUS_A, BUS_B, BUS_C

   a = BUS_A
   b = BUS_B
   o = 0

   shift_bits = control_bits & 0b11000000
   shift_bits = shift_bits >> 6
   control_bits = control_bits & 0b00111111

   if control_bits == 0b011000: o = a
   elif control_bits == 0b010100: o = b
   elif control_bits == 0b011010: o = ~a
   elif control_bits == 0b101100: o = ~b
   elif control_bits == 0b111100: o = a + b
   elif control_bits == 0b111101: o = a + b + 1
   elif control_bits == 0b111001: o = a + 1
   elif control_bits == 0b110101: o = b + 1
   elif control_bits == 0b111111: o = b - a
   elif control_bits == 0b110110: o = b - 1
   elif control_bits == 0b111011: o = -a
   elif control_bits == 0b001100: o = a & b
   elif control_bits == 0b011100: o = a | b
   elif control_bits == 0b010000: o = 0
   elif control_bits == 0b110001: o = 1
   elif control_bits == 0b110010: o = -1
   elif control_bits == 0b100000: o = b * a
   elif control_bits == 0b100001:
      if a != 0: o = b % a
      else: o = 0

   if o == 0:
      N = 0
      Z = 1
   else:
      N = 1 if o < 0 else 0
      Z = 0

   if shift_bits == 0b01: o = o << 1
   elif shift_bits == 0b10: o = o >> 1
   elif shift_bits == 0b11: o = o << 8

   BUS_C = o
    
def next_instruction(nextadd, jam):
   global MPC
   if jam == 0b000:
      MPC = nextadd
      return
   if jam & 0b001: nextadd = nextadd | (Z << 8)
   if jam & 0b010: nextadd = nextadd | (N << 8)
   if jam & 0b100: nextadd = nextadd | MBR
   MPC = nextadd

def memory_io(mem_bits):
   global PC, MAR, MDR, MBR
   if mem_bits & 0b001: MBR = memory.read_byte(PC)
   if mem_bits & 0b010: MDR = memory.read_word(MAR)
   if mem_bits & 0b100: memory.write_word(MAR, MDR)

def step():
   global MIR, MPC
   
   MIR = firmware[MPC]
   if MIR == 0: return False
   
   read_regs( MIR & 0b00000000000000000000000000000111 )
   alu((MIR & 0b00000000000011111111000000000000) >> 12)
   write_regs( (MIR & 0b00000000000000000000111111000000) >> 6)
   memory_io( (MIR & 0b00000000000000000000000000111000) >> 3 )
   next_instruction(MIR >> 23, (MIR & 0b00000000011100000000000000000000) >> 20)
   
   return True

if __name__ == "__main__":
   import memory 
   
   print('\n')
   print("=== Simulador do Processador ===")
   arquivo_bin = input("Digite o nome do arquivo .bin gerado pelo assembler (ex: out.bin): ").strip()
   
   if not arquivo_bin:
      arquivo_bin = "out.bin"
      print(f"Nenhum arquivo informado. Usando padrão: {arquivo_bin}")
      
   try:
      with open(arquivo_bin, 'rb') as f:
         binary_data = f.read()
         for i, b in enumerate(binary_data):
               memory.write_byte(i, b)

      ciclos = 0
      while step():
         ciclos += 1

      print(f"Total de ciclos de clock gastos: {ciclos}")
      print(f"Resultado salvo na Word 1 (RAM): {memory.read_word(1)}")
      print('\n')
      
   except FileNotFoundError:
      print(f"Erro: Arquivo '{arquivo_bin}' não encontrado.")
      print('\n')