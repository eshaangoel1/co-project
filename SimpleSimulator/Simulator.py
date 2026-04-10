
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
