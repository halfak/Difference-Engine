2014-10-04
==========
I haven't written in a while, but I have been working.  The engine priming
enwiki on diffengine.labs needs a lot of babysitting.  I've had this
intermittent problem that has got me devoting a lot of time to mw.xml_dump.map
and it's behavior for catching errors.  The process keeps getting hung up, but
the last reported error doesn't tell me anything useful.

While I have the most recent version of log-riddled code running, I should
really spend some time thinking about diffengine's API and how it will interact
with the persistengine.  The primary way that I expect the persistengine to talk
to diffengine is by way of a call like this:

* /enwiki/?after_rev_id=283473694&dir=newer&limit=50

That would get the next 50 diffs of revisions saved after rev_id 283473694. It
would allows the persistengine to stay in sync with the diffengine.

You could also just query for a user by doing:

* /enwiki/?user_id=567892&dir=newer&limit=50
* /enwiki/?user_id=567892&after_rev_id=1234&dir=newer&limit=50

Or query for a page by doing

* /enwiki/&page_id=38928442&dir=newer&limit=50
* /enwiki/?page_id=38928442&after_rev_id=1234&dir=newer&limit=50

So, I think I'm going to try to drop the storage requirements for the
persistengine and instead just provide the facilities to do the computations on
the fly with diffengine's data.  That might be performant enough for usage.
From an analysis perspective, I'd like to have the persistengine store
something.  Maybe I'll just have it store PWR scores (or something like that).
I can certainly have it cache scores for quick retrieval.  Oh well, all this will be for another worklog. 

2014-08-15
==========
Well...  Wikimania went nicely.  The whole value-added-to-Wikipedia concept was
relatively well recieved.  It looks like I need to kick into gear!  Happily, I
have the entire dump of Simple English Wikipedia loaded.  Sadly, I forgot to
pull some changes, so I have unix_timestamps in the revision.timestamp field
rather than the short DB format (YYYYMMDDHHMMSS) so, that's a fun problem to
solve.

I've been working on JSONable too in order to make sure that pickling will work
as expected.

Anyway, I'm loggin' today because I need to capture an idea.  It's simple.  My
priming script should write out json files that can be loaded into a database
rather than writing directly to the database.  This might break some nice
abstractions that I have with "stores" and such, but it requires a nice
separation of concerns that I'd like to enforce.  Engines do *not* write to a
"store" on their own.  They produce things that can be writen to a store.

2014-07-25
==========

I was nearly home-free when I realized that the dump primer was looking pretty
goddamn crazy.  The biggest problem is that I need to maintain database
connections (via an Engine) for every XML mapper *or* I need to figure out how
the mappers can share a single Engine.

Arg!  This is silly!  If the Engine is responsible for storage, it's easy to
write code that simply makes use of an Engine.  But if the engine is responsible
for storage then it's hard to farm out the CPU intensive work.  Optimally, I'd
like to be able to split the CPU intensive work from the data storage system.

----

Well... I think it is better.  I haven't fixed my XML processor issue, bit an
Engine is no longer coupled with a Store.  Not totally sure this is better, but
I feel better about it.  *fingers crossed* that I didn't just make a bunch of
work for myself later.

2014-07-24
==========
Refactor mostly complete.

* Engine(name, tokenizer)
    *.set_status(status)
    *.processor(status)
* Processor(status)
    *.process(rev_id, timestamp, text)
    *.set_status(status)
* Synchronizer(source, engine, store)
* Webserver(stores)
* Source(wiki_connection_info)
* Store(database_connection_info)

All is pulled from the config file (mwahahaha).

2014-07-23
==========

Alright.  So I did a lot of work on config2.yaml.  I think I have a structure I
like.

* Engine -- Responsible for managing a store of diff information.
* Processor -- Responsible for managing a single page's diff information.
* Synchronizer -- Conbines a source and an engine to load revisions into an Engine
* Webserver -- Publishes a WSGI connector for serving diff information RESTfully
* Source --  A source of changes (new revisions).  (API or Database)
* Store -- A location where a single wiki's difference information is stored

2014-07-22
==========

I'm in war mode.  I want this system operational for Wikimania.  I've given up
on the possibility of having an MVP for Wikimania, but I'm going to get far.
Right now, this biggest problem that I am dealing with is status maintenance.
I need to be able to store the status of the system in a nuanced way, but I
don't want to store any logic in the datastore.  That means I need to store
separate state objects.  Right now, I see two good examples of state objects
to store.

* SynchronizerState -- Represents the state of the entire set of diffs for a
    MediaWiki installation.
* EngineState -- Represents the status of a single page.  An "engine" is
    something that takes a new "text" and produces a new "delta".

----

OK.  Got a lot done today.  All types are tested.  I got the SequenceMatcher
"engine" running.  However, I think I want to restructure the config/system
structure so that one wiki == one engine.  I'll need to rename the
SequenceMatcher "engine" to "processor" or something equivalent.  That's all for
today.

2014-07-15
==========

Trying to cram in a little bit of work in the morning before the rest of the
world wakes up.  My goal today is to finish up the operations stuff.

... so.  I gave up on my inheritance scheme.  Operations are going to be
their own thing within the diffengine.

2014-07-14
==========

Diff functionality officially split out.  See http://github.org/halfak/deltas
Woot.  OK.  So my plan for today is to start removing the diff functionality

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
