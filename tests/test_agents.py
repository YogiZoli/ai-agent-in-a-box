import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

VID = "dQw4w9WgXcQ"

# --- The three agents on the Metrics page ------------------------------------

def _totals(**over):
    base = {"views": 100, "impressions": 1000, "impressions_ctr": 4.0}
    base.update(over)
    return base


def test_three_agents_are_always_all_three():
    """A factor that cannot be measured is still on screen, saying why.

    Dropping a panel and showing a zero look the same to a creator, and only
    one of them is true.
    """
    from app.agents import agent_panels

    panels = agent_panels({}, {"total": 0, "attributed": 0}, {})
    assert [p["key"] for p in panels] == ["reach", "click", "subscriber"]
    assert all(p["support"] and p["note"] for p in panels)
    # Nothing measured, so no invented number, but every panel explains itself.
    assert panels[0]["state"] == "waiting" and panels[0]["value"] is None
    assert panels[1]["state"] == "waiting" and panels[1]["value"] is None


def test_the_subscriber_panel_always_prints_a_number_including_zero():
    from app.agents import agent_panels

    panels = agent_panels({}, {"total": 0, "attributed": 0}, {})
    sub = panels[2]
    assert sub["value"] == "0"
    assert "your tool has to tell this app" in sub["note"]


def test_channel_ctr_is_derived_from_clicks_not_averaged():
    """Two videos with different impression counts: the mean of their two
    percentages is not the channel's click-through rate."""
    from app.agents import agent_panels

    totals = {
        "a": _totals(impressions=1000, impressions_ctr=10.0),   # 100 clicks
        "b": _totals(impressions=9000, impressions_ctr=1.0),    # 90 clicks
    }
    panels = agent_panels(totals, {"total": 0, "attributed": 0}, {})
    # 190 / 10000 = 1.9%, not the 5.5% a naive average would give.
    assert panels[1]["value"] == "1.9%"
    assert panels[0]["value"] == "10\u2009000"


def test_opt_in_rate_needs_a_denominator_and_says_so_when_it_has_none():
    from app.agents import agent_panels

    subs = {"total": 5, "attributed": 4}
    none = agent_panels({}, subs, {})[2]
    assert "no denominator" in none["support"]

    with_clicks = agent_panels({}, subs, {VID: {"description": 30, "comment": 10}})[2]
    assert "10.0% of the 40 people" in with_clicks["support"]
    assert with_clicks["value"] == "5"


def test_a_switched_off_hook_is_said_out_loud_not_shown_as_zero():
    from app.agents import agent_panels

    sub = agent_panels({}, {"total": 0, "attributed": 0}, {}, subscriber_hook=False)[2]
    assert sub["state"] == "off"
    assert "switched off" in sub["note"]


def test_the_compounding_claim_is_only_made_when_all_three_are_measured():
    """1.95 is the product of three measured factors. Quoting it with one of
    them blank would be selling the argument with its evidence missing."""
    from app.agents import agent_panels, compounding_line

    partial = agent_panels({}, {"total": 3, "attributed": 3}, {VID: {"description": 10}})
    assert "1.95" not in compounding_line(partial)
    assert "Reach agent" in compounding_line(partial)

    full = agent_panels(
        {"a": _totals()},
        {"total": 3, "attributed": 3},
        {VID: {"description": 10}},
    )
    assert "1.95" in compounding_line(full)


def test_subscribers_without_a_single_click_do_not_count_as_a_measured_factor():
    """Found on production, 2026-09-06: reach and CTR were measured and the
    subscriber panel read 0, and the page went on to quote the 1.95 arithmetic.
    The factor this agent owns is the opt-in RATE, so it is only measured once
    there is a click to divide by."""
    from app.agents import agent_panels, compounding_line

    panels = agent_panels(
        {"a": _totals()}, {"total": 0, "attributed": 0}, {}
    )
    assert panels[2]["state"] == "waiting"
    line = compounding_line(panels)
    assert "1.95" not in line
    assert "Subscriber agent" in line
    # The count itself is still printed. Silence is the thing being avoided.
    assert panels[2]["value"] == "0"


