import random
import os
import sys

def main():
    string, cipherPad, operationType = readData()
    new_str = OTCP(string, cipherPad, operationType)
    print(new_str)

    # more thorough encoding
    str_5 = new_str.replace(' ', '').upper()
    # split string into 5 long chunks
    str_chunks = [str_5[i:i+5] for i in range(0, len(str_5), 5)]
    # combine list into string
    str_5 = ' '.join(str_chunks)
    print(str_5)

def OTCP(string, cipherPad, operationType):
    new_str = ''

    # make an add operation into a subtraction operation later in the code, this switches the operation from encoding to decoding
    if operationType == 'e':
        c = 1
    elif operationType == 'd':
        c = -1

    i = 0
    j = 0
    while i < len(string):
        str_ch = string[i]
        # go to the jth character of the jth line, if the jth character doesn't exist go to the modulo
        ciph_ch = cipherPad[j][j % 26]

        # change character to upper or lowercase depending on original string, do nothing if charcter isn't a letter
        if str_ch.isupper():
            # add plaintext char values, mod 26, then convert back to char
            new_ch = indexToChar((charToIndex(str_ch.upper()) + c * charToIndex(ciph_ch)) % 26)
            new_ch = new_ch.upper()
        elif str_ch.islower():
            new_ch = indexToChar((charToIndex(str_ch.upper()) + c * charToIndex(ciph_ch)) % 26)
            new_ch = new_ch.lower()
        else:
            new_ch = str_ch
            # neat way to say, don't encode things that aren't letters
            j -= 1
            
        
        i += 1
        j += 1

        new_str = new_str + new_ch
    
    return new_str

def charToIndex(char):
    return ord(char.upper()) - ord('A')

def indexToChar(num):
    return chr(num + ord('a'))

def readData():
    # get command line argument
    filename = sys.argv[1]

    inputType = input('Are you encoding / decoding from a string or a file (s or f)? ')
    if inputType == 's':
        string = input('String: ')
    elif inputType == 'f':
        fileName = input('Filename (with extention): ')
        with open(fileName, 'r') as file:  
            string = file.read()
    else:
        print('Invalid choice, please specify either a string or file type')
        return
    
    # make sure we're not overwriting anything important accidentally
    if '.txt' not in filename:
        print('Invalid file')
        return

    # If file is empty
    if os.stat(filename).st_size == 0:
        num_lines = int(input('Generating cipherpad, how many lines do you need?: '))
        cipherPad = generatePad(num_lines, filename)
        
    else:
        with open(filename, 'r') as file:  
            # remove newline characters from cipherPad
            cipherPad = [line.strip('\n') for line in file]
    
    operationType = input('Encrypt or decrypt ( e or d ): ')

    if operationType not in ['e', 'd'] :
        print('Invalid operation type.')
        return

    return (string, cipherPad, operationType)

def generatePad(num_lines, filename = None):
    # generate list of alphabetical chars
    alphabet = [chr(ord('A') + i) for i in range(26)]
    cipherPad = [] 

    with open(filename, "w") as f:
        for i in range(num_lines):
            # shuffle alphabet, and store it in both an array and a textfile
            random.shuffle(alphabet)
            cipherPad.append(''.join(alphabet))
            # write cipher to file
            f.write(''.join(alphabet) + "\n")
    
    return cipherPad

main()
