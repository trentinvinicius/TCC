import pickle

user = {"hitCrosswalkSignalGreen"	:		0.0333,      \
		"hitCrosswalkSignalRed"		:		0.0333,	    \
		"hitOutsideCrosswalk"		:		0.0333,		\
		"MaleKid" 	 				:		1636,   \
		"MaleAdult"					:		1636,   \
		"MaleElderly"				:		1636,   \
		"FemaleKid"					:		1636,   \
		"FemaleAdult"   			:		1636,   \
		"FemaleElderly"				:		1636,   \
		"mainCarSinglePassenger"	:		2623,  \
		"mainCarDoublePassenger"	:		5448,  \
		"otherCarPassengers"		:		928,   \
		"animal"					:		182,      \
		}
userPercent = [0.1, 0.0, 0.1, 0.0, 0.1, 0.0, 0.1, 0.0, 0.1, 0.0, 0.1, 0.0, 0.2, 0.2]

preferences = {'userPreferences': user, 'userVector': userPercent}

with open('userPreferences/newCombination1', 'wb') as outputfile:
	pickle.dump(preferences, outputfile)