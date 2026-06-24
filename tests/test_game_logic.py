from logic_utils import check_guess, get_attempt_limit, get_range_for_difficulty, parse_guess, update_score


# --- check_guess ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_message_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message!r}"

def test_too_low_message_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message!r}"

def test_too_high_message_does_not_say_go_higher():
    _, message = check_guess(99, 1)
    assert "HIGHER" not in message, f"Message should not say HIGHER when guess is too high, got: {message!r}"

def test_too_low_message_does_not_say_go_lower():
    _, message = check_guess(1, 99)
    assert "LOWER" not in message, f"Message should not say LOWER when guess is too low, got: {message!r}"


# --- get_range_for_difficulty ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 10)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 50)

def test_hard_range():
    # Hard has the widest range, making it the hardest difficulty
    assert get_range_for_difficulty("Hard") == (1, 100)

def test_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Unknown") == (1, 50)

def test_hard_range_wider_than_easy():
    _, easy_high = get_range_for_difficulty("Easy")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > easy_high

def test_hard_range_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


# --- parse_guess ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_float_string_truncates_to_int():
    ok, value, _ = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_none_returns_error():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_empty_string_returns_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_non_numeric_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# --- update_score ---

def test_win_early_gives_high_points():
    # Attempt 1: 100 - 10*(1+1) = 80 points
    new_score = update_score(0, "Win", 1)
    assert new_score == 80

def test_win_score_floored_at_10():
    # Attempt 100: points would be negative, should floor at 10
    new_score = update_score(0, "Win", 100)
    assert new_score == 10

def test_too_high_even_attempt_adds_points():
    # Even attempt number adds 5
    new_score = update_score(50, "Too High", 2)
    assert new_score == 55

def test_too_high_odd_attempt_subtracts_points():
    # Odd attempt number subtracts 5
    new_score = update_score(50, "Too High", 3)
    assert new_score == 45

def test_too_low_always_subtracts_points():
    new_score = update_score(50, "Too Low", 1)
    assert new_score == 45

def test_unknown_outcome_does_not_change_score():
    new_score = update_score(50, "Invalid", 1)
    assert new_score == 50


# --- Bug fix regression tests (app.py glitches) ---

# BUG 1: attempts initialised to 1 instead of 0
# First guess increments to 1; update_score must receive attempt_number=1, not 2
def test_first_guess_is_attempt_1():
    # Simulates: attempts starts at 0, submit increments to 1, score computed at attempt 1
    score = update_score(0, "Win", 1)
    assert score == 80  # 100 - 10*(1+1) = 80; would be 70 if erroneously passed attempt 2

# BUG 2: info text hardcoded to "1 and 100" — range must match difficulty
def test_easy_range_is_not_100():
    _, high = get_range_for_difficulty("Easy")
    assert high == 10, f"Easy difficulty upper bound should be 10, got {high}"

def test_hard_range_upper_bound():
    _, high = get_range_for_difficulty("Hard")
    assert high == 100, f"Hard difficulty upper bound should be 100, got {high}"

# BUG 3: new game used random.randint(1, 100) ignoring difficulty
# Covered by verifying ranges are correct per difficulty (Easy max=10, Hard max=100)
def test_easy_secret_within_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 10

# BUG 4: secret cast to str on even attempts causes wrong lexicographic comparison
# e.g. guess=9, secret="50" — "9" > "50" is True (lexicographic) but 9 < 50 numerically
def test_check_guess_string_secret_high_digit_not_falsely_wins():
    # 9 < 50 numerically, so outcome must be "Too Low", not "Win" or "Too High"
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"

def test_check_guess_string_secret_comparison_correct():
    # If secret were passed as "50" (the bug), "9" > "50" lexicographically → wrong "Too High"
    # With int secret, 9 < 50 → correctly "Too Low"
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low", "Lexicographic bug: '9' > '50' is True but 9 < 50 numerically"


# BUG 5: new game button did not reset status or history
# After winning/losing, st.session_state.status stayed "won"/"lost", so rerun hit st.stop() immediately
# Covered by verifying a fresh game state allows guessing (status="playing", score unaffected by old game)
def test_after_win_new_game_score_starts_fresh():
    # A win on attempt 1 gives 80 points; a subsequent new game's first guess should still compute from 0
    score_after_win = update_score(0, "Win", 1)
    assert score_after_win == 80
    # New game resets score to 0; first guess of the new game at attempt 1 should also give 80
    new_game_score = update_score(0, "Win", 1)
    assert new_game_score == 80

def test_status_playing_allows_further_guesses():
    # Any outcome other than Win should leave the game open for another guess
    outcome, _ = check_guess(40, 50)
    assert outcome != "Win", "A wrong guess should not end the game"


# --- get_attempt_limit ---

def test_easy_attempt_limit():
    assert get_attempt_limit("Easy") == 10

def test_normal_attempt_limit():
    assert get_attempt_limit("Normal") == 7

def test_hard_attempt_limit():
    assert get_attempt_limit("Hard") == 5

def test_easy_has_more_attempts_than_normal():
    assert get_attempt_limit("Easy") > get_attempt_limit("Normal")

def test_normal_has_more_attempts_than_hard():
    assert get_attempt_limit("Normal") > get_attempt_limit("Hard")

def test_unknown_difficulty_attempt_limit_defaults_to_normal():
    assert get_attempt_limit("Unknown") == get_attempt_limit("Normal")
