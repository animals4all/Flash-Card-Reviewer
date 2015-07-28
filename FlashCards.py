#! python3

import sys, os

'''
Flash card file format:

(All cards that don't need to be reviewed above divider line)
<card front>:<card back>
---
(All cards that need to be reviewed below divider line)
<card front>:<card back>
'''

def help(funcName):
	'''Print information about how to use the program while in the current function'''
	print(str(os.path.basename(__file__)))
	print("")
	print("Enter a command at the prompt.")
	print("")
	print("Command list:")
	if funcName == "main":
		print("""

review <flashcard deck name> - Review a deck of flashcards. You must enter the name of the deck after the 'review' command
Example: 'review flashcards.txt'
Example: 'review flashcards.txt'

help - Get a list of commands that can currently be used

quit - Exit the program""")
	elif funcName == "cardReview":
		print("""
		
ENTER key - Press this key after each flashcard to move to the next flashcard

add <flashcard name/'all'> - Transfer a card/cards from the cards in the flashcard deck that aren't being reviewed to the cards in the flashcard deck that are being reviewed
- Put the name of the flashcard that you want to be added after the command, or
- Put the keyword 'all' after the command to add all the cards
Example: 'add 7 ocean names'
Example: 'add all'

remove <flashcard name (optional)> - Transfer a card from the cards in the flashcard deck that are being reviewed to the cards in the flashcard deck that aren't being reviewed
- Put the name of the flashcard that you want to be removed after the command
- If no flashcard name is given, the current card will be removed

help - Get a list of commands that can currently be used

quit - Exit the program""")

def cardInDeck(cardName, deck):
	'''Return True if the card name matches the front of any of the cards in the deck, return False
	otherwise'''
	for cardFront in deck.keys():
		# deck = dictionary, keys = card fronts
		if cardFront == cardName:
			return True, cardFront, deck[cardFront]
	return False, None, None


def cardReview(cardDecks, fileName):
	reviewedDeck = cardDecks[0]
	unreviewedDeck = cardDecks[1]

	# Make dicts of cards to be added to or removed from the deck of unreviewed cards
	cardsToAdd = {}
	cardsToRemove = {}

	for cardFront, cardBack in unreviewedDeck.items():
		# deck = dict, dict keys = card fronts, dict values = card backs
		print("")
		print(cardFront)
		print("")
		input("(Press ENTER to see the answer.)")
		print("")
		print(cardBack)

		while True:
			print("")
			command = input("> ")
			command = command.split()

			if command == []:
				# Command is blank, continue on to the next card
				break

			elif command[0].lower() in ("a", "add"):
				# Transfer card(s) from 'reviewed' deck to 'unreviewed' deck

				# Add format is 'add' command plus the name of the card. Because the card name can be 
				# more than one word long, the rest of the command needs to be rejoined together
				command.remove(command[0])
				command = " ".join(command)
				cardName = command.strip()

				if cardName == "all":
					# Put all cards in 'reviewed' deck into 'unreviewed' deck
					for cardFront, cardBack in reviewedDeck.items():
						if cardFront not in cardsToAdd:
							cardsToAdd[cardFront] = cardBack
					print("Cards will be transferred to 'unreviewed' deck on next iteration.")
				elif cardName == "":
					# Card name not given, give error
					print("Please enter the name of the card you want to add after the 'add' command.")
				else:
					# Card name given, add named card
					isCardInDeck, cardFront, cardBack = cardInDeck(cardName, reviewedDeck)
					if isCardInDeck and cardFront not in cardsToAdd:
						cardsToAdd[cardFront] = cardBack
						print("Card will be transferred to 'unreviewed' deck on next iteration.")
					else:
						print("That card could not be found.")

			elif command[0].lower() in ("r", "remove"):
				# Transfer card from 'unreviewed' deck to 'reviewed' deck

				# Remove format is 'remove' command plus the name of the card. Because the card name
				# can be more than one word long, the rest of the command needs to be rejoined together
				command.remove(command[0])
				command = " ".join(command)
				cardName = command.strip()

				if cardName == "":
					# Card name not given, remove current card
					if cardFront not in cardsToRemove:
						cardsToRemove[cardFront] = cardBack
						print("Card will be transferred to 'reviewed' deck on next iteration.")
					else:
						print("That card has already been removed.")
				else:
					# Card name given, remove named card
					isCardInDeck, cardFront, cardBack = cardInDeck(cardName, unreviewedDeck)
					if isCardInDeck and cardFront not in cardsToRemove:
						cardsToRemove[cardFront] = cardBack
						print("Card will be transferred to 'reviewed' deck on next iteration.")
					else:
						print("That card could not be found.")

			elif command[0].lower() in ("q", "quit"):
				ans = input("Are you sure you want to quit? Any changes you made to the deck won't be saved! (y/n): ")
				if ans.strip().lower() in ("y", "yes"):
					sys.exit()
			elif command[0].lower() in ("h", "help"):
				help("cardReview")
			else:
				print("""'%s' is not a recognized command. To view a list of commands, enter 'h' or 'help', or just press the 'Enter' key to continue reviewing the cards.""" % (command[0]))

	endMsg = "Finished reviewing " + str(len(unreviewedDeck)) + " flashcards. Go through this deck again? (y/n): "

	reviewedDeck, unreviewedDeck = makeChangesToDecks(cardsToAdd, cardsToRemove, reviewedDeck, unreviewedDeck)
	writeChangesToFile(fileName, reviewedDeck, unreviewedDeck)

	# Check if the user wants to review the current deck again
	print("")
	return input(endMsg).strip().lower()


