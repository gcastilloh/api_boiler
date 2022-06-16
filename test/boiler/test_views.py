from unittest.case import _AssertRaisesContext
import pytest
from app.boiler.models import Programms

@pytest.mark.django_db
def test_get_single_Programm(client):
    ## --- given ---

    Programm = Programms.objects.create(
        day = 1,
        hour = 15,
        minutes = 0,
        duration = 15,
        active = True,
    )

    ## --- when: ------
    resp = client.get(f"/programas/{Programm.id}")

    ## --- then: -----
    assert resp.status_code == 200
    assert resp.data["day"] == Programm.day and resp.data["hour"]==Programm.hour and resp.data["minutes"]==Programm.minutes

    
@pytest.mark.django_db
def test_get_single_Programm_incorrect_id(client):
    ## ----- when: ------
    resp = client.get(f"/programas/4")

    ## -- then ---
    assert resp.status_code == 404



