"""Builds the animated contributions graph (dark + light) from the GitHub calendar.

Run:  GITHUB_TOKEN=... python assets/make_contrib.py   (locally: token from `gh auth token`)
Output: assets/contrib-dark.svg, assets/contrib-light.svg

Animation: cells appear in a wave once; then every 7 s a light sweep runs over the
active cells and today's cell pulses. Reduced-motion users get a static graph.
"""
import json
import os
import subprocess
import urllib.request
from datetime import date
from pathlib import Path

LOGIN = "AkirraBskyi"
QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  totalContributions weeks{contributionDays{date contributionCount}}}}}}"""

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", muted="#8d96a0", accent="#3fb950", glint="#7ee787",
                 glint_op=.7, levels=["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]),
    "light": dict(bg="#ffffff", border="#d0d7de", muted="#59636e", accent="#1a7f37", glint="#2da44e",
                  glint_op=.6, levels=["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]),
}
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
STEP, SIZE, GY = 15, 12, 42


def token() -> str:
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        return tok
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def fetch() -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def level(v: int) -> int:
    return 0 if v == 0 else 1 if v <= 20 else 2 if v <= 50 else 3 if v <= 100 else 4


def svg(cal: dict, t: dict) -> str:
    weeks = cal["weeks"]
    n = len(weeks)
    gx = (860 - n * STEP + (STEP - SIZE)) / 2
    height = GY + 7 * STEP + 30
    days = [d for w in weeks for d in w["contributionDays"]]
    active = sum(1 for d in days if d["contributionCount"] > 0)
    last = days[-1]["date"]

    cells, glints, ring = [], [], ""
    for i, w in enumerate(weeks):
        for d in w["contributionDays"]:
            row = date.fromisoformat(d["date"]).isoweekday() % 7  # Sunday = 0, as on GitHub
            v = d["contributionCount"]
            x, y = gx + i * STEP, GY + row * STEP
            cells.append(f'<rect class="pop" style="animation-delay:{.15 + i * .028 + row * .012:.3f}s" '
                         f'x="{x:.1f}" y="{y}" width="{SIZE}" height="{SIZE}" rx="2.5" fill="{t["levels"][level(v)]}"/>')
            if v:
                glints.append(f'<rect class="gl" style="animation-delay:{2.4 + i * .03 + row * .01:.3f}s" '
                              f'x="{x:.1f}" y="{y}" width="{SIZE}" height="{SIZE}" rx="2.5" fill="{t["glint"]}"/>')
            if d["date"] == last:
                ring = (f'<rect class="ring" x="{x:.1f}" y="{y}" width="{SIZE}" height="{SIZE}" rx="2.5" '
                        f'fill="none" stroke="{t["levels"][4]}" stroke-width="1.5"/>')

    labels, prev, last_i = [], date.fromisoformat(weeks[0]["contributionDays"][0]["date"]).month, -9
    for i, w in enumerate(weeks):
        m = date.fromisoformat(w["contributionDays"][0]["date"]).month
        if m != prev and i - last_i >= 3 and i < n - 1:
            labels.append(f'<text x="{gx + i * STEP:.1f}" y="{GY + 7 * STEP + 16}" class="m" font-size="10" '
                          f'fill="{t["muted"]}">{MONTHS[m - 1]}</text>')
            last_i = i
        prev = m

    total = cal["totalContributions"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{height}" viewBox="0 0 860 {height}" role="img" aria-label="{total:,} contributions in the last year">
  <style>
    .m {{ font-family: {MONO}; }}
    .soft {{ opacity: 0; animation: soft 1s cubic-bezier(.2,.7,.2,1) forwards; }}
    .pop {{ opacity: 0; transform-box: fill-box; transform-origin: center; animation: pop .5s cubic-bezier(.2,.7,.2,1) forwards; }}
    .gl {{ opacity: 0; animation: gl 7s ease-in-out infinite; }}
    .ring {{ opacity: 0; transform-box: fill-box; transform-origin: center; animation: ring 2.4s ease-out 2s infinite; }}
    @keyframes soft {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes pop {{ from {{ opacity: 0; transform: scale(.4); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes gl {{ 0%, 10%, 100% {{ opacity: 0; }} 5% {{ opacity: {t["glint_op"]}; }} }}
    @keyframes ring {{ 0% {{ opacity: .9; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(2.2); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .soft, .pop {{ animation: none; opacity: 1; transform: none; }}
      .gl, .ring {{ display: none; }}
    }}
  </style>
  <rect x="1" y="1" width="858" height="{height - 2}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>
  <g class="soft">
    <text x="24" y="28" class="m" font-size="12" fill="{t["muted"]}">{total:,} contributions · last 12 months</text>
    <text x="836" y="28" text-anchor="end" class="m" font-size="12" fill="{t["accent"]}">{active} active days</text>
  </g>
  {"".join(cells)}
  {"".join(glints)}
  {ring}
  <g class="soft" style="animation-delay:.45s">{"".join(labels)}</g>
</svg>
"""


if __name__ == "__main__":
    cal = fetch()
    out = Path(__file__).parent
    for name, theme in THEMES.items():
        (out / f"contrib-{name}.svg").write_text(svg(cal, theme), encoding="utf-8")
        print("wrote", out / f"contrib-{name}.svg", "-", cal["totalContributions"], "contributions")
