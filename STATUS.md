# STATUS: ai-agent-in-a-box

Updated: 2026-10-07

End goal: the 3x AI Agents page lives here, in its own Railway project, fed by a
read-only internal API of Publishing Dream Team.

Done: the page, its pure panel code and its tests were moved over unchanged. The
page renders its empty state. PDT still serves its own copy and is untouched.

Next: create the Railway project `ai-agent-in-a-box` and deploy (default domain);
then the data feed and sign-in, which Zoltan decides later; then remove the page
from PDT in a separate PR.
