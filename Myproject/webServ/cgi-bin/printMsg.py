__author__ = 'user'
import sys
def printMsg(name):
    return "Hello "+name
if __name__ == '__main__':
    name=sys.argv[1]
    print(printMsg(name))

