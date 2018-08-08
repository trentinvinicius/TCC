from createSituations import call

situations = []
situations.append('0001')
for i in range(6):
	situations.append('10'+str(i)+'0')
	situations.append('11'+str(i)+'0')
	situations.append('20'+str(i)+'0')
	situations.append('21'+str(i)+'0')
situations = situations[::-1]
for s in situations:
	for i in range(2):
		name = s + '_' + str(i+4)
		print name
		call(s, name, False, 20)
