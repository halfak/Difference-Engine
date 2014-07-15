from nose.tools import eq_

from ..delta import Delta
from ..operations import Insert, Equal, Delete
from ..user import User
from ..revision import Revision, Timestamp

def test_revision():
    rev_id = 10
    timestamp = Timestamp(1234567890)
    page_id = 12
    user = User(10, "foobar")
    delta = Delta("foobar_matcher", 55, 35, [Insert(0, 2, 0, 2, ["who", "?"])])
    
    revision = Revision(rev_id, timestamp, page_id, user, delta)
    
    r2 = Revision(revision.to_json())
    eq_(revision, r2)
    eq_(r2.rev_id, rev_id)
    eq_(r2.timestamp, timestamp)
    eq_(r2.page_id, page_id)
    eq_(r2.user, user)
    eq_(r2.delta, delta)
