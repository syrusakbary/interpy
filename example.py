# coding: interpy

# Vars
package = "Interpy"
print "Enjoy #{package}!"

# Complex data inside interpolation
caller = lambda: "Caller called!"
print """
The interpolation tag is #{"#{}"}.
And have any Python expression inside
	- #{caller()}
	- #{{'say':'Hello World!'}['say']}
	- #{"Happy" if package else "Sad"}
"""
