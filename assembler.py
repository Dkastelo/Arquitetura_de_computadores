PROLOGUE_SIZE = 4

instruction_set = {
    'ld'   :  0x01, 
    'add'  :  0x02, 
    'sub'  :  0x0D, 
    'goto' :  0x09, 
    'mov'  :  0x06,  
    'jz'   :  0x0B, 
    'halt' :  0xFF,
    'jn'   :  0x11, 
}
lines = []       # armazena as linhas limpas
labels = {}      # tabela de Símbolos ('nome': endereco_byte)
binary_data = bytearray() 

def open_archive(file_path):
    try:
        with open(file_path, 'r') as fsrc:
            for line in fsrc:
                line = line.strip().lower().replace(',', '').split()
                if line:
                    lines.append(line)
        return True
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não foi encontrado.")
        return False

def calculate_instruction_size(inst, ops):
    if (inst == 'halt') or (inst == 'wb'):
        return 1
    elif (inst in ['ld', 'add', 'sub', 'mov', 'jz', 'goto', 'jn']):
        return 2
    elif (inst == 'ww'):
        return 4
    else:
        return 0

def _find_first_code_label():
    for line in lines:
        if (line[0] not in instruction_set) and (line[0] not in ('wb', 'ww')):
            if (len(line) > 1) and (line[1] not in ('wb', 'ww')):
                return line[0]
        elif line[0] in instruction_set:
            return None
    return None


def first_look():
    actual_adress = PROLOGUE_SIZE # já existe um byte 0 padrão na posição 0

    for line in lines:
        if (line[0] in instruction_set) or line[0] in ['wb', 'ww']:
            inst = line[0]
            ops = line[1:]
            actual_adress += calculate_instruction_size(inst, ops)
        else:
            label_name = line[0]
            labels[label_name] = actual_adress

            if (len(line) > 1):
                inst = line[1]
                ops = line[2:]
                actual_adress += calculate_instruction_size(inst, ops)


def encode_math(inst, ops):
    generated_bytes = []

    if len(ops) > 1:
        if ops[0] == 'x':
            var_name = ops[1]
        elif ops[1] == 'x':
            var_name = ops[0]
        else:
            return generated_bytes

        if var_name in labels:
            byte_adress = labels[var_name]
            divided_adress = byte_adress // 4
            
            generated_bytes.append(instruction_set[inst])
            generated_bytes.append(divided_adress)
    return generated_bytes

def encode_jump(inst, ops):
    generated_bytes = []

    if (len(ops) > 0):
        label_name = ops[0]
        if (label_name in labels):
            generated_bytes.append(instruction_set[inst])
            generated_bytes.append(labels[label_name])
    return generated_bytes

def encode_ww(inst, ops):
        generated_bytes = []
        if (len(ops)) > 0:
            try:
                val = int(ops[0])
                
                generated_bytes.append(val & 0xFF)
                generated_bytes.append((val & 0xFF00) >> 8)
                generated_bytes.append((val & 0xFF0000) >> 16)
                generated_bytes.append((val & 0xFF000000) >> 24)
            except ValueError:
                pass 
        return generated_bytes

def second_look(destination_path):
    routes = {
        'ld'   : encode_math,
        'add'  : encode_math,
        'sub'  : encode_math,
        'mov'  : encode_math,
        'goto' : encode_jump,
        'jz'   : encode_jump,
        'jn'   : encode_jump,
        'ww'   : encode_ww
    }

    first_code = _find_first_code_label()
    if (first_code is not None):
        code_addr = labels[first_code]
        binary_data.append(instruction_set['goto'])
        binary_data.append(code_addr)
        binary_data.append(0x00)
        binary_data.append(0x00)
    else:
        for k in labels:
            labels[k] -= PROLOGUE_SIZE
    
    for tokens in lines:
        if (tokens[0] in instruction_set) or (tokens[0] in ['wb', 'ww']):
            inst = tokens[0]
            ops = tokens[1:]
        else:
            if (len(tokens) > 1):
                inst = tokens[1]
                ops = tokens[2:]
            else:
                continue
        
        if (inst == 'halt'):
            binary_data.append(instruction_set['halt'])
        elif (inst in routes):
            instruction_bytes = routes[inst](inst, ops)
            if (not instruction_bytes):
                print(f"erro de sintaxe na instrução {inst} {ops}")
                return False
            binary_data.extend(instruction_bytes)
        else:
            print(f'o assembler não soube oq fazer aqq {inst}')
            return False
    
    try:
        with open(destination_path, 'wb') as fdst:
            fdst.write(binary_data)
        return True
    except Exception as e:
        print(f'erro ao gravar arquivo final: {e}')
        return False

def run(destination_path):        
    first_look()
    second_look(destination_path)
