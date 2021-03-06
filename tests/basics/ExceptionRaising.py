#     Copyright 2013, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Python tests originally created or extracted from other peoples work. The
#     parts were too small to be protected.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
import sys

print "Raising an exception type in a function:"

def raiseExceptionClass():
    raise ValueError

try:
    raiseExceptionClass()
except Exception, e:
    print "Caught exception", e, repr(e), type(e)

print "After catching, sys.exc_info is this", sys.exc_info()
print "*" * 20

print "Raising an exception instance in a function:"

def raiseExceptionInstance():
    raise ValueError( "hallo" )

try:
    raiseExceptionInstance()
except Exception, f:
    print "Caught exception", f, repr(f), type(f)

print "After catching, sys.exc_info is this", sys.exc_info()
print "*" * 20

print "Raising an exception, then catch it to re-raise it:"

def raiseExceptionAndReraise():
    try:
        x = 0
        y = x / x
    except:
        raise

try:
    raiseExceptionAndReraise()
except:
    print "Catched reraised"

print "After catching, sys.exc_info is this", sys.exc_info()
print "*" * 20

print "Access an undefined global variable in a function:"

def raiseNonGlobalError():
    return undefined_value

try:
   raiseNonGlobalError()
except:
   print "NameError caught"

print "After catching, sys.exc_info is this", sys.exc_info()
print "*" * 20

print "Raise a new style class as an exception, should be rejected:"

def raiseIllegalError():
    class X( object ):
        pass

    raise X()

try:
    raiseIllegalError()
except TypeError, E:
    print "New style class exception correctly rejected:", E
except:
    print sys.exc_info()
    assert False, "Error, new style class exception was not rejected"

print "After catching, sys.exc_info is this", sys.exc_info()
print "*" * 20

print "Raise an old-style class, version dependent outcome:"

class ClassicClassException:
    pass

def raiseCustomError():
    raise ClassicClassException()

try:
    try:
        raiseCustomError()
    except ClassicClassException:
        print "Caught classic class exception"
    except:
        print sys.exc_info()

        assert False, "Error, old style class exception was not caught"
except TypeError, e:
    print "Python3 hates to even try and catch classic classes", e
else:
    print "Classic exception catching was considered fine."

print "After catching, sys.exc_info is this", sys.exc_info()
print "*" * 20

print "Checking tracebacks:"

def checkTraceback():
    import sys, traceback

    try:
        raise "me"
    except:
        assert sys.exc_info()[0] is not None
        assert sys.exc_info()[1] is not None
        assert sys.exc_info()[2] is not None

        print "Check traceback:"

        traceback.print_tb( sys.exc_info()[2], file = sys.stdout )

        print "End of traceback"

        print "Type is", sys.exc_info()[0]
        print "Value is", sys.exc_info()[1]

checkTraceback()

print "*" * 20

print "Check lazy exception creation:"

def checkExceptionConversion():
    try:
        raise Exception( "some string")
    except Exception, err:
        print "Catched raised object", err, type( err )

    try:
        raise Exception, "some string"
    except Exception, err:
        print "Catched raised type, value pair", err, type( err )


checkExceptionConversion()
print "*" * 20

print "Check exc_info scope:"

def checkExcInfoScope():
    try:
        raise ValueError
    except:
        assert sys.exc_info()[0] is not None
        assert sys.exc_info()[1] is not None
        assert sys.exc_info()[2] is not None

    if sys.version_info[0] < 3:
        print "Exc_info remains visible after exception handler for Python2"

        assert sys.exc_info()[0] is not None
        assert sys.exc_info()[1] is not None
        assert sys.exc_info()[2] is not None
    else:
        print "Exc_info is clear after exception handler for Python3"

        assert sys.exc_info()[0] is None
        assert sys.exc_info()[1] is None
        assert sys.exc_info()[2] is None

    def subFunction():
        print "Entering with exception info", sys.exc_info()

        assert sys.exc_info()[0] is not None
        assert sys.exc_info()[1] is not None
        assert sys.exc_info()[2] is not None

        try:
            print "Trying"
        except:
            pass

        print "After trying something and didn't have an exception, info is", sys.exc_info()

    print "Call a function inside the exception handler and check there too."

    try:
        raise KeyError
    except:
        assert sys.exc_info()[0] is not None
        assert sys.exc_info()[1] is not None
        assert sys.exc_info()[2] is not None

        subFunction()

    print "Call it twice and see."

    try:
        raise "me"
    except:
        assert sys.exc_info()[0] is not None
        assert sys.exc_info()[1] is not None
        assert sys.exc_info()[2] is not None

        subFunction()
        subFunction()


if sys.version_info[0] < 3:
    sys.exc_clear()

checkExcInfoScope()

print "*" * 20

# Check that the sys.exc_info is cleared again, after being set inside the
# function checkExcInfoScope, it should now be clear again.
assert sys.exc_info()[0] is None, sys.exc_info()[0]
assert sys.exc_info()[1] is None
assert sys.exc_info()[2] is None

