from nose.tools import eq_

from ..user import User

def test_user():
    
    id = 10
    text = "Foobar?"
    
    user = User(id, text)
    
    eq_(user.id, id)
    eq_(user.text, text)
    
    eq_(user, User(user))
    eq_(user, User(user.to_json()))
