from sys import exit
from os import system
from msvcrt import getch
#from os import getcwd

clear = lambda: system('cls')
clear()

# -- Engima Configuration --
#cwd = getcwd()
reflectorSelection = "UKW-B"
rotorsInMachine = [2,4,5]
rotorDisplay = [17,26,16]
plugConfig = "QH EN RM TL YS UI OK PC DV FG"

# -- Engima Configuration --

class hitler():

	ref = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	rotor = ["PEZUOHXSCVFMTBGLRINQJWAYDK", "ZOUESYDKFWPCIQXHMVBLGNJRAT", "EHRVXGAOBQUSIMZFLYNWKTPDJC", "IMETCGFRAYSQBZXWLHKDVUPOJN", "QWERTZUIOASDFGHJKPYXCVBNML"]
	#reflectorB = "VKWRGIETFZBUSPQNODMHLACYXJ"
	reflectorB = {'A': 'V', 'B': 'K', 'C': 'W', 'D': 'R', 'E': 'G', 'F': 'I', 'G': 'E', 'H': 'T', 'I': 'F', 'J': 'Z', 'K': 'B', 'L': 'U', 'M': 'S', 'N': 'P', 'O': 'Q', 'P': 'N', 'Q': 'O', 'R': 'D', 'S': 'M', 'T': 'H', 'U': 'L', 'V': 'A', 'W': 'C', 'X': 'Y', 'Y': 'X', 'Z': 'J'}


	def __init__(self, reflectorSelection, rotorsInMachine, rotorDisplay, plugConfig):
		
		self.reflectorSelection = reflectorSelection
		self.rotorsInMachine = rotorsInMachine
		self.rotorDisplay = rotorDisplay
		self.plugConfig = plugConfig
			
	def routeToPlug(self,character):
		if character in self.plugConfig:
			index = self.plugConfig.index(character)
			if index == (len(self.plugConfig) - 1) or self.plugConfig[index + 1] == " ":
				return self.plugConfig[index - 1]
			else:
				return self.plugConfig[index + 1]
		else:
			return character
		
	def reflector(self,character):
		if self.reflectorSelection == "UKW-B":
			reflectorWiring = self.reflectorB
		return reflectorWiring[character]

	def assignRotors(self):
		A = self.rotorsInMachine[2]
		B = self.rotorsInMachine[1]
		C = self.rotorsInMachine[0]
		rotorA = self.rotor[A-1]
		rotorB = self.rotor[B-1]
		rotorC = self.rotor[C-1]
		return rotorC, rotorB, rotorA

	def rotateRotors(self):
		self.rotorDisplay[2] += 1
		if self.rotorDisplay[2] > 26:
			self.rotorDisplay[2] -= 26
			self.rotorDisplay[1] += 1
			if self.rotorDisplay[1] > 26:
				self.rotorDisplay[1] -= 26
				self.rotorDisplay[0] += 1
				if self.rotorDisplay[0] > 26:
					self.rotorDisplay[0] -= 26

	def passRotor(self, rotor, character, mode):
		if rotor == rotorA:
			count = self.rotorDisplay[2]
		elif rotor == rotorB:
			count = self.rotorDisplay[1]
		else:
			count = self.rotorDisplay[0]
		if mode == "FRWD":
			count = (count + self.ref.index(character)) % 26
			return rotor[count-1]
		else:
			count = rotor.index(character) - count + 1
			if count < 0:
				count +=26
			return self.ref[count]

	def rotors(self,character):
		self.rotateRotors()
		char = [""]*10
		char[0] = character
		char[1] = self.routeToPlug(char[0])
		char[2] = self.passRotor(rotorA, char[1],"FRWD")
		char[3] = self.passRotor(rotorB, char[2],"FRWD")
		char[4] = self.passRotor(rotorC, char[3],"FRWD")
		char[5] = self.reflector(char[4])
		char[6] = self.passRotor(rotorC, char[5],"BKWD")
		char[7] = self.passRotor(rotorB, char[6],"BKWD")
		char[8] = self.passRotor(rotorA, char[7],"BKWD")
		char[9] = self.routeToPlug(char[8])
		return char[9]

