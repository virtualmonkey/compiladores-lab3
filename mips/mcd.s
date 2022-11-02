# code extracted from https://stackoverflow.com/questions/59151329/recursion-greatest-common-divisor-in-mips

.data
n1: .word 54
n2: .word 18

.text
.globl main
main:
    lw $a0,n1  # load value n1
    lw $a1,n2  #load value n2
    jal GCD # call funtion GCD

    add $a0,$v0,$zero 
    li $v0,1
    syscall # print result
li $v0, 10 # exit program 
syscall

GCD:
    #GCD(n1, n2)
    # n1 = $a0
    # n2 = $a1

    addi $sp, $sp, -12
    sw $ra, 0($sp) # save function into stack
    sw $s0, 4($sp) # save value $s0 into stack 
    sw $s1, 8($sp) # save value $s1 into stack 

    add $s0, $a0, $zero # s0 = a0 ( value n1 ) 
    add $s1, $a1, $zero # s1 = a1 ( value n2 ) 

    addi $t1, $zero, 0 # $t1 = 0
    beq $s1, $t1, returnn1 # if s1 == 0 returnn1

    add $a0, $zero, $s1 # make a0 = $s1
    div $s0, $s1 # n1/n2
    mfhi $a1 # reminder of n1/n2 which is equal to n1%n2

    jal GCD

exitGCD:
    lw $ra, 0 ($sp)  # read registers from stack
    lw $s0, 4 ($sp)
    lw $s1, 8 ($sp)
    addi $sp,$sp , 12 # bring back stack pointer
    jr $ra
returnn1:
    add $v0, $zero, $s0 # return $v0 = $s0 ( n1)
    j exitGCD