import sys

REGISTERS={
    "zero": "00000",
    "x0": "00000",
    "ra": "00001",
    "x1": "00001",
    "sp": "00010",
    "x2": "00010",
    "gp": "00011",
    "x3": "00011",
    "tp": "00100",
    "x4": "00100",
    "t0": "00101",
    "x5": "00101",
    "t1": "00110",
    "x6": "00110",
    "t2": "00111",
    "x7": "00111",
    "s0": "01000",
    "fp": "01000",
    "x8": "01000",
    "s1": "01001",
    "x9": "01001",
    "a0": "01010",
    "x10": "01010",
    "a1": "01011",
    "x11": "01011",
    "a2": "01100",
    "x12": "01100",
    "a3": "01101",
    "x13": "01101",
    "a4": "01110",
    "x14": "01110",
    "a5": "01111",
    "x15": "01111",
    "a6": "10000",
    "x16": "10000",
    "a7": "10001",
    "x17": "10001",
    "s2": "10010",
    "x18": "10010",
    "s3": "10011",
    "x19": "10011",
    "s4": "10100",
    "x20": "10100",
    "s5": "10101",
    "x21": "10101",
    "s6": "10110",
    "x22": "10110",
    "s7": "10111",
    "x23": "10111",
    "s8": "11000",
    "x24": "11000",
    "s9": "11001",
    "x25": "11001",
    "s10": "11010",
    "x26": "11010",
    "s11": "11011",
    "x27": "11011",
    "t3": "11100",
    "x28": "11100",
    "t4": "11101",
    "x29": "11101",
    "t5": "11110",
    "x30": "11110",
    "t6": "11111",
    "x31": "11111"
}

R_INSTRUCTIONS={
    "add": ("0000000", "000", "0110011"),
    "sub": ("0100000", "000", "0110011"),
    "sll": ("0000000", "001", "0110011"),
    "slt": ("0000000", "010", "0110011"),
    "sltu": ("0000000", "011", "0110011"),
    "xor": ("0000000", "100", "0110011"),
    "srl": ("0000000", "101", "0110011"),
    "or": ("0000000", "110", "0110011"),
    "and": ("0000000", "111", "0110011")
}

I_ARTH={
    "addi": ("000", "0010011"),
    "sltiu":("011", "0010011"),
}

I_LOAD={
    "lw":  ("010", "0000011"),
}

I_JUMP={
    "jalr": ("000", "1100111")
}


B_INSTRUCTIONS={
    "beq": ("000", "1100011"),
    "bne": ("001", "1100011"),
    "blt": ("100", "1100011"),
    "bge": ("101", "1100011"),
    "bltu": ("110", "1100011"),
    "bgeu": ("111", "1100011")
}

S_INSTRUCTIONS={
    "sw":  ("010", "0100011")
}

U_INSTRUCTIONS={
    "lui":   "0110111",
    "auipc": "0010111"
}

J_INSTRUCTIONS={
    "jal": "1101111"
}

def bin_12(a):
    a=bin(a)[2:]
    if len(a)<12:
        b=a[::-1]
        while(len(b)!=12):
            b+="0"
        a=b[::-1]
    else:
        pass
    return a
    
def bin_20(a):
    a=bin(a)[2:]
    if len(a)<20:
        b=a[::-1]
        while(len(b)!=20):
            b+="0"
        a=b[::-1]
    else:
        pass
    return a

def r_inst(a,b,c,d):
    print(R_INSTRUCTIONS[a][0],end="")
    p=b.rstrip(",")
    q=c.rstrip(",")
    print(REGISTERS[d],end="")
    print(REGISTERS[q],end="")
    print(R_INSTRUCTIONS[a][1],end="")
    print(REGISTERS[p],end="")
    print(R_INSTRUCTIONS[a][2],end="")
    print()

def b_inst(a,b,c,d,e):
    e = int(e) // 2
    if int(e)<0:
        e=(2**12)+int(e)
    m=int(e)
    m=bin_12(m)
    imm12=m[0]
    imm10_5=m[2:8]
    imm4_1=m[8:12]
    imm11=m[1]
    b=b.rstrip(",")
    c=c.rstrip(",")
    print(imm12+imm10_5,end="")
    print(REGISTERS[c],end="")
    print(REGISTERS[b],end="")
    print(B_INSTRUCTIONS[a][0],end="")
    print(imm4_1+imm11,end="")
    print(B_INSTRUCTIONS[a][1],end="")
    print()

