import sys

def decode(s):
    t=s[-1:-8:-1]
    opcode=t[::-1]
    #R instruction
    if opcode=="0110011":
        a=s[-20:-15]
        b=s[-25:-20]
        c=s[-12:-7]
        funct7=s[-32:-25]
        funct3=s[-15:-12]
        return a,b,c,funct3,funct7

    #I instructions
    elif opcode=="0000011" or opcode=="0010011" or opcode=="1100111":
        a=s[-20:-15]
        b=s[-32:-20]
        c=s[-12:-7]
        funct3=s[-15:-12]
        return a,b,c,funct3,None       

    #sw
    elif opcode=="0100011":
        funct3=s[-15:-12]
        a=s[-20:-15]
        b=s[-25:-20]
        c=s[-32:-25]+s[-12:-7]
        return a,b,c,funct3,None

    #B instructions
    elif opcode=="1100011":
        a=s[-20:-15]
        b=s[-25:-20]
        c=s[-32]+s[-8]+s[-31:-25]+s[-12:-8]+"0"
        funct3=s[-15:-12]
        return a,b,c,funct3,None
    
    #U instructions
    elif opcode=="0110111" or opcode=="0010111":
        a=s[-32:-12]
        c=s[-12:-7]
        return a,None,c,None,None

    #jal
    elif opcode=="1101111":
        a=s[-32]+s[-20:-12]+s[-21]+s[-31:-21]+"0"
        c=s[-12:-7]
        return a,None,c,None,None
    return None

