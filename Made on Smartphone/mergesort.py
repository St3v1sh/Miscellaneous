"""
This program was written on my smartphone. This was written just to test
out a python IDE app from the Google Play Store.
"""

def merge_sort(arr):
	c = arr[:]
	merge_sort_rec(c, 0, len(c))
	return c

def merge_sort_rec(arr, l, r):
	if r-l > 1:
		m = (l+r)//2
		merge_sort_rec(arr, l, m)
		merge_sort_rec(arr, m, r)
		merge(arr, l, m, r)

def merge(arr, l, m, r):
	a = arr[l:m]
	b = arr[m:r]
	
	i = 0
	while len(a) > 0 < len(b):
		arr[l+i] = a.pop(0) if a[0] < b[0] else b.pop(0)
		i += 1
	
	arr[l+i:r] = a if len(b) == 0 else b

tests = [
	[],
	[1],
	[2, 1],
	[1, 2, 3, 4, 5],
	[5, 4, 3, 2, 1],
	[2, 1, 4, 3, 5],
	[7, 5, 3, 9, 1, 6, 2, 4, 8]
]

for test in tests:
	print(merge_sort(test))