def i_arth(a,b,c,d):
    if int(d)<0:
        d=(2**12)+int(d)
    m=bin_12(int(d))
    print(m,end="")
    b=b.rstrip(",")
    c=c.rstrip(",")
    print(REGISTERS[c],end="")
    print(I_ARTH[a][0],end="")
    print(REGISTERS[b],end="")
    print(I_ARTH[a][1],end="")
    print()

def s_inst(a,b,c):
    d=c.split("(")
    e=d[0]
    f=d[1]
    f=f.rstrip(")")
    if int(e)<0:
        e=(2**12)+int(e)
    m=int(e)
    m=bin_12(m)
    n=m[:7]
    o=m[7:]
    print(n,end="")
    b=b.rstrip(",")
    print(REGISTERS[b],end="")
    print(REGISTERS[f],end="")
    print(S_INSTRUCTIONS[a][0],end="")
    print(o,end="")
    print(S_INSTRUCTIONS[a][1],end="")
    print()

def u_inst(a,b,c):
    t=int(c)
    c=bin_20(t)
    b=b.rstrip(",")
    print(c,end="")
    print(REGISTERS[b],end="")
    print(U_INSTRUCTIONS[a],end="")
    print()

def j_inst(a,b,c,d):
    d=int(d)//2
    if int(d)<0:
        d=(2**20)+int(d)
    m=int(d)
    m=bin_20(m)
    imm20 = m[0]
    imm19_12 = m[1:9]
    imm11 = m[9]
    imm10_1 = m[10:20]
    b=b.rstrip(",")
    print(imm20 + imm10_1 + imm11 + imm19_12, end="")
    print(REGISTERS[b], end="")
    print(J_INSTRUCTIONS[a], end="")
    print()

def i_load(a,b,c):
    d=c.split("(")
    e=d[0]
    f=d[1]
    f=f.rstrip(")")
    if int(e)<0:
        e=(2**12)+int(e)
    m=int(e)
    m=bin_12(m)
    print(m,end="")
    b=b.rstrip(",")
    print(REGISTERS[f],end="")
    print(I_LOAD[a][0],end="")
    print(REGISTERS[b],end="")
    print(I_LOAD[a][1],end="")
    print()

def i_jump(a,b,c,d):
    if int(d)<0:
        d=(2**12)+int(d)
    m=int(d)
    m=bin_12(m)
    print(m,end="")
    b=b.rstrip(",")
    c=c.rstrip(",")
    print(REGISTERS[c],end="")
    print(I_JUMP[a][0],end="")
    print(REGISTERS[b],end="")
    print(I_JUMP[a][1],end="")
    print()

