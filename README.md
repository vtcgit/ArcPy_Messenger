ArcPy Messenger
============

This is a python class that is intended to be included in Esri python scripts. Our organization found that scripts left running for a weekend failed an hour into processing. This results in a lot of wasted time.

Our solution was to create a python class that sends a message to a user when a script fails (even when the exception isn't caught) or when the creator of the script feels it is necessary.

Currently, this project has had a bare minimum of testing and should not be considered "guaranteed" to work.

One important thing to note: The default exception hook has to be overridden in each new thread.

Future development priorities:

1. Create test cases
2. Create example usages
3. Solve the multi-threading issue
4. Allow usage with any email client (through the use of abstract classes).

If you have any ideas, let us know!

This was developed with the default python compiler included with ArcMap 10.1 (Python 2.7.2). This version of python compiler was chosen because all of our computers are using Python 2.7.2 and it doesn't seem like Esri will be changing the version of Python they use in the near future.

