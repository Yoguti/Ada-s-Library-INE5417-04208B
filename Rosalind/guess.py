import random


def main():
    print('guess the number i\'m thinking of (1-10): ')
    guess = int(input())
    while True:
        if isinstance(guess, int):
            break
        else:
            print('value must be an integer')
    
    while True:
        randint = random.randint(1, 10)

        if (randint == guess):
            print('good job!')
            break
        else:
            print('try again!\n')
            guess = int(input())

main()
