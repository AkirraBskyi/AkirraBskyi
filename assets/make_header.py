"""Generates the animated profile header panel (dark + light).

Run:  python assets/make_header.py
Output: assets/header-dark.svg, assets/header-light.svg
"""
from pathlib import Path

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", text="#e6edf3", muted="#8d96a0",
                 chip="#161b22", track="#21262d", blue="#58a6ff", green="#3fb950",
                 purple="#a371f7"),
    "light": dict(bg="#ffffff", border="#d0d7de", text="#1f2328", muted="#59636e",
                  chip="#f6f8fa", track="#eaeef2", blue="#0969da", green="#1a7f37",
                  purple="#8250df"),
}

CHIPS = [
    ("Valuation &amp; modelling", "DCF · 3-statement · WACC", "blue"),
    ("Quant research", "backtests · VaR · Black-Litterman", "green"),
    ("AI for markets", "Claude skills &amp; agents", "purple"),
]

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"


def svg(t: dict) -> str:
    chips = []
    for i, (title, sub, color) in enumerate(CHIPS):
        x = 28 + i * 274
        delay = 2.05 + i * 0.15
        chips.append(f"""
  <g class="f" style="animation-delay:{delay:.2f}s">
    <rect x="{x}" y="172" width="256" height="46" rx="10" fill="{t['chip']}" stroke="{t['border']}"/>
    <rect x="{x}" y="184" width="3" height="22" rx="1.5" fill="{t[color]}"/>
    <text x="{x + 16}" y="191" class="sans" font-size="13" font-weight="600" fill="{t['text']}">{title}</text>
    <text x="{x + 16}" y="208" class="mono" font-size="11" fill="{t['muted']}">{sub}</text>
  </g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="234" viewBox="0 0 860 234" role="img" aria-label="Kyrylo Bichkovskyi — Finance · Quant research · AI tools for markets">
  <defs>
    <linearGradient id="bar" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="{t['blue']}"/>
      <stop offset="1" stop-color="{t['purple']}"/>
    </linearGradient>
  </defs>
  <style>
    .sans {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; }}
    .f {{ opacity: 0; animation: rise .6s cubic-bezier(.2,.7,.2,1) forwards; }}
    .grow {{ transform-box: fill-box; transform-origin: left center; transform: scaleX(0);
             animation: grow 1.4s cubic-bezier(.65,0,.35,1) .6s forwards; }}
    .out {{ animation: fadeout .3s ease 2s forwards; }}
    .pulse {{ animation: pulse 2.4s ease-in-out 2.6s infinite; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes grow {{ to {{ transform: scaleX(1); }} }}
    @keyframes fadeout {{ to {{ opacity: 0; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .f, .grow, .out, .pulse {{ animation: none; opacity: 1; transform: none; }}
      .out {{ opacity: 0; }}
    }}
  </style>

  <rect x="1" y="1" width="858" height="232" rx="14" fill="{t['bg']}" stroke="{t['border']}"/>

  <g class="f">
    <circle cx="24" cy="22" r="5.5" fill="#ff5f57"/>
    <circle cx="42" cy="22" r="5.5" fill="#febc2e"/>
    <circle cx="60" cy="22" r="5.5" fill="#28c840"/>
    <text x="82" y="26" class="mono" font-size="12" fill="{t['muted']}">~/AkirraBskyi</text>
    <circle class="pulse" cx="752" cy="22" r="4" fill="{t['green']}"/>
    <text x="764" y="26" class="mono" font-size="12" fill="{t['muted']}">Wrocław · PL</text>
    <line x1="1" y1="41" x2="859" y2="41" stroke="{t['border']}"/>
  </g>

  <g class="f" style="animation-delay:.15s">
    <text x="28" y="88" class="sans" font-size="32" font-weight="700" fill="{t['text']}">Kyrylo Bichkovskyi</text>
  </g>
  <g class="f" style="animation-delay:.3s">
    <text x="28" y="115" class="mono" font-size="14" fill="{t['blue']}">finance · quant research · AI tools for markets</text>
  </g>
  <g class="f" style="animation-delay:.45s">
    <text x="28" y="138" class="sans" font-size="13" fill="{t['muted']}">BBA Finance @ University of Wrocław</text>
  </g>

  <g class="f" style="animation-delay:.55s">
    <rect x="28" y="154" width="804" height="4" rx="2" fill="{t['track']}"/>
  </g>
  <rect class="grow" x="28" y="154" width="804" height="4" rx="2" fill="url(#bar)"/>
  <g class="f" style="animation-delay:.6s"><g class="out">
    <text x="832" y="138" text-anchor="end" class="mono" font-size="11" fill="{t['muted']}">loading profile…</text>
  </g></g>
  <g class="f" style="animation-delay:2.05s">
    <text x="832" y="138" text-anchor="end" class="mono" font-size="11" fill="{t['green']}">ready ✓</text>
  </g>
{''.join(chips)}
</svg>
"""


if __name__ == "__main__":
    out = Path(__file__).parent
    for name, theme in THEMES.items():
        (out / f"header-{name}.svg").write_text(svg(theme), encoding="utf-8")
        print("wrote", out / f"header-{name}.svg")
