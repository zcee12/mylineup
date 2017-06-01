from twisted.internet import reactor

print "Running..."


def f(s):
    print "this will run 3.5 seconds after it was scheduled: %s" % s
    reactor.callLater(3.5, f, "hello, world")

reactor.run()
