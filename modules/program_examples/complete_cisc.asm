# There are 89 (I think?) different instructions for CISC ISA
# (counting different operand types for the same instructions)
# This assembly program aims to meaningfully test all of them, with edge cases considered
#########################################################################################
mov %R00, $512
mov %R01, %R00
mov %R00, [%R01]
mov %R00, [%R01+$2]
mov [%R01], %R00
mov [%R01], $666
mov %R01, $128
mov [%R01+$2], %R01
mov [%R01+$2], $512
push %R01
push $512
pop %R01
enter $5
leave
add %R00, [%R00]
add %R00, %R01
add %R01, [%R01+$2]
mov %R00, $512
add [%R00], %R00
mov %R01, $514
sub %R01, [%R01]
sub %R00, %R01
sub %R00, [%R00+$2]
mov %R00, $514
sub %R00, [%R00+$-2]
inc %R00
inc [%R01]
inc [%R01+$2]
dec %R00
dec [%R01]
dec [%R01+$2]
mov %R00, $2
mov %R01, $6
mov %R02, $514
mul %R00, %R01
div %R00, %R01
mul %R00, [%R02]
div %R00, [%R02]
mul [%R02], %R00
div [%R02], %R00
mul %R01, $3
div %R01, $3
mov %R02, $512
mul %R00, [%R02+$2]
div %R00, [%R02+$2]
and %R00, %R01
mov %R01, $5
or %R00, %R01
and %R00, [%R02]
or %R00, [%R02]
mov %R00, $5
mov %R01, $2
xor %R00, %R01
xor %R00, [%R02]
not %R00
not [%R02]
mov %R00, $4
lsh %R00, $1
rsh %R00, $1
rsh [%R02], $1
lsh [%R02], $1
rsh [%R02+$2], $1
lsh [%R02+$2], $1
call $2
nop
call %R00
call %R00+$1
jmp $5
nop
ret
nop
ret
nop
jmp %R00
cmp %R00, $-5
je $4
nop
mov %R00, $-5
jmp %R00+$1
cmp %R00, %R01
jne $2
nop
cmp %R00, [%R02]
jg $5
jl $2
nop
mov %R00, $512
cmp %R00, [%R02+$2]
jl $2
jge $2
jmp $2
jle $-1
test %R00, %R01
test %R00, [%R02]
test %R00, [%R02+$2]
in %R00, $1
in [%R02], $1
in [%R02+$2], $1
out $1, %R00
out $1, [%R02]
out $1, [%R02+$2]
mov %R02, $512
load4 [%R02]
mov %R02, $256
store4 [%R02]
mov %R00, $1
add4 [%R02], %R00
sub4 [%R02], %R00
mov %R00, $2
mul4 [%R02], %R00
div4 [%R02], %R00