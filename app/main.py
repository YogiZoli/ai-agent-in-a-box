"""3x AI Agents In A Box: the page moved out of publishing-dreamteam.

Stateless on purpose: no database, no Google sign-in, no stored data. The data
feed from Publishing Dream Team is wired in a later step; until then the page
renders its honest empty state.
"""
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.agents import agent_panels, compounding_line

BASE = Path(__file__).resolve().parent
PDT_URL = os.getenv("PDT_URL", "https://dreamteam.commentclient.com").rstrip("/")

app = FastAPI(title="3x AI Agents In A Box", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
templates = Jinja2Templates(directory=BASE / "templates")
templates.env.globals["asset"] = lambda path: path


@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/")
async def agents_page(request: Request):
    panels = agent_panels({}, {"total": 0, "attributed": 0}, {})
    return templates.TemplateResponse(
        request=request,
        name="agents.html",
        context={
            "pdt_url": PDT_URL,
            "feed_connected": False,
            "channel_title": "",
            "connected": False,
            "granted": False,
            "metrics_agents": True,
            "agents": panels,
            "compounding": compounding_line(panels),
            "subscriber_hook": True,
            "subscribers_total": 0,
            "subscribers_attributed": 0,
        },
    )
