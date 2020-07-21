#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Assembly Simulator project 2020
# GNU General Public License v3.0

import logging
from bitarray import bitarray

# About Flag register:
# Flags in the register are represented like  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | CF | ZF | OF | SF |

logging.basicConfig(filename="../log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('funclogger')


def load_store(operands, flag_register):
    """
    Loads value from memory to register
    /
    Stores value from register in the memory
    Zero operand is the value of destination
    First one is the value to be stored
    :param operands: list of operands
    :param flag_register: Flag register
    :return: value of the register/memory
    """
    return operands[1]


def mov_low(operands, flag_register):
    """
    Writes immediate constant into the low byte of the register,
    setting high byte to all zeros
    Zero operand is the value of the register object, which will be the destination
    for writing information into it
    First one is the value of the immediate constant
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the register
    """
    return bitarray("0" * 8) + operands[1]


def mov_high(operands, flag_register):
    """
    Writes immediate constant into the high byte of the register,
    does not affect the low byte
    Zero operand is the value of the register object, which will be the destination
    for writing information into it
    First one is the value of the immediate constant
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the register
    """
    return operands[0][:8] + operands[1]


def mov(operands, flag_register):
    """
    Writes register value into another register
    Zero operand is the value of the register object, which will be the destination
    for writing information into it
    First one is the value of the second register, which will be written
    into the first one
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the register
    """
    return bitarray(operands[1].to01())


def add(operands, flag_register):
    """
    Performs addition of two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (first operand in the operation)
    Second one is the value of the third register (second operand in the operation)
    Third one is the value of Flag register
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the first register
    """
    reg1 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    reg2 = twos_complement(int(operands[2].to01(), 2), len(operands[2]))
    result = bin(twos_complement(reg1 + reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if len(result) > 16:
        flag_register._state[12] = "1"  # Carry flag
        result = bin(twos_complement(reg1 + reg2, 18))[-16:]
    if operands[1].to01()[0] == operands[2].to01()[0] != result[0]:
        flag_register._state[14] = "1"  # Overflow flag
    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def sub(operands, flag_register):
    """
    Performs subtraction of two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (first operand in the operation)
    Second one is the value of the third register (second operand in the operation)
    Third one is the value of Flag register
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the first register
    """
    reg1 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    reg2 = twos_complement(int(operands[2].to01(), 2), len(operands[2]))
    result = bin(twos_complement(reg1 - reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if len(result) > 16:
        flag_register._state[12] = "1"  # Carry flag
        result = bin(twos_complement(reg1 + reg2, 18))[-16:]
    if operands[1].to01()[0] == operands[2].to01()[0] != result[0]:
        flag_register._state[14] = "1"  # Overflow flag
    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def mul(operands, flag_register):
    """
    Performs multiplication of two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (first operand in the operation)
    Second one is the value of the third register (second operand in the operation)
    Third one is the value of Flag register
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the first register
    """
    reg1 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    reg2 = twos_complement(int(operands[2].to01(), 2), len(operands[2]))
    result = bin(twos_complement(reg1 * reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if len(result) > 16:
        flag_register._state[12] = "1"  # Carry flag
        result = bin(twos_complement(reg1 + reg2, 18))[-16:]
    if operands[1].to01()[0] == operands[2].to01()[0] != result[0]:
        flag_register._state[14] = "1"  # Overflow flag
    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def div(operands, flag_register):
    """
    Performs division of two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (first operand in the operation)
    Second one is the value of the third register (second operand in the operation)
    Third one is the value of Flag register
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the first register
    """
    reg1 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    reg2 = twos_complement(int(operands[2].to01(), 2), len(operands[2]))
    result = bin(twos_complement(reg1 // reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if len(result) > 16:
        flag_register._state[12] = "1"  # Carry flag
        result = bin(twos_complement(reg1 + reg2, 18))[-16:]
    if operands[1].to01()[0] == operands[2].to01()[0] != result[0]:
        flag_register._state[14] = "1"  # Overflow flag
    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def bit_and(operands, flag_register):
    """
    Performs bitwise and on two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (first operand in the operation)
    Second one is the value of the third register (second operand in the operation)
    Third one is the value of Flag register
    :param operands: list of operands
     :param flag_register: Flag register
   :return: new value of the first register
    """
    reg1 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    reg2 = twos_complement(int(operands[2].to01(), 2), len(operands[2]))
    result = bin(twos_complement(reg1 & reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def bit_or(operands, flag_register):
    """
    Performs bitwise or on two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (first operand in the operation)
    Second one is the value of the third register (second operand in the operation)
    Third one is the value of Flag register
    :param operands: list of operands
     :param flag_register: Flag register
   :return: new value of the first register
    """
    reg1 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    reg2 = twos_complement(int(operands[2].to01(), 2), len(operands[2]))
    result = bin(twos_complement(reg1 | reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def bit_xor(operands, flag_register):
    """
    Performs bitwise xor on two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (first operand in the operation)
    Second one is the value of the third register (second operand in the operation)
    Third one is the value of Flag register
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the first register
    """
    reg1 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    reg2 = twos_complement(int(operands[2].to01(), 2), len(operands[2]))
    result = bin(twos_complement(reg1 ^ reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def bit_not(operands, flag_register):
    """
    Performs bitwise and on two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (main operand in the operation)
    Second one is the value of Flag register
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the first register
    """
    result = operands[1].to01()
    result.replace("1", "2")
    result.replace("0", "1")
    result.replace("2", "0")

    flag_register._state = bitarray("0" * 16)

    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] != operands[1][0]:
        flag_register._state[14] = "1"  # Overflow flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def lsh(operands, flag_register):
    """
    Performs bitwise xor on two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (first operand in the operation)
    Second one is the value of the third register (second operand in the operation)
    Third one is the value of Flag register
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the first register
    """
    reg1 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    reg2 = twos_complement(int(operands[2].to01(), 2), len(operands[2]))
    result = bin(twos_complement(reg1 << reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if len(result) > 16:
        flag_register._state[12] = "1"  # Carry flag
        result = bin(twos_complement(reg1 + reg2, 18))[-16:]
    if operands[1].to01()[0] == operands[2].to01()[0] != result[0]:
        flag_register._state[14] = "1"  # Overflow flag
    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def rsh(operands, flag_register):
    """
    Performs bitwise xor on two registers, saving the result in the third one
    Zero operand the value of the first register
    First one is the value of the second register (first operand in the operation)
    Second one is the value of the third register (second operand in the operation)
    Third one is the value of Flag register
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the first register
    """
    reg1 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    reg2 = twos_complement(int(operands[2].to01(), 2), len(operands[2]))
    result = bin(twos_complement(reg1 >> reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if len(result) > 16:
        flag_register._state[12] = "1"  # Carry flag
        result = bin(twos_complement(reg1 + reg2, 18))[-16:]
    if operands[1].to01()[0] == operands[2].to01()[0] != result[0]:
        flag_register._state[14] = "1"  # Overflow flag
    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return bitarray(result)


def cmp(operands, flag_register):
    """
    Compares two registers by subtraction of their values
    Only affects flags
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the flag register
    """
    reg1 = twos_complement(int(operands[0].to01(), 2), len(operands[0]))
    reg2 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    result = bin(twos_complement(reg1 - reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")

    flag_register._state = bitarray("0" * 16)

    if len(result) > 16:
        flag_register._state[12] = "1"  # Carry flag
    if operands[0].to01()[0] == operands[1].to01()[0] != result[0]:
        flag_register._state[14] = "1"  # Overflow flag
    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return flag_register._state


def test(operands, flag_register):
    """
    Compares two registers by performing bitwise "and" on their values
    Only affects flags
    :param operands: list of operands
    :param flag_register: Flag register
    :return: new value of the flag register
    """
    reg1 = twos_complement(int(operands[0].to01(), 2), len(operands[0]))
    reg2 = twos_complement(int(operands[1].to01(), 2), len(operands[1]))
    result = bin(twos_complement(reg1 & reg2, len(operands[1])))[2:]

    result = result.rjust(16, "0")
    flag_register._state = bitarray("0" * 16)

    if result == "0" * 16:
        flag_register._state[13] = "1"  # Zero flag
    if result[0] == "1":
        flag_register._state[14] = "1"  # Sign flag

    return flag_register._state


def twos_complement(val, bits):
    """
    Works with signed bit numbers
    :param val: int - int value of the bit number
    :param bits: int - length of the bit number
    """
    if val < 0:
        val = (1 << bits) + val
    else:
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)
    return val


functions_dictionary = {"load": load_store, "mov_low": mov_low,
                        "mov_high": mov_high, "mov": mov, "add": add,
                        "sub": sub, "mul": mul, "div": div,
                        "and": bit_and, "or": bit_or,
                        "xor": bit_xor, "not": bit_not,
                        "store": load_store, "cmp": cmp,
                        "lsh": lsh, "rsh": rsh, "test": test}