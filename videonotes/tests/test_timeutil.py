from videonotes import timeutil as tu


def test_ids_and_days():
    ts = 1_795_357_920.0
    sid = tu.new_session_id(ts)
    assert len(sid) == 20 and sid[8] == "-" and sid[15] == "-"
    day = tu.local_date(ts)
    a, b = tu.day_bounds(day)
    assert a <= ts < b and 23 * 3600 <= b - a <= 25 * 3600
    assert tu.parse_day(day) == day and tu.parse_day(None) == tu.parse_day("today")


def test_formatting():
    assert tu.fmt_offset(5) == "0:05" and tu.fmt_offset(3725) == "1:02:05"
    assert tu.fmt_duration(45) == "45 s" and tu.fmt_duration(720) == "12 min" and tu.fmt_duration(3900) == "1 h 05 min"
    assert tu.slugify('Budget: Q3/"plan"?') == "Budget Q3 plan" and tu.slugify("///") == "Untitled"
