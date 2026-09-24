
import random

number = random.randint(1, 100)
attempts = 0

print("Я загадал число от 1 до 100. Попробуй угадать!")

while True:
    guess = int(input("Твой вариант: "))
    attempts += 1

    if guess < number:
        print("Моё число больше!")
    elif guess > number:
        print("Моё число меньше!")
    else:
        print(f"🎉 Ты угадал! Попыток: {attempts}")
        break

