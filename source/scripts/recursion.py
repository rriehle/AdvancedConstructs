# Recursion tutorial
# rriehle 2018

# Divide & conquer.
# Need a termination condition.

name = "enola"

# How in python do we get the last element of a sequence?
name[-1]

# How do we get everything but the last element?
name[:-1]

# What if we were to add these things together?
name[-1] + name[:-1]

# So what we really want is to reverse the second portion
# before concatening, something like this:
name[-1] + reverse(name[:-1])

# But since reverse isn't defined, let's define it.
def reverse(word):
    return word[-1] + reverse(word[:-1])

reverse(name)

# Hm. This looks promising, but what went wrong?
def reverse(word):
    print("word is {}, word[-1] is {}, word[:-1] is {}".format(
       word, word[-1], word[:-1]
    ))
    return word[-1] + reverse(word[:-1])

reverse(name)

# No termination condition.  Let's add one.
def reverse(word):
    if word == '': return ''
    print("word is {}, word[-1] is {}, word[:-1] is {}".format(
       word, word[-1], word[:-1]
    ))
    return word[-1] + reverse(word[:-1])

reverse(name)

# Let's clean it up a bit.
def reverse(word):
    if word == '':
        return ''
    return word[-1] + reverse(word[:-1])

reverse(name)

# Perhaps flipping conditional looks a little better.
def reverse(word):
    if word:
        return word[-1] + reverse(word[:-1])
    return ''

reverse(name)

# The stack is not infinite.
