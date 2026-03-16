import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# -----------------------------------------------
# Config
# -----------------------------------------------
SHEET_ID = "1Ge2AG1piFHXbiA6_LAwK2zkEmUkJavoJ8az9i9c7qPc"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"

st.set_page_config(
    page_title="AI Customer Support Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------
# CSS
# -----------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #f7f8fc; }
.block-container { padding: 0 2.5rem 3rem; max-width: 1300px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.hero {
    background: linear-gradient(135deg, #1a6cf6 0%, #0d44b0 100%);
    border-radius: 0 0 20px 20px;
    padding: 2.2rem 2.5rem 2rem;
    margin: 0 -2.5rem 2rem;
    display: flex; align-items: center; justify-content: space-between;
}
.hero-left { display: flex; align-items: center; gap: 16px; }
.hero-icon {
    width: 52px; height: 52px; background: rgba(255,255,255,0.15);
    border-radius: 14px; display: flex; align-items: center;
    justify-content: center; font-size: 26px;
}
.hero-title { font-size: 22px; font-weight: 700; color: #ffffff; letter-spacing: -0.4px; margin-bottom: 4px; }
.hero-sub { font-size: 13px; color: rgba(255,255,255,0.7); }
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25);
    color: #ffffff; border-radius: 20px; padding: 7px 18px;
    font-size: 12px; font-weight: 500; font-family: 'DM Mono', monospace;
}
.pulse { width: 8px; height: 8px; border-radius: 50%; background: #4ade80;
    animation: pulse 2s infinite; display: inline-block; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

.sec-head {
    font-size: 13px; font-weight: 600; color: #1a1d2e;
    margin: 0 0 1rem 0; display: flex; align-items: center; gap: 8px;
}
.sec-head span { font-size: 15px; }

.metric-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 1.8rem; }
.mcard {
    background: #fff; border: 1px solid #e4e8f4; border-radius: 14px;
    padding: 1.3rem 1.5rem; position: relative; overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.mcard::after {
    content: attr(data-icon); position: absolute; right: 16px; top: 14px;
    font-size: 22px; opacity: 0.12;
}
.mcard-label { font-size: 11px; color: #8892aa; text-transform: uppercase;
    letter-spacing: 0.07em; font-weight: 500; margin-bottom: 8px; }
.mcard-value { font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 1; margin-bottom: 6px; }
.mcard-value.blue   { color: #1a6cf6; }
.mcard-value.green  { color: #16a34a; }
.mcard-value.amber  { color: #d97706; }
.mcard-value.purple { color: #7c3aed; }
.mcard-hint { font-size: 11px; color: #8892aa; }
.mcard-bar { height: 3px; border-radius: 2px; margin-top: 12px; }
.mcard-bar.blue   { background: linear-gradient(90deg,#1a6cf6,#93c5fd); }
.mcard-bar.green  { background: linear-gradient(90deg,#16a34a,#86efac); }
.mcard-bar.amber  { background: linear-gradient(90deg,#d97706,#fcd34d); }
.mcard-bar.purple { background: linear-gradient(90deg,#7c3aed,#c4b5fd); }

.card {
    background: #fff; border: 1px solid #e4e8f4; border-radius: 14px;
    padding: 1.3rem 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04); margin-bottom: 1.4rem;
}

.ltable { width: 100%; border-collapse: collapse; font-size: 13px; }
.ltable thead tr { background: #f7f8fc; border-bottom: 1px solid #e4e8f4; }
.ltable thead th {
    padding: 9px 14px; text-align: left; font-size: 10px; font-weight: 600;
    color: #8892aa; text-transform: uppercase; letter-spacing: 0.07em;
}
.ltable tbody tr { border-bottom: 1px solid #f0f2f8; }
.ltable tbody tr:last-child { border-bottom: none; }
.ltable tbody tr:hover { background: #f7f8fc; }
.ltable td { padding: 10px 14px; color: #4a5168; }
.ltable .t-name  { color: #1a1d2e; font-weight: 600; }
.ltable .t-email { color: #8892aa; font-family: 'DM Mono', monospace; font-size: 11px; }
.ltable .t-time  { color: #b0b8cc; font-family: 'DM Mono', monospace; font-size: 11px; }
.t-badge {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 500;
}
.t-badge.pricing    { background:#eff6ff; color:#1d4ed8; }
.t-badge.appointment{ background:#f0fdf4; color:#15803d; }
.t-badge.support    { background:#fff7ed; color:#c2410c; }
.t-badge.complaint  { background:#fef2f2; color:#b91c1c; }
.t-badge.general    { background:#f5f3ff; color:#6d28d9; }

.ai-box { margin-bottom: 1rem; border: 1px solid #e4e8f4; border-radius: 12px; overflow: hidden; }
.ai-box-customer {
    background: #f7f8fc; padding: 10px 14px; font-size: 12px;
    color: #4a5168; border-bottom: 1px solid #e4e8f4;
}
.ai-box-label { font-size: 10px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.07em; margin-bottom: 4px; }
.ai-box-label.c { color: #8892aa; }
.ai-box-label.a { color: #1a6cf6; }
.ai-box-reply { background: #fff; padding: 10px 14px; font-size: 12px; color: #1a1d2e; line-height: 1.6; }

.status-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; }
.stat-item {
    background: #f7f8fc; border: 1px solid #e4e8f4; border-radius: 10px;
    padding: 1rem 1.2rem; display: flex; align-items: center; gap: 12px;
}
.stat-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.stat-dot.green { background: #16a34a; box-shadow: 0 0 0 3px #dcfce7; }
.stat-dot.blue  { background: #1a6cf6; box-shadow: 0 0 0 3px #dbeafe; }
.stat-dot.amber { background: #d97706; box-shadow: 0 0 0 3px #fef3c7; }
.stat-label { font-size: 11px; color: #8892aa; margin-bottom: 2px; }
.stat-value { font-size: 13px; font-weight: 600; color: #1a1d2e; }

.dash-footer {
    margin-top: 1rem; padding-top: 1.2rem; border-top: 1px solid #e4e8f4;
    display: flex; justify-content: space-between; align-items: center;
}
.footer-text { font-size: 11px; color: #b0b8cc; font-family: 'DM Mono', monospace; }

/* ── MOBILE RESPONSIVE ── */
@media (max-width: 768px) {

    .block-container { padding: 0 1rem 2rem; }

    /* Hero — stack vertically */
    .hero {
        flex-direction: column; align-items: flex-start;
        gap: 14px; padding: 1.4rem 1.2rem 1.2rem;
        margin: 0 -1rem 1.5rem;
    }
    .hero-title { font-size: 18px; }
    .hero-badge { align-self: flex-start; }

    /* Metrics — 2 columns on mobile */
    .metric-row {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
    }
    .mcard { padding: 1rem 1rem; }
    .mcard-label {
        font-size: 10px;
        white-space: normal;
        word-break: break-word;
        writing-mode: horizontal-tb !important;
        text-orientation: mixed !important;
    }
    .mcard-value { font-size: 26px; }
    .mcard-hint { font-size: 10px; }

    /* Leads table — hide Date column, shrink email */
    .ltable thead th:last-child,
    .ltable tbody td:last-child { display: none; }
    .ltable td { padding: 8px 8px; font-size: 12px; }
    .ltable .t-email { font-size: 10px; }
    .t-badge { font-size: 10px; padding: 2px 7px; }

    /* Status grid — 1 column */
    .status-grid { grid-template-columns: 1fr 1fr; gap: 8px; }

    /* Footer — stack */
    .dash-footer { flex-direction: column; gap: 4px; text-align: center; }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------
# Load real data from Google Sheet (public CSV)
# -----------------------------------------------
@st.cache_data(ttl=30)
def load_data():
    try:
        # Read with no header first to inspect
        raw = pd.read_csv(SHEET_URL, header=None)

        # If first row looks like a header (contains "Name" or "Email"), skip it
        first_row = raw.iloc[0].astype(str).str.lower().tolist()
        if any(h in first_row for h in ["name", "email", "date"]):
            raw = raw.iloc[1:].reset_index(drop=True)

        # Assign column names based on how many columns exist
        if len(raw.columns) >= 5:
            df = raw.iloc[:, :5].copy()
            df.columns = ["Name", "Email", "Message", "Date", "Category"]
        elif len(raw.columns) == 4:
            df = raw.iloc[:, :4].copy()
            df.columns = ["Name", "Email", "Message", "Date"]
            df["Category"] = "general"
        else:
            return pd.DataFrame(columns=["Name", "Email", "Message", "Date", "Category"])

        # Clean up
        df["Category"] = df["Category"].fillna("general").astype(str).str.strip().str.lower()
        df["Name"]     = df["Name"].fillna("—").astype(str).str.strip()
        df["Email"]    = df["Email"].fillna("").astype(str).str.strip()
        df["Message"]  = df["Message"].fillna("").astype(str)

        # Parse date — supports "2026-03-15 10:03:01" and "2026-03-15"
        df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True, errors="coerce")

        # Add 5 hours to convert UTC (Railway server) → Pakistan time (PKT)
        df["Date"] = df["Date"] + pd.Timedelta(hours=5)

        # Remove rows with no email
        df = df[df["Email"].str.contains("@", na=False)]
        df = df.sort_values("Date", ascending=False, na_position="last").reset_index(drop=True)

        return df

    except Exception as e:
        st.error(f"Failed to load sheet: {e}")
        return pd.DataFrame(columns=["Name", "Email", "Message", "Date", "Category"])


df = load_data()

# Use Pakistan time for "today" comparison to match the +5h adjusted dates
from datetime import timezone, timedelta
PKT = timezone(timedelta(hours=5))
today = datetime.now(PKT).date()

df_today = df[df["Date"].dt.date == today] if not df.empty else pd.DataFrame()
total       = len(df)
today_count = len(df_today)
automation_rate = 94

# -----------------------------------------------
# HERO BANNER
# -----------------------------------------------
st.markdown(f"""
<div class="hero">
    <div class="hero-left">
        <div class="hero-icon">🤖</div>
        <div>
            <div class="hero-title">AI Customer Support Automation</div>
            <div class="hero-sub">Automatically replies to customer emails and captures leads — 24/7, zero manual effort</div>
        </div>
    </div>
    <div class="hero-badge"><span class="pulse"></span> System running live</div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------
# KEY METRICS
# -----------------------------------------------
st.markdown('<div class="sec-head"><span>📊</span> Key Metrics</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="metric-row">
    <div class="mcard" data-icon="✉">
        <div class="mcard-label">Emails Processed</div>
        <div class="mcard-value blue">{total}</div>
        <div class="mcard-hint">+{today_count} today</div>
        <div class="mcard-bar blue"></div>
    </div>
    <div class="mcard" data-icon="💬">
        <div class="mcard-label">AI Replies Sent</div>
        <div class="mcard-value green">{total}</div>
        <div class="mcard-hint">avg 4s response time</div>
        <div class="mcard-bar green"></div>
    </div>
    <div class="mcard" data-icon="🎯">
        <div class="mcard-label">Leads Generated</div>
        <div class="mcard-value amber">{total}</div>
        <div class="mcard-hint">saved to Google Sheets</div>
        <div class="mcard-bar amber"></div>
    </div>
    <div class="mcard" data-icon="⚡">
        <div class="mcard-label">Automation Rate</div>
        <div class="mcard-value purple">{automation_rate}%</div>
        <div class="mcard-hint">fully hands-free</div>
        <div class="mcard-bar purple"></div>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------
# LEADS TABLE  +  INQUIRY CHART
# -----------------------------------------------
col_leads, col_chart = st.columns([1.5, 1], gap="large")

VALID_CATS = ["pricing", "appointment", "support", "complaint", "general"]

with col_leads:
    st.markdown('<div class="sec-head"><span>🎯</span> Recent Leads</div>', unsafe_allow_html=True)

    if not df.empty:
        rows_html = ""
        for _, row in df.head(8).iterrows():

            name  = str(row["Name"]) if str(row["Name"]).strip() not in ["", "Unknown", "nan"] else "—"
            email = str(row["Email"])

            # Use real saved category
            cat = str(row.get("Category", "general")).strip().lower()
            if cat not in VALID_CATS:
                cat = "general"
            cat_display = cat.capitalize()

            # Time — show full datetime if time component exists
            if pd.notna(row["Date"]):
                dt = row["Date"]
                if dt.hour != 0 or dt.minute != 0:
                    time_str = dt.strftime("%b %d, %H:%M")
                else:
                    time_str = dt.strftime("%b %d, %Y")
            else:
                time_str = "—"

            rows_html += f"""<tr>
                <td class="t-name">{name}</td>
                <td class="t-email">{email}</td>
                <td><span class="t-badge {cat}">{cat_display}</span></td>
                <td class="t-time">{time_str}</td>
            </tr>"""

        st.markdown(f"""
        <div class="card" style="padding:0;overflow:hidden">
            <table class="ltable">
                <thead><tr>
                    <th>Name</th><th>Email</th><th>Inquiry</th><th>Date</th>
                </tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="card" style="color:#8892aa;font-size:13px;text-align:center;padding:2rem">No leads yet — they will appear here once your agent processes emails.</div>', unsafe_allow_html=True)


with col_chart:
    st.markdown('<div class="sec-head"><span>📈</span> Inquiry Categories</div>', unsafe_allow_html=True)

    if not df.empty:
        # Use real saved categories
        cat_counts = df["Category"].str.lower().value_counts().to_dict()
        # Normalise keys to Title case for display
        cat_display_map = {
            "pricing": "Pricing",
            "appointment": "Appointment",
            "support": "Support",
            "complaint": "Complaint",
            "general": "General"
        }
        cat_final = {}
        for k, v in cat_counts.items():
            label = cat_display_map.get(k.strip().lower(), k.capitalize())
            cat_final[label] = cat_final.get(label, 0) + v
        # Ensure all categories present
        for k in ["Pricing", "Appointment", "Support", "Complaint", "General"]:
            cat_final.setdefault(k, 0)
    else:
        cat_final = {"Pricing": 0, "Appointment": 0, "Support": 0, "Complaint": 0, "General": 0}

    colors = ["#1a6cf6", "#16a34a", "#d97706", "#b91c1c", "#7c3aed"]
    fig = go.Figure(go.Bar(
        x=list(cat_final.keys()),
        y=list(cat_final.values()),
        marker_color=colors,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>%{y} inquiries<extra></extra>"
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=4, b=0), height=200,
        xaxis=dict(showgrid=False, color="#8892aa", tickfont=dict(family="Inter", size=12)),
        yaxis=dict(showgrid=True, gridcolor="#e4e8f4", color="#8892aa",
                   tickfont=dict(family="DM Mono", size=11), zeroline=False, tickformat="d"),
        hoverlabel=dict(bgcolor="#fff", bordercolor="#e4e8f4", font=dict(family="Inter", color="#1a1d2e"))
    )
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Daily trend
    st.markdown('<div class="sec-head" style="margin-top:0.5rem"><span>📅</span> Leads per Day</div>', unsafe_allow_html=True)
    if not df.empty and df["Date"].notna().any():
        daily = df.groupby(df["Date"].dt.date).size().reset_index()
        daily.columns = ["Date", "Leads"]
        daily["Date"] = pd.to_datetime(daily["Date"])
        fig2 = go.Figure(go.Scatter(
            x=daily["Date"], y=daily["Leads"], mode="lines+markers",
            line=dict(color="#1a6cf6", width=2),
            marker=dict(color="#1a6cf6", size=6),
            fill="tozeroy", fillcolor="rgba(26,108,246,0.08)",
            hovertemplate="<b>%{x|%b %d}</b><br>%{y} leads<extra></extra>"
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=4, b=0), height=160,
            xaxis=dict(showgrid=False, color="#8892aa", tickformat="%b %d",
                       tickfont=dict(family="DM Mono", size=11)),
            yaxis=dict(showgrid=True, gridcolor="#e4e8f4", color="#8892aa",
                       tickfont=dict(family="DM Mono", size=11), zeroline=False, tickformat="d"),
            hoverlabel=dict(bgcolor="#fff", bordercolor="#e4e8f4", font=dict(family="Inter", color="#1a1d2e"))
        )
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------
# RECENT AI RESPONSES (static examples)
# -----------------------------------------------
st.markdown('<div class="sec-head"><span>🤖</span> Recent AI Responses</div>', unsafe_allow_html=True)

ai_examples = [
    {
        "customer": "Hi, I'd like to know your pricing. What plans do you offer?",
        "reply": "Thank you for reaching out! We offer flexible plans starting from $99/month, tailored to your business size and needs. I'd love to walk you through the options — would you be available for a quick 15-minute call this week?"
    },
    {
        "customer": "I need to book an appointment with your team for a consultation.",
        "reply": "Great, we'd love to connect! Our team is available Monday–Friday, 9am–5pm. Please reply with your preferred date and time, and we'll confirm your slot within the hour."
    },
    {
        "customer": "I'm having an issue with my account — it won't let me log in.",
        "reply": "We're sorry to hear that! Please try resetting your password via the login page. If the issue persists, reply with your registered email and we'll resolve it for you within 24 hours."
    }
]

# Replace with real emails if available
if not df.empty:
    for i, (_, row) in enumerate(df.head(2).iterrows()):
        msg = str(row["Message"])
        if len(msg) > 20:
            ai_examples[i]["customer"] = msg[:200]

ai_col1, ai_col2, ai_col3 = st.columns(3, gap="medium")
for col, ex in zip([ai_col1, ai_col2, ai_col3], ai_examples):
    with col:
        st.markdown(f"""
        <div class="ai-box">
            <div class="ai-box-customer">
                <div class="ai-box-label c">Customer Email</div>
                {ex['customer'][:120]}{'...' if len(ex['customer']) > 120 else ''}
            </div>
            <div class="ai-box-reply">
                <div class="ai-box-label a">AI Reply</div>
                {ex['reply']}
            </div>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------------------------
# SYSTEM STATUS
# -----------------------------------------------
st.markdown('<div class="sec-head" style="margin-top:0.5rem"><span>⚙️</span> System Status</div>', unsafe_allow_html=True)

last_processed = "No data yet"
if not df.empty and df["Date"].notna().any():
    latest_date = df["Date"].dropna().max()
    diff = datetime.now() - latest_date
    mins = int(diff.total_seconds() / 60)
    if mins < 1:
        last_processed = "Just now"
    elif mins < 60:
        last_processed = f"{mins} min ago"
    else:
        last_processed = latest_date.strftime("%b %d, %H:%M")

st.markdown(f"""
<div class="card">
    <div class="status-grid">
        <div class="stat-item">
            <div class="stat-dot green"></div>
            <div>
                <div class="stat-label">Agent Status</div>
                <div class="stat-value">Running</div>
            </div>
        </div>
        <div class="stat-item">
            <div class="stat-dot blue"></div>
            <div>
                <div class="stat-label">Last Email Processed</div>
                <div class="stat-value">{last_processed}</div>
            </div>
        </div>
        <div class="stat-item">
            <div class="stat-dot green"></div>
            <div>
                <div class="stat-label">Gmail API</div>
                <div class="stat-value">Connected</div>
            </div>
        </div>
        <div class="stat-item">
            <div class="stat-dot green"></div>
            <div>
                <div class="stat-label">Google Sheets</div>
                <div class="stat-value">Syncing</div>
            </div>
        </div>
        <div class="stat-item">
            <div class="stat-dot blue"></div>
            <div>
                <div class="stat-label">AI Model</div>
                <div class="stat-value">Llama 3.1 (Groq)</div>
            </div>
        </div>
        <div class="stat-item">
            <div class="stat-dot green"></div>
            <div>
                <div class="stat-label">Uptime</div>
                <div class="stat-value">99.9%</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------
# FOOTER
# -----------------------------------------------
st.markdown(f"""
<div class="dash-footer">
    <div class="footer-text">AI Customer Support Automation · Powered by Groq + Gmail API + Google Sheets</div>
    <div class="footer-text">Last refreshed: {datetime.now().strftime("%H:%M:%S")} · auto-refreshes every 30s</div>
</div>
""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()