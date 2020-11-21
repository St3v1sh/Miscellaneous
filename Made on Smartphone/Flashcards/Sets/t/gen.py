for i in range(70):
	f = open("f{}.flashcards".format(i), "x")
	f.write("Q%d\n" % i)
	f.write("A%d\n" % i)
	f.close()
