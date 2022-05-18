import configparser

def start():
    config = configparser.ConfigParser()
    config.read("confix.txt")

if __name__ == "__main__":
    start()