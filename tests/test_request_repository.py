from lib.request_repository import RequestRepository
from lib.request import Request
from lib.space_repository import SpaceRepository
from lib.space import Space

def test_all(db_connection):
    db_connection.seed("seeds/scar_bnb.sql")
    repository = RequestRepository(db_connection)
    assert repository.all() == []

"""
When we choose avaliable date,
we create a request to book a space
"""
def test_create_request(db_connection):
    db_connection.seed("seeds/scar_bnb.sql")
    repository = RequestRepository(db_connection)
    repository.create(Request(None, 1, 1, "01/01/2023", "TBC"))
    result = repository.all()
    assert result == [Request(1, 1, 1, "01/01/2023", "TBC")]

def test_find_request(db_connection):
    repository = RequestRepository(db_connection)
    repository.create(Request(None, 1, 1, "01/01/2023", "TBC"))
    assert repository.find(1) == Request(1, 1, 1, "01/01/2023", "TBC")

def test_decline_a_request(db_connection):
    repository = RequestRepository(db_connection)
    request = Request(None, 1, 1, "01/01/2023", "TBC")
    repository.create(request)
    request_1 = repository.find(1)
    repository.confirm(request_1)
    assert request_1.request_status == "True"

def test_find_spaces_by_user_id(db_connection):
    repository = RequestRepository(db_connection)
    space_repository = SpaceRepository(db_connection)

    space_2 = Space(None,"Example Name","Example description",200,"02-03-2023",1)
    space_repository.create(space_2)

    repository.create(Request(None, 1, 1, "01/01/2023", "TBC"))
    repository.create(Request(None, 1, 2, "01/01/2023", "TBC"))
    repository.create(Request(None, 2, 1, "01/01/2023", "TBC"))
    repository.create(Request(None, 2, 2, "01/01/2023", "TBC"))
    assert repository.find_spaces_by_user_id(1) == ""