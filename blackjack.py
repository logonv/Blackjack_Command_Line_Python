import random

"""

Objects for game

"""

#card class
class card:
    
    def __init__(self, suit, value):
        self.suit=suit
        self.value=value
        
    def __str__(self):
        return "The card is a " + str(self.value)+" of " + str(self.suit)

#deck of cards class
class deck:
    
    def __init__(self):
        
        self.deck= []
        self.num=0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.num >= len(self.deck):
            self.num=0
            raise StopIteration
        else:
            self.num += 1
            return self.deck[self.num-1]
       
    
    #builds a deck    
    def build(self):
        values=[]
        values.append("Ace")
        for a in range(2,11):
            values.append(a)
        values.append("Jack")
        values.append("Queen")
        values.append("King")
        for suit in ["Spades","Diamonds","Clubs","Hearts"]:
            for val in values:
                self.deck.append(card(suit,val))
    
    def __str__(self):
        returnstring=[]
        for i in range(0,len(self.deck)):
             returnstring.append(str(self.deck[i]))
        return str(returnstring)

    def __len__(self):
        return len(self.deck)

    #deals a card
    def deal(self):
        return self.deck.pop()

    #shuffles the deck
    def shuffle(self):
        return random.shuffle(self.deck)

    #rebuilds and shuffles the deck
    def reset(self):
        self.deck = []
        self.build()
        self.shuffle()

    def add(self,cardtoadd):
        
        self.deck.append(cardtoadd)

#player class
class player:
    
    def __init__(self, name, chips=0):
        self.name=name
        self.chips=chips
    
    #returns the bet ammount
    def bet(self,amount):
        while amount>self.chips:
            print("Not possible, select another amount")
            amount=int(input())
        if amount<=self.chips:
            self.chips=self.chips-amount
            print("You have bet " + str(amount))
        return amount
    
    #increases chip amount if win
    def win(self,winnings):
        self.chips=self.chips+winnings
        print("You have won " + str(winnings))
        
    #increase chip amount if buying more chips    
    def buyin(self,buyin):
        self.chips=self.chips+buyin
        print("You have bought " + str(buyin) +" more chips")


def showhand(hand):
    returnstring=""
    for card in hand:
        returnstring+=str(card)+"."
    return returnstring

def showdealerhand(hand):
    #returnstring=" "
    cardlist=[]
    for card in hand:
        cardlist.append(card)
    return str(cardlist[0])+". Other card is hidden"

def totalhand(hand):
    total=0
    for card in hand:
        val=card.value
        if card.value in ["King", "Queen", "Jack",]:
            val=10
        if card.value in ["Ace"]:
            val=11
        total+=val
    if total>21:
        vallist=[]
        for card in hand:
            vallist.append(card.value)
        if "Ace" in vallist:
            total=total-10
    return total

def checkifbust(hand):
    return totalhand(hand)>21 
    
"""
Initialises the dealer, the player and deck

"""
carddeck=deck()
carddeck.reset()
dealer=player("Dealer",0)
username=input("What is the player's name? \n")
while True:
    try:
        starting_chips=int(input("How many chips do you want to start with? \n"))
        print("The number of chips you will start with is "+ str(starting_chips)+".\n The game will start now.")
    except:
        print("That is not an integer, please input again")
        continue
    else:
        break

user=player(username,starting_chips)
playerhasbet=False
playerhaschips=True

while True:
    if playerhaschips==False:
        print("You are bust. \n Game over")
        while True:
            pass
        
    while playerhaschips==True:
        while playerhasbet==False:
            print("Player has "+str(user.chips)+" chips.\n")
            if user.chips==0:
                playerhaschips=False
                break
            try:
                userbet=user.bet(int(input("How much do you want to bet?\n")))
            except:
                print("That is not an integer, please input again")
                continue
            print(username+" has bet "+str(userbet)+" chips.")
            playerhasbet=True
            break
        while playerhasbet==True:
            print("player has bet")
            dealerhand=deck()
            playerhand=deck()
            dealerhand.add(carddeck.deal())
            playerhand.add(carddeck.deal())
            dealerhand.add(carddeck.deal())
            playerhand.add(carddeck.deal())            
            print("The dealer's hand is:")
            print(showdealerhand(dealerhand))            
            print(user.name+"'s hand is:")
            print(showhand(playerhand))
            hit=input("Would you like to get another card? Yes or no \n")
            hit=hit.strip()
            
            while hit[0].lower() not in ["y","n"]:
                print("Please answer yes or no")
                hit=input("Would you like to get another card? Yes or no \n")
                hit=hit.strip()
            
            while hit[0].lower()=="y":
                print("new card")
                playerhand.add(carddeck.deal())
                print("Your hand is now:\n"+showhand(playerhand))
                if checkifbust(playerhand)==True:
                    print("You are bust \nEnd of hand. \nYou have lost "+str(userbet)+" chips.\n")
                    playerhasbet=False
                    dealerplays=False
                    break
                hit=input("Would you like to get another card? Yes or no \n")
                hit=hit.strip()
                while hit[0].lower() not in ["y","n"]:
                    print("Please answer yes or no")
                    hit=input("Would you like to get another card? Yes or no \n")
                    hit=hit.strip()
            
            if hit[0].lower()=="n":
                print("no new card\n")
                print("Your hand is now:\n"+showhand(playerhand))
                print("Your total is " + str(totalhand(playerhand)))
                dealerplays=True
                
            while dealerplays==True:
                print("It is now the dealer's turn. \nHis hand is:\n"+showhand(dealerhand))

                dealertotal=totalhand(dealerhand)
                while dealertotal<totalhand(playerhand):
                    print("Dealer has "+str(dealertotal)+".\n" +"He will add a card.")
                    dealerhand.add(carddeck.deal())
                    print("His hand is:\n"+showhand(dealerhand))
                    if checkifbust(dealerhand)==True:
                        print("Dealer has bust. \nEnd of hand. \nPlayer has won "+str(userbet)+" chips. \n")
                        user.chips=user.chips+2*userbet
                        playerhasbet=False
                        dealerplays=False
                        break
                    dealertotal=totalhand(dealerhand)

                
                if dealertotal==totalhand(playerhand):
                    print("Dealer has "+str(dealertotal)+".\n" )
                    print("This is a split pot. Player does not lose anything")
                    user.chips=user.chips+userbet
                    playerhasbet=False
                    dealerplays=False
                elif dealertotal>totalhand(playerhand):
                    print("Dealer has "+str(dealertotal)+".\n" )
                    print("This is more than the player who has "+ str(totalhand(playerhand))+".\n ")
                    print("Player loses "+ str(userbet)+"chips.")
                    playerhasbet=False
                    dealerplays=False
                            
