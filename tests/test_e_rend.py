import pytest
from FBs.events.E_REND_2 import E_REND_2, States


@pytest.fixture
def instance():
    return E_REND_2()


def test_first_then_second(instance):
    inst = instance
    val, *other = inst.schedule("EI1", 1)
    assert val is None
    val, *other = inst.schedule("EI2", 1)
    assert val == 1


def test_second_than_first(instance):
    inst = instance
    val, *other = inst.schedule("EI2", 1)
    assert val is None
    val, *other = inst.schedule("EI1", 1)
    assert val == 1


def test_reset_e2(instance):
    inst = instance
    val, *other = inst.schedule("EI2", 1)
    assert val is None
    val, *other = inst.schedule("R", 1)
    assert val is None
    assert inst.state == States.START


def test_reset_e1(instance):
    inst = instance
    val, *other = inst.schedule("EI1", 1)
    assert val is None
    val, *other = inst.schedule("R", 1)
    assert val is None
    assert inst.state == States.START


def test_reset_at_start(instance):
    inst = instance
    val, *other = inst.schedule("R", 1)
    assert val is None
    assert inst.state == States.START
