"""Generates the animated profile banner (dark + light).

Run:  python assets/make_header.py
Output: assets/header-dark.svg, assets/header-light.svg
The banner keeps its own colours; only the waves at the bottom take the page
background, so each theme gets its own file.
"""
from pathlib import Path

NAME = "Kyrylo Bichkovskyi"
TAGLINE = "finance · quant research · AI tools for markets"
SUBLINE = "BBA Finance @ University of Wrocław · Wrocław · PL"

# gradient: deep -> accent (green) -> second accent (blue)
THEMES = {
    "dark": dict(page="#0d1117", deep="#0a1a33"),
    "light": dict(page="#ffffff", deep="#0b2a5b"),
}
ACCENT, ACCENT2 = "#1a7f37", "#0969da"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
H = 196


def wave(y: int, amp: int, fill: str, opacity: float, dur: int, reverse: bool) -> str:
    """Sine-like wave, 2 periods wider than the banner, sliding by one period (430px)."""
    d = f"M0 {y} q107.5 {-amp} 215 0" + " t215 0" * 7 + f" V{H} H0 Z"
    cls = "wv rv" if reverse else "wv"
    return f'<path class="{cls}" style="animation-duration:{dur}s" d="{d}" fill="{fill}" opacity="{opacity}"/>'


def svg(t: dict) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{H}" viewBox="0 0 860 {H}" role="img" aria-label="{NAME} — {TAGLINE}">
  <defs>
    <linearGradient id="bn" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="{t['deep']}"/>
      <stop offset=".6" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT2}"/>
    </linearGradient>
    <radialGradient id="gl">
      <stop offset="0" stop-color="#fff" stop-opacity=".22"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="cb"><rect x="1" y="1" width="858" height="{H - 2}" rx="14"/></clipPath>
  </defs>
  <style>
    .s {{ font-family: {SANS}; }}
    .m {{ font-family: {MONO}; }}
    .soft {{ opacity: 0; animation: soft 1.1s cubic-bezier(.2,.7,.2,1) forwards; }}
    .wv {{ animation-name: wv; animation-timing-function: linear; animation-iteration-count: infinite; }}
    .rv {{ animation-direction: reverse; }}
    .glow {{ animation: glow 9s ease-in-out infinite alternate; }}
    @keyframes soft {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes wv {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-430px); }} }}
    @keyframes glow {{ from {{ transform: translateX(-240px); }} to {{ transform: translateX(240px); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .soft {{ animation: none; opacity: 1; transform: none; }}
      .wv, .glow {{ animation: none; }}
    }}
  </style>

  <g clip-path="url(#cb)">
    <rect width="860" height="{H}" fill="url(#bn)"/>
    <circle class="glow" cx="430" cy="40" r="280" fill="url(#gl)"/>
    {wave(H - 44, 9, t['page'], .35, 16, True)}
    {wave(H - 32, 11, t['page'], 1, 11, False)}
  </g>

  <g class="soft" style="animation-delay:.1s">
    <text x="430" y="76" text-anchor="middle" class="s" font-size="40" font-weight="700" fill="#fff">{NAME}</text>
  </g>
  <g class="soft" style="animation-delay:.3s">
    <text x="430" y="104" text-anchor="middle" class="m" font-size="15" fill="#fff" fill-opacity=".92">{TAGLINE}</text>
  </g>
  <g class="soft" style="animation-delay:.45s">
    <text x="430" y="126" text-anchor="middle" class="s" font-size="13" fill="#fff" fill-opacity=".75">{SUBLINE}</text>
  </g>
</svg>
"""


if __name__ == "__main__":
    out = Path(__file__).parent
    for name, theme in THEMES.items():
        (out / f"header-{name}.svg").write_text(svg(theme), encoding="utf-8")
        print("wrote", out / f"header-{name}.svg")
