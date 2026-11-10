"""Create original, lightweight SVG product illustrations. No external assets."""

from html import escape
from pathlib import Path

YELLOW = "#ffcc00"
GREEN = "#a8d5b5"
MUTED = "#a4aea6"
ASSETS = Path(__file__).parent / "assets"


def text(x, y, value, size=16, color="#e9eee9", weight=400, anchor="start"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'


def line(x1, y1, x2, y2, color="#485248", dash=False, width=2):
    dash_attr = 'stroke-dasharray="5 7"' if dash else ''
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{width}" fill="none" {dash_attr}/>'


def path(d, color=YELLOW, width=2, dash=False):
    dash_attr = 'stroke-dasharray="5 9"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {dash_attr}/>'


def rect(x, y, w, h, fill="#202720", stroke="#3b463c", radius=14):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def dot(x, y, color=YELLOW, r=5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def card(x, y, w, title, subtitle="", badge="", accent=YELLOW):
    return rect(x, y, w, 86) + dot(x+22, y+27, accent, 4) + text(x+38, y+33, title, 16, weight=600) + text(x+22, y+62, subtitle, 12, MUTED) + (text(x+w-18, y+33, badge, 12, accent, anchor="end") if badge else "")


def brand(x, y, size=100):
    return f'<g transform="translate({x} {y}) scale({size/100})"><rect width="100" height="100" rx="26" fill="{YELLOW}"/>' + path("M31 39 50 50 69 39M50 50V70", "#242b20", 5) + dot(31, 34, "#242b20", 10) + dot(69, 34, "#242b20", 10) + dot(50, 73, "#242b20", 10) + dot(50, 50, "#242b20", 5) + '</g>'


def server(x, y, scale=1, accent=False):
    top = YELLOW if accent else "#55644f"
    return f'<g transform="translate({x} {y}) scale({scale})"><path d="M0 25 65 0 130 25 65 52Z" fill="{top}"/><path d="M0 25 65 52V150L0 123Z" fill="#29332b" stroke="#52604e"/><path d="M65 52 130 25V123L65 150Z" fill="#1b241d" stroke="#52604e"/>' + ''.join(path(f'M12 {y} 52 {y+16}', "#677562", 3) for y in [52, 77, 102]) + ''.join(dot(112, y, YELLOW if accent else GREEN, 3) for y in [55, 79, 103]) + '</g>'


def cylinder(x, y, label="ClickHouse", accent=False):
    c = YELLOW if accent else "#67795e"
    return f'<g transform="translate({x} {y})"><path d="M0 20V116C0 144 150 144 150 116V20" fill="#263126" stroke="{c}" stroke-width="2"/><ellipse cx="75" cy="20" rx="75" ry="24" fill="#37452e" stroke="{c}" stroke-width="2"/>' + path("M0 66C0 94 150 94 150 66", c) + text(75, 115, label, 14, "#edf0e9", 600, "middle") + '</g>'


def save(name, body, title):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 640" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#9eb295" stroke-opacity=".055"/></pattern><radialGradient id="glow"><stop stop-color="#a3b76a" stop-opacity=".13"/><stop offset="1" stop-color="#151b16" stop-opacity="0"/></radialGradient></defs><rect width="960" height="640" fill="#151b16"/><rect width="960" height="640" fill="url(#grid)"/><ellipse cx="480" cy="310" rx="440" ry="290" fill="url(#glow)"/><g font-family="Arial, Helvetica, sans-serif">{body}</g></svg>'''
    (ASSETS / f"{name}.svg").write_text(svg, encoding="utf-8")


def generate():
    ASSETS.mkdir(exist_ok=True)
    rings = ''.join(f'<ellipse cx="480" cy="325" rx="{r}" ry="{r*.62}" fill="none" stroke="#7b8e5b" stroke-opacity=".18" transform="rotate(-15 480 325)"/>' for r in [170, 290, 400])
    fleet = rings + path("M280 175Q440 155 480 300M700 215Q590 220 520 310M340 485Q420 455 480 355", YELLOW, 2, True)
    fleet += server(140, 120, .83) + server(210, 148, .83, True) + text(148, 110, "CLOUD VMs", 13, MUTED, 600)
    fleet += server(650, 130, .68, True) + server(735, 170, .68) + server(650, 240, .68) + text(645, 115, "KUBERNETES", 13, MUTED, 600)
    fleet += server(210, 405, .65) + server(290, 435, .65, True) + text(210, 580, "ON PREMISES", 13, MUTED, 600)
    fleet += '<ellipse cx="500" cy="376" rx="84" ry="22" fill="#080c08" opacity=".55"/>' + brand(444, 270, 110) + text(500, 414, "NEXORA", 16, YELLOW, 700, "middle")
    fleet += card(565, 443, 255, "Fleet connected", "One operational context", "↗", GREEN) + dot(317, 194) + dot(650, 237) + dot(377, 475)
    save("fleet-orbit", fleet, "Cloud, Kubernetes and on-premises clusters connected to Nexora")

    nodes = [(65, 105, "OBSERVABILITY", "Metrics · queries · logs"), (605, 105, "INTELLIGENCE", "Assistant · advisors · scans"), (65, 405, "DATA WORK", "SQL · schedules · health"), (605, 405, "OPERATIONS", "Backups · deploys · support")]
    body = ''.join(path(f'M{x+145} {y+43}Q480 {y+43} 480 300', "#657650", 2, True) + card(x, y, 290, title, subtitle) for x, y, title, subtitle in nodes)
    body += brand(430, 250) + text(480, 390, "ONE CLUSTER CONTEXT", 15, YELLOW, 600, "middle") + rect(280, 545, 400, 46) + text(480, 575, "IDENTITY / ACCESS / AUDIT", 13, MUTED, 600, "middle")
    save("platform-map", body, "Nexora platform capability map")

    body = card(225, 55, 510, "Why is this cluster under pressure?", "A question in the context of your ClickHouse fleet", "?")
    body += path("M480 141V205M220 205H740M220 205V250M480 205V250M740 205V250", "#74875c", 2, True)
    for x, title, subtitle in [(80, "Cluster health", "Topology & node vitals"), (340, "Query evidence", "Memory & execution"), (600, "Documentation", "Configured source snapshots")]:
        body += card(x, 250, 240, title, subtitle, "✓", GREEN)
    body += path("M200 336V395H720V336M460 395V450", YELLOW, 2, True) + rect(225, 450, 510, 125, "#2a321c", "#73804a")
    body += brand(247, 474, 54) + text(326, 489, "Evidence → explanation → next step", 18, YELLOW, 600) + text(326, 522, "An operator reviews the recommendation.", 14, MUTED) + text(326, 549, "ILLUSTRATIVE INVESTIGATION", 11, MUTED)
    save("ai-investigation", body, "A question becomes an evidence-based investigation")

    body = card(330, 45, 300, "production-analytics", "2 shards / 3 replicas each", "●", GREEN)
    body += path("M480 131V190M235 190H725M235 190V250M725 190V250", YELLOW, 2, True)
    for x, title in [(90, "SHARD 01"), (580, "SHARD 02")]:
        body += rect(x, 240, 290, 300, "#1a221b", "#46543e") + text(x+145, 278, title, 14, MUTED, 600, "middle")
        for j in range(3):
            body += rect(x+25, 305+j*65, 240, 45, "#263025") + dot(x+47, 328+j*65, GREEN, 4) + text(x+65, 334+j*65, f"replica-{j+1:02d}", 15) + text(x+245, 334+j*65, "●", 12, GREEN, anchor="end")
    body += text(480, 596, "TOPOLOGY / VITALS / LOGS / HEALTH", 13, YELLOW, 600, "middle")
    save("topology", body, "Two ClickHouse shards, each with three replicas")

    body = rect(80, 85, 800, 460, "#1c241d") + text(115, 126, "SYSTEM SIGNALS", 13, MUTED, 600)
    body += card(115, 155, 215, "Queries", "Live & historical", "↗") + card(350, 155, 215, "Resources", "Database & host", "⌁", GREEN) + card(585, 155, 260, "Storage", "Parts & replication", "▱")
    for y, col in [(315, YELLOW), (405, GREEN)]:
        body += line(115, y+44, 845, y+44, "#364234", True)
        body += path(f'M115 {y+30} 145 {y+15} 175 {y+30} 205 {y} 235 {y+10} 265 {y-12} 295 {y+8} 325 {y-5} 355 {y+20} 385 {y-22} 415 {y-10} 445 {y+5} 475 {y-7} 505 {y-25} 535 {y-10} 565 {y-32} 595 {y-15} 625 {y-20} 655 {y+2} 685 {y-18} 715 {y-8} 745 {y-25} 775 {y-12} 805 {y-22} 845 {y-20}', col, 3)
    body += text(115, 508, "FROM A FLEET SIGNAL TO THE INDIVIDUAL QUERY", 13, MUTED)
    save("observability", body, "ClickHouse operational signals in one view")

    body = ''
    for i, (label, col) in enumerate([("QUERY ACTIVITY", YELLOW), ("HOST MEMORY", GREEN), ("DISK PRESSURE", "#b4bfeb")]):
        y = 65+i*170
        body += rect(70, y, 820, 145) + text(95, y+30, label, 12, MUTED, 600)
        body += ''.join(line(95, y+t, 865, y+t, "#303b30", True, 1) for t in [60, 100, 125])
        body += path(f'M95 {y+115} 140 {y+95} 185 {y+100} 230 {y+82} 275 {y+90} 320 {y+70} 365 {y+80} 410 {y+45+i*7} 455 {y+78} 500 {y+60} 545 {y+65} 590 {y+55} 635 {y+72} 680 {y+45} 725 {y+58} 770 {y+40} 815 {y+48} 865 {y+30}', col, 3)
    save("metrics", body, "Illustrative query, memory and disk time series")

    body = brand(150, 270, 100) + text(200, 415, "NEXORA AI", 14, YELLOW, 600, "middle") + path("M250 320H440M440 145V495M440 145H590M440 320H590M440 495H590", "#6b8053", 2, True)
    for y, title, subtitle in [(100, "Cloud providers", "Configured credentials & models"), (275, "Compatible endpoints", "Your chosen model server"), (450, "Local models", "Ollama / operator-supplied models")]:
        body += card(590, y, 300, title, subtitle, "↗")
    save("model-router", body, "Choose cloud, compatible endpoints or local model providers")

    body = rect(65, 80, 420, 250, "#202820") + text(94, 120, "QUERY.SQL", 13, MUTED, 600)
    body += text(94, 174, "SELECT event_type, count()", 22, YELLOW) + text(94, 215, "FROM analytics.events", 20) + text(94, 256, "GROUP BY event_type;", 20)
    body += path("M485 205H630V375H730", YELLOW, 2, True) + rect(560, 110, 300, 160) + text(590, 149, "EXECUTION PLAN", 13, MUTED, 600)
    body += text(590, 190, "Read → Filter → Aggregate", 16) + text(590, 230, "Inspect the work behind SQL", 13, MUTED)
    body += rect(330, 390, 530, 175) + text(360, 428, "RESULTS", 13, MUTED, 600)
    for j, (a, b) in enumerate([("page_view", "12,841"), ("purchase", "1,208"), ("signup", "486")]):
        body += line(360, 451+j*35, 830, 451+j*35, "#384535", False, 1) + text(360, 477+j*35, a, 15) + text(830, 477+j*35, b, 15, YELLOW, anchor="end")
    body += text(80, 535, "ILLUSTRATIVE", 12, MUTED) + text(80, 557, "SQL WORKFLOW", 12, MUTED)
    save("query-path", body, "SQL exploration, execution planning and example results")

    body = cylinder(50, 255, "Dataset") + path("M200 320H310M650 320H780", YELLOW, 2, True)
    for i, (title, subtitle) in enumerate([("Freshness", "Is the dataset up to date?"), ("Completeness", "Are expected values present?"), ("Schema", "Does the contract still hold?")]):
        body += card(310, 100+i*155, 340, title, subtitle, "✓", GREEN)
    body += rect(775, 260, 140, 120, "#2a3524", "#6c8756") + text(845, 310, "✓", 34, GREEN, 600, "middle") + text(845, 346, "Healthy", 15, GREEN, 600, "middle")
    save("data-health", body, "Dataset health checks for freshness, completeness and schema")

    body = cylinder(70, 245) + path("M220 310H340M340 160V460M340 160H450M340 460H450", YELLOW, 2, True)
    body += card(450, 115, 260, "Full backup", "The recovery baseline", "01") + card(450, 415, 260, "Incremental", "Changes in the chain", "+")
    body += path("M710 158H795V455H710", GREEN, 2, True) + rect(740, 250, 160, 110, "#273323", "#6c8252") + text(820, 295, "STORAGE", 14, YELLOW, 600, "middle") + text(820, 328, "Your destination", 12, MUTED, anchor="middle")
    body += path("M800 505V565H145V400", "#91a8a4", 2, True) + text(470, 594, "RESTORE / RECOVERY WORKFLOW", 13, MUTED, 600, "middle")
    save("backup-flow", body, "Full and incremental backup chains with a restore path")

    body = '<circle cx="480" cy="320" r="205" fill="none" stroke="#506141" stroke-width="2" stroke-dasharray="6 10"/>' + brand(430, 270)
    for x, y, title, subtitle in [(90, 120, "Observe", "Health & telemetry"), (590, 120, "Plan", "Review & prechecks"), (590, 435, "Execute", "Supported workflows"), (90, 435, "Review", "Tasks & history")]:
        body += card(x, y, 280, title, subtitle)
    save("operations-cycle", body, "Observe, plan, execute and review the operational workflow")

    body = path("M130 335H830", "#687b4f", 3, True)
    for i, (title, subtitle) in enumerate([("Analyze", "Version options"), ("Precheck", "Environment checks"), ("Review", "Operator decision"), ("Record", "Plan & maintenance")]):
        x = 55+i*225
        body += rect(x, 230, 190, 190) + dot(x+95, 230, YELLOW, 8) + text(x+95, 286, f"0{i+1}", 34, YELLOW, 600, "middle") + text(x+95, 335, title, 20, weight=600, anchor="middle") + text(x+95, 375, subtitle, 12, MUTED, anchor="middle")
    body += text(480, 490, "A CLEAR PATH THROUGH THE CHANGE", 14, MUTED, 600, "middle")
    save("upgrade-path", body, "Upgrade analysis, prechecks, operator review and maintenance planning")

    body = card(65, 100, 300, "Cluster context", "Health · logs · query evidence", "◫") + card(65, 420, 300, "Support bundle", "Downloadable diagnostics", "↓")
    body += path("M365 143H450V320H550M365 463H450V320", YELLOW, 2, True) + rect(550, 150, 330, 340)
    body += text(580, 195, "SUPPORT CASE", 13, MUTED, 600) + text(580, 242, "Context stays with the work.", 18, YELLOW, 600)
    for y, label in [(295, "Priority & assignment"), (350, "Comments & attachments"), (405, "Status & target tracking")]:
        body += dot(585, y-5, GREEN, 4) + text(604, y, label, 15)
    save("support-workflow", body, "Cluster evidence and support bundles connect to a support case")

    body = ''
    for i, (label, fill, stroke) in enumerate([("IDENTITY", "#1c241c", "#46553b"), ("ROLES & PERMISSIONS", "#243020", "#607348"), ("CLUSTER ACCESS", "#2b3823", "#8b9d53"), ("DATA POLICIES", "#374321", YELLOW)]):
        x, y = 100+i*80, 65+i*67
        body += rect(x, y, 760-i*160, 490-i*118, fill, stroke, 25) + text(x+25, y+39, label, 13, MUTED if i<3 else YELLOW, 600)
    body += brand(444, 342, 72) + text(480, 593, "EXPLICIT ACCESS / SHARED WORKSPACE", 14, MUTED, 600, "middle")
    save("security-layers", body, "Identity, roles, cluster access and data policies form access boundaries")

    body = card(70, 260, 240, "Invited user", "An existing Nexora account", "01") + card(365, 260, 250, "Identity provider", "OIDC / OAuth2 / SAML / LDAP", "02") + card(670, 260, 230, "Scoped access", "Roles & cluster permissions", "03")
    body += path("M310 303H365M615 303H670", YELLOW, 2, True) + brand(442, 90, 76) + text(480, 485, "ONE CONFIGURED PROVIDER / INVITE-ONLY SIGN-IN", 14, MUTED, 600, "middle")
    save("identity-flow", body, "Invite-only SSO connects a user to scoped platform access")

    body = card(50, 100, 270, "MCP client", "Cursor / Claude Desktop", "↗") + card(50, 420, 270, "Nexora AI", "Cluster-aware assistant", "✳")
    body += path("M320 143H400V320H480M320 463H400V320M580 320H700", YELLOW, 2, True) + brand(480, 270) + text(530, 420, "SESSION + PERMISSIONS", 12, YELLOW, 600, "middle")
    body += rect(700, 175, 210, 290)
    for i, label in enumerate(["Cluster health", "Query diagnostics", "System tables", "Documentation"]):
        body += dot(725, 223+i*65, GREEN, 4) + text(743, 229+i*65, label, 14)
    save("mcp-network", body, "Authenticated clients access Nexora diagnostic tools through the API")

    body = brand(430, 270) + '<circle cx="480" cy="320" r="210" fill="none" stroke="#526643" stroke-dasharray="4 8"/>'
    for x, y, title, subtitle, dx, dy in [(345, 35, "Metrics", "Prometheus / node_exporter", 480, 121), (45, 180, "Identity", "Your SSO provider", 320, 223), (45, 400, "Storage", "Your backup destinations", 320, 443), (640, 180, "AI providers", "Cloud / compatible / local", 640, 223), (640, 400, "Notifications", "Your team channels", 640, 443), (345, 520, "MCP clients", "Session-scoped tools", 480, 520)]:
        body += path(f'M480 320L{dx} {dy}', "#566c44", 2, True) + card(x, y, 275, title, subtitle)
    save("integration-hub", body, "The integration ecosystem around Nexora")

    body = path("M480 150V250M220 250H740M220 250V340M480 250V340M740 250V340", YELLOW, 2, True) + brand(438, 60, 84)
    for x, title, subtitle in [(85, "CLOUD VMs", "AWS / Azure / GCP"), (345, "KUBERNETES", "Configured providers"), (605, "ON PREMISES", "Prepared Linux VMs")]:
        body += rect(x, 340, 270, 230, "#20291f", "#536547") + server(x+78, 365, .85, True) + text(x+135, 525, title, 14, YELLOW, 600, "middle") + text(x+135, 552, subtitle, 13, MUTED, anchor="middle")
    save("deployment-landscape", body, "Cloud, Kubernetes and on-premises deployment environments")

    body = rect(90, 70, 780, 500, "#19221a", "#5a7350", 30) + text(125, 115, "KUBERNETES / CONFIGURED PROVIDER", 15, GREEN, 600) + brand(438, 135, 84)
    body += path("M480 219V285M260 285H700M260 285V345M700 285V345", YELLOW, 2, True)
    for x in [180, 620]:
        body += server(x, 350, .65, True) + server(x+85, 380, .65) + text(x+85, 530, "SHARD / REPLICAS", 12, MUTED, anchor="middle")
    save("kubernetes", body, "Kubernetes deployment provider with shards and replicas")

    body = brand(435, 65, 90) + path("M480 155V235M205 235H755M205 235V330M480 235V330M755 235V330", YELLOW, 2, True)
    for i, x in enumerate([100, 375, 650], 1):
        body += rect(x, 330, 210, 230) + server(x+40, 355, .85, i==2) + text(x+105, 520, f"LINUX VM 0{i}", 13, MUTED, 600, "middle") + dot(x+57, 546, GREEN, 4) + text(x+72, 550, "Agent enrolled", 12, GREEN)
    body += text(480, 285, "HTTPS NODE AGENTS / READINESS CHECKS", 12, MUTED, 600, "middle")
    save("onprem", body, "Prepared on-premises Linux VMs with enrolled HTTPS node agents")

    body = path("M190 320H770", "#607544", 2, True)
    for i, (x, title, sub) in enumerate([(80, "Install", "Docker / Helm"), (365, "Connect", "ClickHouse endpoint"), (650, "Explore", "Your operations workspace")], 1):
        body += rect(x, 170, 230, 300) + text(x+25, 215, f"0{i}", 14, MUTED) + (brand(x+76, 245, 76) if i==1 else cylinder(x+55, 255, "Cluster") if i==2 else server(x+62, 240, .8, True)) + text(x+115, 413, title, 23, YELLOW, 600, "middle") + text(x+115, 447, sub, 12, MUTED, anchor="middle")
    save("getting-started", body, "Install Nexora, connect ClickHouse and explore the workspace")


if __name__ == "__main__":
    generate()
    print(f"Generated {len(list(ASSETS.glob('*.svg'))) - 1} original SVG illustrations.")