def makeChangesToDecks(cardsToAdd, cardsToRemove, reviewedDeck, unreviewedDeck):
	# Make the changes to the decks
	for cardFront, cardBack in cardsToAdd.items():
		# Transfer cards from reviewed deck to unreviewed deck
		del reviewedDeck[cardFront]
		unreviewedDeck[cardFront] = cardBack
	for cardFront, cardBack in cardsToRemove.items():
		# Transfer cards from unreviewed deck to reviewed deck
		del unreviewedDeck[cardFront]
		reviewedDeck[cardFront] = cardBack

	return reviewedDeck, unreviewedDeck

def writeChangesToFile(fileName, reviewedDeck, unreviewedDeck):
	'''Write the changes made to the cards in the reviewed and unreviewed parts of the flashcard
	deck to flashcard's file'''

	# Create a list containing all the lines to be put in the file
	fileLines = []
	for cardFront, cardBack in reviewedDeck.items():
		fileLines.append(cardFront + ":" + cardBack + "\n")
	fileLines.append("---\n")
	for cardFront, cardBack in unreviewedDeck.items():
		fileLines.append(cardFront + ":" + cardBack + "\n")

	fileObj = open(fileName, "w")
	fileObj.writelines(fileLines)
	fileObj.close()


def splitIntoCardDecks(fileObj):
	'''Split the given a file into two dictionaries with the front of the card as the key and the
	back of the card as the value'''

	# Two types of cards, reviewed and unreviewed, are seperated in file by divider line. cardDecks
	# contains the decks for both types of cards
	cardDecks = []
	deckContents = fileObj.read().split("---\n")

	for cardType in deckContents:
		cards = cardType.split("\n")
		for card in reversed(cards):
			if card == "":
				cards.remove(card)
		cardDeck = {}
		for card in cards:
			# Each card in the file is in the format <front of card>:<back of card>
			cardFront, cardBack = card.split(":")[0], card.split(":")[1]
			cardDeck[cardFront] = cardBack
		cardDecks.append(cardDeck)

	return cardDecks


def main():
	command = ""

	while True:
		print("")
		command = input("> ")
		command = command.split()

		if command == []:
			# No command was given
			continue

		elif command[0].lower() in ("r", "review"):
			# Review the given deck
			command.remove(command[0])
			command = " ".join(command)
			fileName = command.strip()
			if fileName == "":
				print("Please enter the name of the file.")
			elif os.path.exists(fileName):
				fileObj = open(fileName, "r")
				cardDecks = splitIntoCardDecks(fileObj)
				fileObj.close()
				reviewAgain = "y"
				while reviewAgain in ("y", "yes"):
					print("")
					print("Reviewing %s" % fileName)
					print("")
					reviewAgain = cardReview(cardDecks, fileName)
			else:
				print("File '%s' not found." % (fileName))

		elif command[0].lower() in ("h", "help"):
			help("main")
		elif command[0].lower() in ("q", "quit"):
			sys.exit()
		else:
			print("""'%s' is not a recognized command. To view a list of commands, enter 'h' or 'help'.""" % (command[0]))


if __name__ == "__main__":
	main()
