2014-07-14
==========

Diff functionality officially split out.  See http://github.org/halfak/deltas
Woot.  OK.  So my plan for today is to start removing the diff functionality
from this project and including it as a dependency.

First, I need to go to conf.yaml to structure it to represent the imports from
deltas. ... {{done}}

Next I need to trim out the modules we won't be using anymore.

... bah!  Ran out of time thinking about how I'd adjust the "Operation" type
now that the difference algorithms have been removed.  I'll have to come back to
that next time. 

2014-07-03
==========

I haven't really figured out how I'd split out the diff functionality.  I
figured that I'd make use of the work-log to work it out.  So, I'd like to have
the token diffing part of this system in its own library, but I'd also like to
have some straightforward configuration for the entire diffengine system.

In the case of logging, I have sort of a sub-documentation format going on.
Logging has it's own dict-based config format so I just put that into the main
config yaml file.  I could do that with diff algorithms and segmenters.

On the other hand, I could just not have a config directive in the difference
algorithms or segmenters and simply extend the segmenters in order to provide
a from_config class method.  What do you think rubber ducky?

Now practically, I could delay this design change.  That would help me keep
pushing toward getting the diffengine online.  On the other hand, I'd be racking
up some technical debt.  Presumably, I'd need to spend more time fixing this later
than right now, so from a utilitarian sense, I should probably do it right now.
However, this decision theory calculus fails to account for deadlines.  I'd like
to present an MVP of the whole persistence project at Wikimedia.  A quick check
of the calendar puts that at less than 1 month away.  Eek.

OK.  So it isn't bad to waste a couple of hours exploring how difficult it is
to decouple these libraries.

2014-06-29
==========

OK.  So I think that it's important that I split out the diff functionality from
this package.  That stuff is generally useful and serves a somewhat different
function than the rest of the package here (servers, synchronization, storage,
etc.), but I don't really want to deal with that right now.
