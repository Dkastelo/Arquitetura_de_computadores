import memory
import sys
import disk
import clock
import processor as cpu

disk.read(str(sys.argv[1]))

memory.write_word(2, 55)
memory.write_word(3, 0)

print('Antes do processamento:')
print(f"Word 0: {memory.read_word(0)}")
print(f"Word 1: {memory.read_word(1)}")
print(f"Word 2: {memory.read_word(2)}")
print(f"Word 3: {memory.read_word(3)}")

print('\nProcessando...')

clock.start([cpu])

print('\nDepois do processamento:')
print(f"Word 0: {memory.read_word(0)}")
print(f"Word 1: {memory.read_word(1)}")
print(f"Word 2: {memory.read_word(2)}")
print(f"Word 3: {memory.read_word(3)}")