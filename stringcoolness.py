import math 
import string
import random
from collections import Counter
import os

# Text colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RED_BACK = "\033[41m"
GREEN_BACK = "\033[42m"
YELLOW_BACK = "\033[43m"
BLUE_BACK = "\033[44m"
MAGENTA_BACK = "\033[45m"
CYAN_BACK = "\033[46m"

COLORS = [YELLOW, GREEN, RED, BLUE, CYAN, MAGENTA, 
          YELLOW_BACK, GREEN_BACK, RED_BACK, BLUE_BACK, 
          CYAN_BACK, MAGENTA_BACK]

retry = 'y'
while retry != 'n':

    LENGTH = int(input("LENGTH: ") or last_length)
    last_length = LENGTH

    for i in range(20):
        random_string = ''.join(random.choices(string.ascii_lowercase, k=LENGTH))

        crs = Counter(random_string).most_common()

        repeated_chars = []

        rawpoints = 0

        for elem in crs:
            if elem[1]==1:
                break
            else:
                if elem[0] == 'm':
                    repeated_chars.insert(0, elem)
                else:
                    repeated_chars.append(elem)

        blockbonus = 1
        accrue = 0
        for char in range(LENGTH):
            if char == 0:
                pass
            elif random_string[char] == random_string[char - 1]:
                accrue += 1
            else:
                accrue = 0
            
            blockbonus += (accrue / LENGTH)

        counthits = 0
        for elem in repeated_chars:
            colored_string = random_string.replace(str(elem[0]), str(COLORS[min(elem[1]-2,len(COLORS)-1)] + str(elem[0]) + RESET))
            random_string = colored_string
            counthits += elem[1]
            rawpoints += elem[1]**4
            

        percent_unique = (LENGTH-counthits)/LENGTH
        bellcurve = abs(percent_unique-0.5)
        points = (rawpoints ** (1 + bellcurve)) ** blockbonus

        print(f"{random_string}     {percent_unique:<8.2%}  {rawpoints:<8.2f}  {blockbonus:<10.2f}  {bellcurve:<10.2f}  {points:>15,.2f}")
    
    retry = input("AGAIN?: ")
    os.system('cls')