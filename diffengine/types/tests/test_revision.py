from nose.tools import eq_

from ..delta import Delta
from ..operations import Delete, Equal, Insert
from ..revision import Revision
from ..timestamp import Timestamp
from ..user import User


def test_revision():
    rev_id = 10
    timestamp = Timestamp(1234567890)
    sha1 = "123467890123457890123457890AB"
    page_id = 12
    user = User(10, "foobar")
    delta = Delta(55, 35, [Insert(0, 2, 0, 2, ["who", "?"])])
    
    revision = Revision(rev_id, timestamp, sha1, page_id, user, delta)
    
    eq_(revision.rev_id, rev_id)
    eq_(revision.timestamp, timestamp)
    eq_(revision.sha1, sha1)
    eq_(revision.page_id, page_id)
    eq_(revision.user, user)
    eq_(revision.delta, delta)
    
    print(revision.to_json())
    eq_(revision, Revision(revision.to_json()))
