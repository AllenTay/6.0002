###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1


def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    toConsider = list(egg_weights)
    if (len(toConsider), target_weight) in memo:
        result = memo[(len(toConsider), target_weight)]

    elif toConsider == [] or target_weight == 0:
        result = (0, ())
    
    elif toConsider[0] > target_weight:
        result = dp_make_weight(toConsider[1:], target_weight, memo) #if adding it is too much, skip to the next

    else:
        nextItem = toConsider[0]
        # Explore left branch, start from 0 becuase it does not run out 
        withnumber, weightwith = dp_make_weight(toConsider[0:], target_weight - nextItem, memo)
        withnumber += nextItem

        #Explore right branch, starts from 1 because you do not take it 
        withoutnumber, weightwithout = dp_make_weight(toConsider[1:], target_weight, memo)

        #Choose better branch
        if withnumber > withoutnumber: # I guess you take the one that makes it heavier 
            result = (withnumber, weightwith + (nextItem, ))
        else:
            result = (withoutnumber, weightwithout)
    memo[(len(toConsider), target_weight)] = result
    return result


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()