## --- Global Functions for Enigma UI ---
# --- Initiating Enigma ---

enigma = hitler(reflectorSelection,rotorsInMachine,rotorDisplay,plugConfig)

# --- Setting up the Rotors ---
rotorC, rotorB, rotorA = enigma.assignRotors()
# --- Required variables for Mode Level Operations ---
global inChars, outChars
inChars = ""
outChars = ""
# --- Display Enigma ---
def displayEnigma(inCh, outCh, inChars, outChars, enigma = enigma):
	clear()
	print("			__---*** ENIGMA SIMULATOR ***---__\n\n")
	print(f" Rotors in Action: 	{enigma.rotorsInMachine[0]} 	{enigma.rotorsInMachine[1]} 	{enigma.rotorsInMachine[2]}\n")
	print(f"    Rotor Display: 	{enigma.rotorDisplay[0]} 	{enigma.rotorDisplay[1]} 	{enigma.rotorDisplay[2]}")
	print(f"\n\n Last Character Entered: 	{inCh} 	Last Enigma's Output: 	{outCh}")
	print(f"\n All Input Characters: {inChars}")
	print(f"\n      Enigma's Output: {outChars}")
	print("\n\n 	Please Enter an Alphabet: 	")

def sentenceMode(enigma = enigma):
	# VAYAZOPKCXDHHO <---> SENDINTHETANKS
	clear()
	inputString = input("\n\n Enter your Message:  ")
	inputString = inputString.upper()
	if inputString == "EXIT":
		exit()
	elif inputString == "START":
		modeMenu()
	inputString = inputString.replace(" ","")
	finalString = ""
	for each in inputString:
		if each.isalpha():
			finalString = finalString + each
	print("Final String Typed into Enigma:  " + finalString)
	outputString = ""
	for each in finalString:
		returnChar = enigma.rotors(each)
		outputString = outputString + returnChar
	print("Enigma's Output:  " + outputString)
	input()
	sentenceMode()

# --- Creating Machine Modes ---
def charMode(inChars, outChars, enigma = enigma):
	inCh = getch()
	inCh = inCh.decode("utf-8")
	if inCh.isalpha():
		inCh = inCh.upper()
		outCh = enigma.rotors(inCh)
		inChars = inChars + inCh
		outChars = outChars + outCh
		displayEnigma(inCh, outCh, inChars, outChars)
	else:
		clear()
		if inCh == '$':
			exit()
		elif inCh == '#':
			modeMenu()
		elif inCh == "%":
			inCh, outCh, inChars, outChars = "","","",""
			displayEnigma(inCh, outCh, inChars, outChars)
		else:
			print("\n\n\n 		Please Enter Alphabets Only..!!!")
			input()
			inCh = ""
			outCh = ""
			displayEnigma(inCh, outCh, inChars, outChars)
	charMode(inChars, outChars)
	
def modeMenu():
	clear()
	print("\n\n 				___~~~***- ENIGMA -***~~~___\n\n")
	print("\n 				[1] . Character Mode")
	print("\n 				[2] . Sentence Mode")
	print("\n 				[3] . Re-config Enigma (-: Work in Progress :-)")
	print("\n 				[4] . Exit")
	mode = getch()
	mode = mode.decode("utf-8")
	if mode == "1":
		inCh = ""
		outCh = ""
		displayEnigma(inCh, outCh, inChars, outChars)
		charMode(inChars, outChars)
	elif mode == "2":
		sentenceMode()
	elif mode == "4":
		exit()
	else:
		clear()
		print("\n\n\n 			Please select Options 1 or 2 or 4")
		input()
		modeMenu()

# --- Starting Windows ---
modeMenu()