print(sum(map({"A X":4+3j,"B X":1+1j,"C X":7+2j,"A Y":8+4j,"B Y":5+5j,"C Y":2+6j,"A Z":3+8j,"B Z":9+9j,"C Z":6+7j}.get,open("d").read().splitlines())))