def error_det(t,k,labels):
    for i in range(len(k)):
        if (k[i] not in R_INSTRUCTIONS and k[i] not in I_ARTH and k[i] not in I_JUMP and k[i] not in I_LOAD and k[i] not in U_INSTRUCTIONS and k[i] not in J_INSTRUCTIONS and k[i] not in S_INSTRUCTIONS and k[i] not in B_INSTRUCTIONS):
            print(f'Wrong instruction name "{k[i]}" at line number {i+1}')
            return -1
    
    for i in range(len(t)):
        if k[i] in R_INSTRUCTIONS:
            if len(t[i][1:])<3:
                print(f'Less number of arguments than required at line {i+1}')
                return -1
        if k[i] in I_ARTH:
            if len(t[i][1:])<3:
                print(f'Less number of arguments than required at line {i+1}')
                return -1
        if k[i] in I_JUMP:
            if len(t[i][1:])<3:
                print(f'Less number of arguments than required at line {i+1}')
                return -1
        if k[i] in I_LOAD:
            if len(t[i][1:])<2:
                print(f'Less number of arguments than required at line {i+1}')
                return -1
        if k[i] in B_INSTRUCTIONS:
            if len(t[i][1:])<3:
                print(f'Less number of arguments than required at line {i+1}')
                return -1
        if k[i] in S_INSTRUCTIONS:
            if len(t[i][1:])<2:
                print(f'Less number of arguments than required at line {i+1}')
                return -1
        if k[i] in U_INSTRUCTIONS:
            if len(t[i][1:])<2:
                print(f'Less number of arguments than required at line {i+1}')
                return -1
        if k[i] in J_INSTRUCTIONS:
            if len(t[i][1:])<2:
                print(f'Less number of arguments than required at line {i+1}')
                return -1

    for i in range(len(t)):
        if k[i] in S_INSTRUCTIONS or k[i] in I_LOAD:
            try:
                z=t[i][2]
                q=z.split("(")[1].rstrip(")")
            except:
                print(f"Formatting not done properly at line number {i+1}")
                return -1

    reg=[]
    for i in range(len(t)):
        if k[i] in R_INSTRUCTIONS:
            reg.append([t[i][1].rstrip(","),t[i][2].rstrip(","),t[i][3]])
        if k[i] in I_ARTH:
            reg.append([t[i][1].rstrip(","),t[i][2].rstrip(",")])
        if k[i] in I_JUMP:
            reg.append([t[i][1].rstrip(","), t[i][2].rstrip(",")])
        if k[i] in I_LOAD:
            z=t[i][2]
            if z[-1]==")":
                q=z.split("(")[1].rstrip(")")
            else:
                print(f"Formatting not done properly at line number {i+1}")
                return -1
            reg.append([t[i][1].rstrip(","),q])
        if k[i] in B_INSTRUCTIONS:
            reg.append([t[i][1].rstrip(","),t[i][2].rstrip(",")])
        if k[i] in S_INSTRUCTIONS:
            z=t[i][2]
            if z[-1]==")":
                q=z.split("(")[1].rstrip(")")
            else:
                print(f"Formatting not done properly at line number {i+1}")
                return -1
            reg.append([t[i][1].rstrip(","),q])
        if k[i] in U_INSTRUCTIONS:
            reg.append([t[i][1].rstrip(",")])
        if k[i] in J_INSTRUCTIONS:
            reg.append([t[i][1].rstrip(",")])

    for i in range(len(reg)):
        for j in reg[i]:
            if j not in REGISTERS:
                print(f'Wrong register name {j} at line number {i+1}')
                return -1
    
    for i in range(len(t)): 
        if k[i] in I_ARTH:
            try:
                if (int(t[i][3])>2047 or int(t[i][3])<-2048):
                    print(f'Wrong immediate value at line number {i+1}')
                    return -1
            except ValueError:
                print(f"Wrong immediate value given at line number {i+1}")
                return -1
        if k[i] in I_JUMP:
            try:
                if (int(t[i][3])>2047 or int(t[i][3])<-2048):
                    print(f'Wrong immediate value at line number {i+1}')
                    return -1
            except ValueError:
                print(f"Wrong immediate value given at line number {i+1}")
                return -1
        if k[i] in I_LOAD:
            d=t[i][2].split("(")
            try:
                if (int(d[0])>2047 or int(d[0])<-2048):
                    print(f'Wrong immediate value at line number {i+1}')
                    return -1
            except ValueError:
                print(f"Wrong immediate value given at line number {i+1}")
                return -1
        if k[i] in S_INSTRUCTIONS:
            d=t[i][2].split("(")
            try:
                if (int(d[0])>2047 or int(d[0])<-2048):
                    print(f'Wrong immediate value at line number {i+1}')
                    return -1
            except ValueError:
                print(f"Wrong immediate value given at line number {i+1}")
                return -1
        if k[i] in U_INSTRUCTIONS:
            try:
                if (int(t[i][2])>1048575 or int(t[i][2])<0):
                    print(f'Wrong immediate value at line number {i+1}')
                    return -1
            except ValueError:
                print(f"Wrong immediate value given at line number {i+1}")
                return -1
        
    for i in range(len(t)):
        if k[i] in B_INSTRUCTIONS:
            if t[i][3] not in labels:
                try:
                    int(t[i][3])
                except:
                    print(f"{t[i][3]} label not found at line number {i+1}")
                    return -1
        if k[i] in J_INSTRUCTIONS:
            if t[i][2] not in labels:
                try:
                    int(t[i][2])
                except:
                    print(f"{t[i][2]} label not found at line number {i+1}")
                    return -1
