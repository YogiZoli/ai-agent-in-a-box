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

## Plan to a standalone SaaS (Zoltan, 2026-10-08)

No temporary data feed from PDT: the PDT UI stays as it is, and a feed built
there would be thrown away once this service has its own access. The page stays
empty until the steps below.

Data sources, final: YouTube (impressions, click-through rate) through this
service's own Google project and OAuth; email subscribers and buyers from vidrev
(app.vidrev.app), never from PDT.

Order, when there is money and time:
1. Domain on Cloudflare, CNAME to a Railway custom domain on this project.
2. Own GCP project named `ai-agent-in-a-box`: YouTube Data API v3 and YouTube
   Analytics API, OAuth consent screen with the same name, scope
   yt-analytics.readonly (sensitive, no CASA), redirect URI on the domain.
   Own quota and own brand on the Google screen; a problem here never touches
   PDT's verified app.
3. Privacy and Terms on the domain, then Google verification (demo video).
4. Own sign-in (Google) and a database for the analytics rows and the sync.
5. A read API in vidrev for email subscribers and buyers per video.
