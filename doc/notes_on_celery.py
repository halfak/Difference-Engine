# database setup initialized here like in Wikimetrics
#   https://github.com/wikimedia/analytics-wikimetrics/blob/master/wikimetrics/configurables.py#L161
#   https://github.com/wikimedia/analytics-wikimetrics/blob/master/wikimetrics/database.py
#   
#   Oh!  So, you're constructing DB at the module level.  I guess that makes sense.  That will 
#   force the worker to hang onto the reference, right?
#   The session is managed using celery signals
#       https://github.com/wikimedia/analytics-wikimetrics/blob/master/wikimetrics/configurables.py#L203
#       db sessions are removed there ^ when a task ends, and that signal is fired regardless of task status
#       signals in general are good things to know about.
#           Will that destruct the db at the end of task execution, when a task is killed or when the whole
#           worker is killed?
#               It won't destroy the db, it'll just close the session, the "db" object is just a way to wrap methods like
#               get_session around configuration that's loaded at import time.  Timing wise, it'll close the session at
#               the end of task execution OR when the task is killed
#                   My confusion here:  What's a session?  .. if not a connection?
#                       Oh, right, a SQLAlchemy session is an object that will open a connection when it executes, but may
#                       do different things with that connection throughout its lifetime.  If you call .remove() on it, it
#                       will just rollback any transactions and kill any open connections.
#                           Ahh yeah.  That's what I meant by "destruct".  But my real question is "when it will happen"... 
#                           ahh.  OK.  So a task is killed -- not when it finishes executing -- but when celery decides to 
#                           kill it -- which should be less often?
#                               Usually the task exits and returns a result.  Less usually the task will error and raise,
#                               in which case celery cleans up after it and still fires that signal.  Least usual is when
#                               the task is unresponsive and celery decides the SoftTimeLimit has been exceeded.  At this
#                               point it raises a "Soft Time Limit Exceeded" exception and the task can gracefully deal.
#                               If it does not deal, a "Hard Time Limit Exceeded" exception is thrown and the task stops.
# Ok.  So, is a database connection/session being created and closed for each task execution?
#   In wikimetrics it is, but this is up to you.  Normally it's pretty cheap so it's ok
#       I want to process ~50 tasks every 5 seconds or so.  So, 10 dbconnects per second.
#           I don't think this would be a problem, we've done much more in wikimetrics, but you can keep the session around.
#           problem with keeping it is you have to serialize it to each task and then json serialization no worky :) (pickle)
#               Yeah.  That's one of the things I was worried about.  So.  Final check.  I'll make notes below...
#
from configurables import db # Import of DB stuff happens here
# also, I think Yuvi looked through the wikimetrics code and made it better for quarry, so that may be worth a read

@app.task
def process_revisions(page_id, page_revs):
    """
    Processes a sequence of revisions, updates state and 
    returns a list of diffs for the revisions.
    """
    # load from some DB or create new.  Where will I get the DB connection?
    # just use the "db" object as imported above
    page_processor = load_page_processor(db, page_id) # I get to assume that 'db' exists here
    
    # process revision in sequence
    # if you want to be able to re-run a single failed revision processing operation,
    #   and/or be able to abort the chain if such a failure happens, you may want each
    #   revision to be a separate task in the chain (not sure about performance either way)
    diffs = []
    for revision in page_revs:
        diffs.append(page_processor.process(revision))
    
    # store new state
    store_page_processor(db, page_processor) # And I get to assume that db exists here


@task_postrun.connect()
def task_postrun(*args, **kwargs):
    # always, no matter exceptions or not, remove database sessions
    
    

def store_diffs(diffs):
    # stores diffs in some DB.  This DB connection is easy


def main():
    listener = # some streaming iterable of revision metadata
    
    for revisions in take_n(listener, 50):
        
        # Group revisions by page
        pages_revs = defaultdict(lambda: [])
        for revision in revisions:
            pages_revs[revision.page_id].append(revision)
        
        # Start tasks -- one per page
        page_tasks = {}
        for page_id, page_revs in pages_revs.items():
            task = process_revisions.delay(page_id, page_revs)
            page_tasks[page_id] = task
        
        # Barrier synchronization for all tasks to finish
        for page_id, task in page_tasks.items():
            diffs = task.get()
            store_diffs(diffs)
        
