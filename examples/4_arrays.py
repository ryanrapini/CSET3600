import pprint

# with for loop
array = []
for x in range(0,10):
	new = []
	for y in range(0,10):
		new.append(0)
	array.append(new)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(array)

# or even more elegantly with list comprehensions!
array = [[0 for i in range(10)] for j in range(10)]
pp.pprint(array)

for row in array:
	print(" ".join(str(item) for item in row))