
all: helloworld_opaque helloworld_normal

helloworld_opaque: helloworld.c
	$(SCC) $? -f elf --anti-disasm --anti-disasm-freq 1 -o $@

helloworld_normal: helloworld.c
	$(SCC) $? -f elf -o $@

clean:
	rm -f helloworld_normal helloworld_opaque
