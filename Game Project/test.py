import time

limit = 5 # you can set out the limit here.

def leaderboard():
    scores = [] 
    print ("\n") 
    print ("⬇ Check out the leaderboard ⬇")
    #LEADERBOARD SECTION 
    for line in open('H_Highscore.txt', 'r'):
        name, score = line.split(",")
        score = int(score) # clean and convert to int to order the scores using sort()
        scores.append((score, name))
        
    sorted_scores = sorted(scores, reverse = True) # this will sort the scores based on the first position of the tuples
    
    for register in sorted_scores[:limit]:
        # I will use string formating, take a look at it, it is really usefull.
        text = f"%s: %s pts" % (register[1], register[0])
        print(text)

user = str(input("Enter a name: "))
file = open("H_Highscore.txt", "a")
score = str(input("enter you score: "))
# file.write("\n")
file.write(user)
file.write(",")
file.write(str(score)) # (int(x)) can not be written
file.write("\n")
# file.write("\n")
file.close()
time.sleep(0.5)
leaderboard() 

