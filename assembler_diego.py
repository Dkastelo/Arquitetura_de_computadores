import sys

PROLOGUE_SIZE = 4

class Assembler:
    def __init__(self):
        self.instruction_set = {
            'add': 0x02, 'sub': 0x0D, 'goto': 0x09, 
            'mov': 0x06, 'jz': 0x0B, 'halt': 0xFF
        }
        self.lines = []       # armazena as linhas limpas
        self.labels = {}      # tabela de Símbolos ('nome': endereco_byte)
        self.binary_data = bytearray([0]) 

    def open_archive(self, file_path):
        try:
            with open(file_path, 'r') as fsrc:
                for line in fsrc:
                    line = line.strip().lower().replace(',', '').split()
                    if line:
                        self.lines.append(line)
            return True
        except FileNotFoundError:
            print(f"Erro: Arquivo '{file_path}' não foi encontrado.")
            return False

    def calculate_instruction_size(self, inst, ops):
        if (inst == 'halt') or (inst == 'wb'):
            return 1
        elif (inst in ['add', 'sub', 'mov', 'jz', 'goto']):
            return 2
        elif (inst == 'ww'):
            return 4
        else:
            return 0
    
    def _find_first_code_label(self):
        for line in self.lines:
            if (line[0] not in self.instruction_set) and (line[0] not in ('wb', 'ww')):
                if (len(line) > 1) and (line[1] not in ('wb', 'ww')):
                    return line[0]
            elif line[0] in self.instruction_set:
                return None
        return None


    def first_look(self):
        actual_adress = PROLOGUE_SIZE # já existe um byte 0 padrão na posição 0

        for line in self.lines:
            if (line[0] in self.instruction_set) or line[0] in ['wb', 'ww']:
                inst = line[0]
                ops = line[1:]
                actual_adress += self.calculate_instruction_size(inst, ops)
            else:
                label_name = line[0]
                self.labels[label_name] = actual_adress

                if (len(line) > 1):
                    inst = line[1]
                    ops = line[2:]
                    actual_adress += self.calculate_instruction_size(inst, ops)


    def encode_math(self, inst, ops):
        generated_bytes = []

        if len(ops) > 1:
            if ops[0] == 'x':
                var_name = ops[1]
            elif ops[1] == 'x':
                var_name = ops[0]
            else:
                return generated_bytes

            if var_name in self.labels:
                byte_adress = self.labels[var_name]
                divided_adress = byte_adress // 4
                
                generated_bytes.append(self.instruction_set[inst])
                generated_bytes.append(divided_adress)
        return generated_bytes
    
    def encode_jump(self, inst, ops):
        generated_bytes = []

        if (len(ops) > 0):
            label_name = ops[0]
            if (label_name in self.labels):
                generated_bytes.append(self.instruction_set[inst])
                generated_bytes.append(self.labels[label_name])
        return generated_bytes
    
    def encode_ww(self, inst, ops):
        generated_bytes = []

        if (len(ops) > 0) and (ops[0].isnumeric()):
            val = int(ops[0])
            generated_bytes.append(val & 0xFF)
            generated_bytes.append((val & 0xFF00) >> 8)
            generated_bytes.append((val & 0xFF0000) >> 16)
            generated_bytes.append((val & 0xFF000000) >> 24)
        return generated_bytes

    def second_look(self, destination_path):
        routes = {
            'add'  : self.encode_math,
            'sub'  : self.encode_math,
            'mov'  : self.encode_math,
            'goto' : self.encode_jump,
            'jz'   : self.encode_jump,
            'ww'   : self.encode_ww
        }

        first_code = self._find_first_code_label()
        if (first_code is not None):
            code_addr = self.labels[first_code]
            self.binary_data.append(self.instruction_set['goto'])
            self.binary_data.append(code_addr)
            self.binary_data.append(0x00)
            self.binary_data.append(0x00)
        else:
            for k in self.labels:
                self.labels[k] -= PROLOGUE_SIZE

        for tokens in self.lines:
            if (tokens[0] in self.instruction_set) or (tokens[0] in ['wb', 'ww']):
                inst = tokens[0]
                ops = tokens[1:]
            else:
                if (len(tokens) > 1):
                    inst = tokens[1]
                    ops = tokens[2:]
                else:
                    continue
            
            if (inst == 'halt'):
                self.binary_data.append(self.instruction_set['halt'])
            elif (inst in routes):
                instruction_bytes = routes[inst](inst, ops)
                if (not instruction_bytes):
                    print(f"erro de sintaxe na instrução {inst} {ops}")
                    return False
                self.binary_data.extend(instruction_bytes)
            else:
                print(f'o assembler não soube oq fazer aqq {inst}')
                return False
        
        try:
            with open(destination_path, 'wb') as fdst:
                fdst.write(self.binary_data)
            print('sucesso! arquivo gerado')
            return True
        except Exception as e:
            print(f'erro ao gravar arquivo final: {e}')
            return False


    def run(self, destination_path):
        # ? *SE PA EU APAGO ISSO NE*
        print(f"linhas carregadas para processamento: {len(self.lines)}")
        
        self.first_look()
        print('iniciando segunda olhada')
        self.second_look(destination_path)


if (len(sys.argv) < 3):
    print("digite: python3 assembler_diego.py arquivo.asm destino.bin")
else:
    asm = Assembler()
    if (asm.open_archive(sys.argv[1])):
        asm.run(sys.argv[2])
