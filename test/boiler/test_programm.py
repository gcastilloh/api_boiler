import pytest
from app.boiler.models import Programms

@pytest.mark.django_db
def test_Programms_model():
    ## ------- Given: -------
    Programm = Programms(
        day = 0,
        hour = 15,
        minutes = 0,
        duration = 15,
        active = True,
    )

    ## ------ When: ---------
    Programm.save()

    ## ----- Then ---------

    assert Programm.day == 0
    assert Programm.hour == 15
    assert Programm.minutes == 0
    assert Programm.duration == 15
    assert Programm.active == True
