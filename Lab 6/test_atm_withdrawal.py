import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup

def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_withdraw_unknown_account_branch():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "demat", True)


def test_withdraw_invalid_amount_zero_or_negative():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)

    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, -500, "savings", True)


def test_withdraw_invalid_amount_not_multiple_of_100():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 250, "savings", True)


def test_withdraw_limit_exceeded_savings():
    assert withdraw(50000, 26000, "savings", True) == "limit exceeded"


def test_withdraw_limit_exceeded_current():
    assert withdraw(100000, 51000, "current", True) == "limit exceeded"


def test_withdraw_current_account_success():
    assert withdraw(60000, 40000, "current", True) == 20000


def test_withdraw_other_bank_under_10k():
    assert withdraw(5000, 3000, "savings", False) == 1980


def test_withdraw_other_bank_over_10k():
    assert withdraw(20000, 15000, "savings", False) == 4970


def test_withdraw_insufficient_funds_plain():
    assert withdraw(1000, 2000, "savings", True) == "insufficient funds"


def test_withdraw_insufficient_funds_due_to_fee():
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_withdraw_exact_balance_own_bank():
    assert withdraw(1000, 1000, "savings", True) == 0


def test_pin_check_card_blocked_attempts_three():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_pin_check_card_blocked_attempts_greater_than_three():
    assert pin_check(1234, 1234, 5) == "card blocked"


def test_pin_check_wrong_pin_second_attempt_blocks_card():
    assert pin_check(9999, 1234, 2) == "card blocked"


def test_pin_check_wrong_pin_first_attempt_retries():
    assert pin_check(9999, 1234, 1) == "retry"


def test_pin_check_wrong_pin_zero_attempt_retries():
    assert pin_check(9999, 1234, 0) == "retry"


def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(175)


def test_note_breakup_remaining_greater_or_equal_200():
    assert note_breakup(800) == (1, 1, 1)

    assert note_breakup(400) == (0, 2, 0)


def test_note_breakup_remaining_less_than_200():
    assert note_breakup(600) == (1, 0, 1)

    assert note_breakup(500) == (1, 0, 0)
