import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup

def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_withdraw_unknown_account():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "fixed_deposit", True)


def test_withdraw_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, -100, "savings", True)


def test_withdraw_limit_exceeded():
    assert withdraw(50000, 30000, "savings", True) == "limit exceeded"


def test_withdraw_other_bank_with_fee():
    assert withdraw(20000, 15000, "savings", False) == 4970


def test_withdraw_insufficient_funds():
    assert withdraw(1000, 2000, "savings", True) == "insufficient funds"

def test_pin_check_card_blocked_max_attempts():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_pin_check_card_blocked_on_second_failed_attempt():
    assert pin_check(9999, 1234, 2) == "card blocked"


def test_pin_check_retry():
    assert pin_check(9999, 1234, 1) == "retry"


def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)


def test_note_breakup_with_200_notes():
    assert note_breakup(800) == (1, 1, 1)


def test_note_breakup_without_200_notes():
    assert note_breakup(600) == (1, 0, 1)
