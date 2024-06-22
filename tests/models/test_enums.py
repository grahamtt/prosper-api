from prosper_api.models import ProsperRating


def test_repr():
    assert repr(ProsperRating.NA) == "ProsperRating.NA"
