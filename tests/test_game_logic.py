from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Tests targeting the high/low message bug ---
# The original bug: when guess > secret the message said "Go HIGHER!" (wrong),
# and when guess < secret it said "Go LOWER!" (wrong). Both messages were swapped.

def test_too_high_message_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message!r}"

def test_too_low_message_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message!r}"

def test_too_high_message_does_not_say_go_higher():
    # Regression guard: the old bug returned "Go HIGHER!" for a guess that was too high
    _, message = check_guess(99, 1)
    assert "HIGHER" not in message, f"Message should not say HIGHER when guess is too high, got: {message!r}"

def test_too_low_message_does_not_say_go_lower():
    # Regression guard: the old bug returned "Go LOWER!" for a guess that was too low
    _, message = check_guess(1, 99)
    assert "LOWER" not in message, f"Message should not say LOWER when guess is too low, got: {message!r}"