def execute(s,registers,mem,r1,r2,rd,f3,f7,pc,l_no):
    t=s[-1:-8:-1]
    opcode=t[::-1]
    res=0

    #R instruction
    if opcode=="0110011":
        a=s_i(r1)
        b=s_i(r2)
        c=s_i(rd)
        if f3=="000" and f7=="0000000":
            res=n(registers[a]+registers[b])
        elif f3=="000" and f7=="0100000":
            res=n(registers[a]-registers[b])
        elif f3=="001":
            d=registers[b]%32
            res=registers[a]*(2**d)
            res=n(res%(2**32))
        elif f3=="010":
            if registers[a]<registers[b]:
                res=1
            else:
                res=0
        elif f3=="011":
            x=registers[a]
            y=registers[b]
            if x<0:
                x+=2**32
            if y<0:
                y+=2**32
            if x<y:
                res=1
            else:
                res=0
        elif f3=="100":
            res=n(registers[a]^registers[b])
        elif f3=="101":
            x=registers[a]
            y=registers[b]
            d=y%32
            if x<0:
                x+=2**32
            res=n(x//(2**d))
        elif f3=="110":
            res=n(registers[a]|registers[b])
        elif f3=="111":
            res=n(registers[a]&registers[b])
        else:
            print(f'Invalid funct3 or funct7 value at line no. {l_no}')
            registers[0]=0
            return -1
        registers[0]=0

    #lw
    elif opcode=="0000011":
        if f3!="010":
            print(f'Invalid funct3 value at line no. {l_no}')
            return -1
        a=s_i(r1)
        b=s_i(r2)
        c=s_i(rd)
        add=registers[a]+b
        if mem_check(add)==0:
            print(f'Invalid memory access at line no. {l_no}')
            return "error"
        if add in mem:
            res=n(mem[add])
        registers[0]=0

    #addi
    elif opcode=="0010011":
        a=s_i(r1)
        c=s_i(rd)
        
        if f3=="000":
            b=s_i(r2)
            res=n(registers[a]+b)
        elif f3=="011":
            b=n_i(r2)
            x=registers[a]
            if x<0:
                x+=2**32
            if b<0:
                b+=2**32
            if x<b:
                res=1
            else:
                res=0
        else:
            print(f'Invalid funct3 value at line no. {l_no}')
            registers[0]=0
            return -1
        registers[0]=0

    #jalr
    elif opcode=="1100111":
        if f3!="000":
            print(f'Invalid funct3 value at line no. {l_no}')
            return -1
        
        a=s_i(r1)
        b=s_i(r2)
        c=s_i(rd)
        newpc=registers[a]+b
        if c!=0:
            registers[c]=n(pc+4)
        registers[0]=0
        return newpc-(newpc%2)

    #sw
    elif opcode=="0100011":
        if f3!="010":
            print(f'Invalid funct3 value at line no. {l_no}')
            return -1
        a=s_i(r1)
        b=s_i(r2)
        c=s_i(rd)
        add=registers[a]+c
        if mem_check(add)==0:
            print(f'Invalid memory access at line no. {l_no}')
            return "error"
        mem[add]=registers[b]
        registers[0]=0
        return pc+4

    #b type instructions
    elif opcode=="1100011":
        a=s_i(r1)
        b=s_i(r2)
        c=s_i(rd)
        if f3=='000' and a==0 and b==0 and c==0:
            return -1
        if f3=='000':
            if registers[a]==registers[b]:
                registers[0]=0
                return pc+c                                             
        elif f3=='001': 
            if registers[a]!=registers[b]:
                registers[0]=0
                return pc+c                                               
        elif f3=='100':
            if registers[a]<registers[b]:
                registers[0]=0
                return pc+c              
        elif f3=='101':
            if registers[a]>=registers[b]:
                registers[0]=0
                return pc+c              
        elif f3=='110':
            x=registers[a]
            y=registers[b]
            if x<0:
                x+=2**32
            if y<0:
                y+=2**32
            if x<y:
                registers[0]=0
                return pc+c    
        elif f3=='111':
            x=registers[a]
            y=registers[b]
            if x<0:
                x+=2**32
            if y<0:
                y+=2**32
            if x>=y:
                registers[0]=0
                return pc+c
        else:
            print(f'Invalid funct3 value at line no. {l_no}')
            registers[0]=0
            return -1
        registers[0]=0
        return pc+4
    
    #lui
    elif opcode=="0110111":
        a=s_i(r1)
        c=s_i(rd)
        if c!=0:
            registers[c]=n(a<<12)
        registers[0]=0
    
    #auipc
    elif opcode=="0010111":
        a=s_i(r1)
        c=s_i(rd)
        if c!=0:
            registers[c]=n(pc+(a<<12))
        registers[0]=0

    #jal
    elif opcode=="1101111":
        a=s_i(r1)
        c=s_i(rd)
        if c!=0:
            registers[c]=n(pc+4)
        registers[0]=0
        return pc+a
    else:
        print(f'Invalid opcode value at line no. {l_no}')
        registers[0]=0
        return -1

    if c!=0:
        registers[c]=n(res)
    return pc+4

def s_i(s):
    e=len(s)
    t=0
    for i in s:
        i=int(i)
        t+=i*(2**(e-1))
        e-=1
    if s[0]=="1":
        t-=2**len(s)
    return t

def n_i(s):
    e=len(s)
    t=0
    for i in s:
        i=int(i)
        t+=i*(2**(e-1))
        e-=1
    return t

def n(x):
    x=x&0xFFFFFFFF
    if x>=2**31:
        x-=2**32
    return x

def mem_check(x):
    if 0x00000100<=x<=0x0000017C or 0x00010000<=x<=0x0001007C:
        if x%4==0:
            return 1
        else:
            return 0
    else:
        return 0
    
def bi(x):
    x=x&0xFFFFFFFF
    a=bin(x)[2:]
    while len(a)<32:
        a="0"+a
    return "0b"+a

def read(pc,registers,mem):
    vals = [bi(pc)]
    for i in registers:
        vals.append(bi(i))
    print(" ".join(vals))

def main(registers):
    with open(sys.argv[1],"r") as f:
        l=f.readlines()
    if len(l)>64:
        print("Program exceeds instruction memory ")
        return -1
    
    pc=0
    mem={}
    for i in range(0x00010000,0x00010080,4):
        mem[i]=0

    for i in range(0x00000100,0x00000180,4):
        mem[i]=0
    for j in range(len(l)):
        l[j]=l[j].strip()
    for i in range(len(l)):
        if len(l[i])!=32:
            print(f'Number of bits not equal to 32 at line no. {i+1}')
            return -1
        for j in l[i]:
            if j!="0" and j!="1":
                print(f'Bits other than 0 and 1 at line no. {i+1}')
                return -1
            
    while True:
        if pc<0 or pc>=len(l)*4:
            print(f'PC out of instruction memory range at line no. {(pc//4)+1}')
            return -1
        if pc%4!=0:
            print(f'Unaligned instruction address at line no. {(pc//4)+1}')
            return -1
        ins=l[pc//4]
        decoded=decode(ins)
        if decoded is None:
            print(f'Invalid instruction encoding at line no. {(pc//4)+1}')
            return -1
        r1,r2,rd,f3,f7=decoded
        l_no=(pc//4)+1
        a=execute(ins,registers,mem,r1,r2,rd,f3,f7,pc,l_no)
        if a=="error":
            return -1
        if a==-1:
            read(pc,registers,mem)
            break
        else:
            read(a,registers,mem)
            pc=a
    for addr in range(0x00010000, 0x00010080, 4):
        print(f"0x{addr:08X}:{bi(mem[addr])}")

outputfile = open(sys.argv[2], "w")
sys.stdout = outputfile

registers=[0]*32
registers[2]=0x0000017C
a=main(registers)

outputfile.close()
