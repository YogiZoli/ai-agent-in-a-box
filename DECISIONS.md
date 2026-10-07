# DECISIONS: ai-agent-in-a-box

## 2026-10-07: first a plain file move
Zoltan's call: move the page over now, wire data and sign-in later. No database
(nothing to store), no own GCP project, no own YouTube OAuth, no custom domain.

## 2026-10-07: the page left PDT
Done as a plain move. PDT no longer serves it. Your Tracking Link and Per Video in
PDT were not touched by the move. The data feed and sign-in are a later step.

## 2026-10-08: no temporary feed from PDT
Zoltan: the PDT UI stays untouched. The service gets its data only once it has
its own domain, GCP project, OAuth and sign-in (STATUS.md, plan). Subscriber
numbers come from vidrev. Own GCP project because of own quota, own brand on
the consent screen and isolation from PDT's verified app.
