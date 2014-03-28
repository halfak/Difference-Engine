"""
A collection of operations necessary to represent a difference.  
"""
Insert = namedtuple("Insert", ['start', 'end'])
Persist   = namedtuple("Persist",   ['start', 'end'])
Remove = namedtuple("Remove", ['start', 'end'])

OPERATIONS = {Insert, Copy, Remove}

"""
    0   |1 |2 |3 |4   |5 |6      |7   |8 |9   |10 |11  |12 |13     |14  |15  |16  |17 |18 |19 |20  |21
=========================================================================================
1. 'This|  |is|  |some|  |content|.   |  |This|   |is  |   |going  |    |away|.   '
2. 'This|  |is|  |some|  |content|.   |  |This|   |is  |   |new    |.   '
3. 'This|  |is|  |new |. |       |This|  |is  |   |some|   |content|.   '

Sequence Matcher."""
[
	{
		"new": [
			Insert(0, 17) # 'This| |is| |some| |content|.  |This| |is| |going| |away|.'
		],
		"removed": []
	},
	{
		"new": [
			Persist(0, 8), # 'This| |is| |some| |content|.'
			Insert(8, 14)    # '|This| |is| |new|.'
		],
		"removed": [
			Remove(9, 17) # 'This| |is| |going| |away|.'
		]
	},
	{
		"new": [
			Insert(0, 7), # 'This| |is| |new|.'
			Persist(0, 15), # 'This|  |is  |   |some|   |content|.'
		],
		"removed": [
			Remove(0, 6) # 'This| |is| |new|.|  '
		]
	}
]
"""
Hierarchical Matcher."""
[
	{
		"new": [
			Insert(0, 8), # 'This| |is| |some| |content|.'
			Insert(8, 9), # '  '
			Insert(9, 21) # 'This| |is| |going| |away|.'
		],
		"removed": []
	},
	{
		"new": [
			Persist(0, 8), # 'This| |is| |some| |content|.'
			Persist(8, 9), # '  '
			Insert(8, 14)    # '|This| |is| |new|.'
		],
		"removed": [
			Remove(9, 17) # 'This| |is| |going| |away|.'
		]
	},
	{
		"new": [
			Persist(9, 14), # 'This| |is| |new|.'
			Persist(8, 9), # ' '
			Persist(0, 8), # 'This|  |is  |   |some|   |content|.'
		],
		"removed": []
	}
]
