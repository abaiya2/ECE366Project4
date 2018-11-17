addi $1, $0, 2
addi $2, $0, 28
sw_loop:
sw $1, 0x2000($2)
addi $2, $2, -4
beq $2, $0, out
add $1, $1, $1
sub $1, $0, $1
addi $1, $1, 3
beq $3, $3, sw_loop
out:
addi $5, $0, 32
lw_loop:
lw $1, 0x2000($2)
slt $3, $1, $0
beq $3, $0, skip
add $4, $4, $1
skip:
addi $2, $2, 4
bne $2, $5, lw_loop
sw $4, 0x2000($0)
end: beq $0, $0, end