addi $1, $0, 5
addi $2, $0, 60
sw_loop:
#sw $1, 0x2000($2)
addi $2, $2, -4
beq $2, $0, out
add $1, $1, $1
sub $1, $0, $1
addi $1, $1, 3
beq $3, $3, sw_loop
out:
addi $6, $0, 60
loop:
add $4, $0, $0
lw $1, 0x2004($2)
xor $4, $4, $1
lw $1, 0x2008($2)
xor $4, $4, $1
lw $1, 0x200c($2)
xor $4, $4, $1
#sw $4, 0x2004($2)
xor $5, $5, $4
addi $2, $2, 4
bne $2, $6, loop
#sw $5, 0x2000($0)
end: beq $0, $0, end
