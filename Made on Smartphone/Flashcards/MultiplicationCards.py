f = open("Sets/multiplication.flashcards", "x")

for i in range(1, 100):
	for j in range(i, 100):
		f.write("{} * {}\n".format(i, j))
		f.write("{}\n".format(i*j))

f.close()