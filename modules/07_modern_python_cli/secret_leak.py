import sys
import time

def login(user_name, password):
    print("You're in")


def main():
    user_name = sys.argv[1]
    password = sys.argv[2]
    time.sleep(10)
    login(user_name, password)

if __name__ == "__main__":
    main()