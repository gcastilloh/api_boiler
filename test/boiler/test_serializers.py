from app.boiler.serializers import ProgrammSerializer

def test_valid_Programm_serializar():
    ## ----- Given: --------
    valid_serializer_data = {
        "day": 1,
        "hour": 15,
        "minutes": 0,
        "duration": 15,
        "active": True,
    }
    serializer = ProgrammSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}
    
def test_invalid_Programm_serialaizar():
    pass