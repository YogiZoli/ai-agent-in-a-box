# STATUS: ai-agent-in-a-box

Updated: 2026-10-07

End goal: the 3x AI Agents page lives here, in its own Railway project, fed by a
read-only internal API of Publishing Dream Team.

Live: https://ai-agent-in-a-box-production.up.railway.app (Railway project
`ai-agent-in-a-box`, health check /health). The page, its pure panel code and its
tests were moved over unchanged from publishing-dreamteam. It has no database and
no sign-in, and renders its honest empty state because the data feed is not
connected.

Publishing Dream Team no longer serves the page: the menu item, the route, the
template, the panel code and the `metrics_agents` flag are gone from it. Its
`/metrics` lands on Per video.

Next (Zoltan decides when): the data feed from PDT (a read-only internal API with
a service token) and how a visitor is recognised (a signed hand-off from PDT was
proposed in publishing-dreamteam docs/CARD-PLAN.md; nothing is built).
