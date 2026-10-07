"""The three agents panels. Copied unchanged from publishing-dreamteam app/analytics.py (2026-10-07). Pure, no I/O."""

def _fmt_int(n: int) -> str:
    """Thousands separated with a thin space, the same in every locale."""
    return f"{int(n):,}".replace(",", " ")


# The three agents (DECISIONS.md, 2026-09-06). The page is shaped like the
# argument the product is sold on:
#
#     subscribers = impressions x click-through rate x opt-in rate
#
# Each agent owns exactly one of those three factors, so every claim in the
# marketing is a number the creator can read off their own screen. The order is
# the order of the multiplication, not an order of importance.
AGENTS = (
    {
        "key": "reach",
        "name": "Reach agent",
        "owns": "impressions",
        "does": "title, tags, hashtags, chapters, localization",
    },
    {
        "key": "click",
        "name": "Click agent",
        "owns": "click-through rate",
        "does": "thumbnail prompt, title",
    },
    {
        "key": "subscriber",
        "name": "Subscriber agent",
        "owns": "subscribers, opt-in rate",
        "does": "description link, pinned comment, keyword automation",
    },
)


def agent_panels(
    totals: dict,
    subs: dict,
    clicks: dict,
    *,
    subscriber_hook: bool = True,
) -> list[dict]:
    """One panel per agent, always three, always carrying a real number.

    A panel is never omitted and never left blank. A factor that cannot be
    measured yet says why in its own words and still shows the nearest number
    that IS measured, because a silent panel and a panel reading zero look
    identical to a creator, and only one of them is honest.

    Pure: `totals` is totals_by_video(), `subs` is hooks.summary(), `clicks` is
    shortlinks.clicks_for(). Nothing here queries anything.
    """
    impressions = sum(int(t.get("impressions") or 0) for t in totals.values())
    views = sum(int(t.get("views") or 0) for t in totals.values())
    # CTR is re-derived from implied clicks over the whole channel, never an
    # average of per-video percentages: those are computed over different
    # impression counts, so their mean is not the channel's click-through rate.
    implied = sum(
        int(t.get("impressions") or 0) * float(t.get("impressions_ctr") or 0.0) / 100
        for t in totals.values()
    )
    link_clicks = sum(sum(by_medium.values()) for by_medium in clicks.values())
    total_subs = int(subs.get("total") or 0)
    attributed = int(subs.get("attributed") or 0)

    reach = {
        "value": _fmt_int(impressions) if impressions else None,
        "state": "measured" if impressions else "waiting",
        "support": f"{_fmt_int(views)} views so far.",
        "note": (
            "How many times YouTube put your videos in front of someone."
            if impressions
            else "Impressions arrive from YouTube two to three days late, and "
            "only from the day your channel was connected. Until the first "
            "report lands, views are the honest stand-in."
        ),
    }

    ctr = round(implied / impressions * 100, 2) if impressions else None
    click = {
        "value": f"{ctr}%" if ctr is not None else None,
        "state": "measured" if ctr is not None else "waiting",
        "support": (
            f"{_fmt_int(round(implied))} of those impressions turned into a view."
            if impressions
            else f"{_fmt_int(views)} views, with nothing yet to divide them by."
        ),
        "note": (
            "How often the thumbnail and title were good enough to click."
            if ctr is not None
            else "This one needs impressions, so it fills in when the reach "
            "report above does."
        ),
    }

    # The opt-in rate is the whole reason a click is counted at all. It is a
    # denominator here and nowhere else: the click is never a headline number.
    opt_in = round(attributed / link_clicks * 100, 1) if link_clicks else None
    if not subscriber_hook:
        sub_note = (
            "Subscriber counting is switched off right now, so this number "
            "cannot move. Nothing has been lost; it resumes when it is back on."
        )
    elif total_subs:
        sub_note = (
            f"{attributed} of them can be traced to a specific video."
            if attributed < total_subs
            else "Every one of them can be traced to a specific video."
        )
    else:
        sub_note = (
            "Your list lives in your own tool and this app never reads it, so "
            "your tool has to tell this app when someone subscribes. One step, "
            "set up once, on your account page."
        )
    subscriber = {
        # Always a number, including zero. A list nobody has joined and a
        # webhook that was never wired up both read zero here, and the note is
        # what tells them apart.
        "value": _fmt_int(total_subs),
        # The factor this agent OWNS is the opt-in rate, not the subscriber
        # count, so it is only "measured" once a click exists to divide by.
        # Without this the compounding line below would quote the 1.95
        # arithmetic over a factor that has no denominator, which is the exact
        # dishonesty this page exists to avoid.
        "state": (
            ("measured" if opt_in is not None else "waiting")
            if subscriber_hook
            else "off"
        ),
        "support": (
            f"{opt_in}% of the {_fmt_int(link_clicks)} people who clicked a link subscribed."
            if opt_in is not None
            else "Nobody has clicked one of your links yet, so the opt-in rate "
            "has no denominator to stand on."
        ),
        "note": sub_note,
    }

    by_key = {"reach": reach, "click": click, "subscriber": subscriber}
    return [{**agent, **by_key[agent["key"]]} for agent in AGENTS]


def compounding_line(panels: list[dict]) -> str:
    """One sentence under the three panels, and never an invented one.

    The 1.95 arithmetic is only quoted when all three factors are actually being
    measured. Quoting it over two measured factors and a blank would be selling
    the argument with the argument's own evidence missing.
    """
    measured = [p for p in panels if p["state"] == "measured" and p["value"] is not None]
    if len(measured) == 3:
        return (
            "All three are measured, so they multiply. Improve each by 25 "
            "percent and you get 1.95 times the subscribers, nearly double, "
            "from three changes that each look small on their own."
        )
    missing = [p["name"] for p in panels if p not in measured]
    return (
        "These three multiply together, so the weakest one caps the other two. "
        "Not measured yet: " + ", ".join(missing) + "."
    )