print "Check catching subclasses"

def checkDerivedCatch():
    class A( BaseException ):
        pass
    class B( A ):
        def __init__( self ):
            pass

    a = A()
    b = B()

    try:
        raise A, b
    except B, v:
        print "Caught B", v
    except A, v:
        print "Didn't catch as B, but as A, Python3 does that", v
    else:
        print "Not caught A class, not allowed to happen."

    try:
        raise B, a
    except TypeError, e:
        print "TypeError with pair form for class not taking args:", e


checkDerivedCatch()

print "*" * 20


def checkNonCatch1():
    print "Testing if the else branch is executed in the optimizable case:"

    try:
        0
    except TypeError:
        print "Should not catch"
    else:
        print "Executed else branch correctly"

checkNonCatch1()
print "*" * 20

def checkNonCatch2():
    try:
        print "Testing if the else branch is executed in the non-optimizable case:"
    except TypeError:
        print "Should not catch"
    else:
        print "Executed else branch correctly"


checkNonCatch2()
print "*" * 20

print "Checking raise that with exception arguments that raise error themselves."


def checkRaisingRaise():
    def geterror():
        return 1/0

    try:
        geterror()
    except Exception, e:
        print "Had exception", e

    try:
        raise TypeError, geterror()

    except Exception, e:
        print "Had exception", e

    try:
        raise TypeError, 7, geterror()

    except Exception, e:
        print "Had exception", e


checkRaisingRaise()
print "*" * 20

print "Checking a re-raise that isn't one:"

def checkMisRaise():
    raise

try:
    checkMisRaise()
except Exception, e:
    print "Without existing exception, re-raise gives:", e

print "*" * 20

print "Raising an exception in an exception handler gives:"

def nestedExceptions( a, b ):
    try:
        a / b
    except ZeroDivisionError:
        a / b

try:
    nestedExceptions( 1, 0 )
except Exception, e:
    print "Nested exception gives", e

print "*" * 20

print "Checking unpacking from an exception as a sequence:"

def unpackingCatcher():
    try:
        raise ValueError(1,2)
    except ValueError as (a,b):
        print "Unpacking caught exception and unpacked", a, b

unpackingCatcher()
print "*" * 20

print "Testing exception that escapes __del__ and therefore cannot be raised"

def unraisableExceptionInDel():
    class C:
        def __del__( self ):
            c = 1 / 0

    def f():
        C()

    f()

unraisableExceptionInDel()
print "*" * 20

print "Testing exception changes between generator switches:"

def yieldExceptionInteraction():
    def yield_raise():
        try:
            raise KeyError("caught")
        except KeyError:
            yield sys.exc_info()[0]
            yield sys.exc_info()[0]
        yield sys.exc_info()[0]

    g = yield_raise()
    print "Initial yield from catch in generator", next( g )
    print "Checking from here", sys.exc_info()[0]
    print "Second yield from the catch reentered", next( g )
    print "Checking from here again ", sys.exc_info()[0]
    print "After leaving the catch generator yielded", next( g )

yieldExceptionInteraction()
print "*" * 20

print "Testing exception change between generator switches while handling an own exception"

def yieldExceptionInteraction2():

    def yield_raise():
        print "Yield finds at generator entry", sys.exc_info()[0]
        try:
            raise ValueError("caught")
        except ValueError:
            yield sys.exc_info()[0]
            yield sys.exc_info()[0]
        yield sys.exc_info()[0]

    try:
        z
    except Exception:
        print "Checking from here", sys.exc_info()[0]
        g = yield_raise()
        v = next( g )
        print "Initial yield from catch in generator", v
        print "Checking from here", sys.exc_info()[0]
        print "Second yield from the catch reentered", next( g )
        print "Checking from here again ", sys.exc_info()[0]
        print "After leaving the catch generator yielded", next( g )

yieldExceptionInteraction2()
print "*" * 20

print "Check what happens if a function attempts to clear the exception in a handler"

def clearingException():
    def clearit():
        try:
            if sys.version_info[0] < 3:
                sys.exc_clear()
        except KeyError:
            pass

    try:
        raise KeyError
    except:
        print "Before clearing, it's", sys.exc_info()
        clearit()

        print "After clearing, it's", sys.exc_info()

clearingException()
print "*" * 20

print "Check that multiple exceptions can be caught in a handler through a variable:"

def multiCatchViaTupleVariable():
    some_exceptions = (KeyError, ValueError)

    try:
        raise KeyError
    except some_exceptions:
        print "Yes, indeed."

multiCatchViaTupleVariable()

def raiseValueWithValue():
    try:
        raise ValueError(1,2,3), (ValueError(1,2,3))
    except Exception as e:
        print "Gives", e

print "Check exception given when value is raised with value", raiseValueWithValue()

# Make sure the repr is fine, at one time for Python3, they were actually really string objects, unnoticed:

a = IOError
print repr(a)
