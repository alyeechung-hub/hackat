import streamlit as st
import altair as alt
import pandas as pd
st.set_page_config(page_title="Retirement Guardian", page_icon="🛡️", layout="centered")

# ---------------- Data ----------------
ASSETS = ["Cash savings", "Government bonds", "Dividend shares", "Growth funds", "Inflation-linked"]
BASE = {"Low": [25, 50, 15, 0, 10], "Medium": [15, 35, 25, 15, 10], "High": [10, 20, 30, 30, 10]}
YIELD = [4, 4.5, 4, 1, 2.5]
PURPOSES = ["Retirement income", "Healthcare buffer", "Preserve capital",
            "Legacy for family", "Charitable giving"]
SCAM_SIGNS = {
    "guarantee": "Promises guaranteed returns. No real investment can.",
    "risk-free": "Calls itself risk-free. All investments carry risk.",
    "act now": "Pressure to act now. Scammers rush you.",
    "today only": "Pressure to act now. Scammers rush you.",
    "crypto": "Involves crypto, common in scams aimed at retirees.",
    "secret": "Asks you to keep it secret. Genuine firms never do.",
    "gift card": "Asks for gift cards. This is always a scam.",
    "safe account": "Asks you to move money to a 'safe account'. Known scam.",
    "double": "Promises to double your money. Classic scam sign.",
}

# ---------------- State ----------------
defaults = {"step": 0, "name": "", "age": 70, "amount": 50000,
            "who": None, "purpose": None, "risk": None, "bundle": None, "term": None}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)
s = st.session_state

# ---------------- Accessibility: text size ----------------
size = st.sidebar.radio("Text size", ["Normal", "Large", "Extra large"])
px = {"Normal": 19, "Large": 22, "Extra large": 26}[size]
st.markdown(f"""
<style>
html, body, [class*="css"], p, label {{ font-size: {px}px !important; }}
.stButton>button {{ min-height: 3.2rem; border-radius: 14px; width: 100%; }}
</style>""", unsafe_allow_html=True)

# ---------------- Helpers ----------------
def pick(label, options, key):
    """Radio that remembers its answer when you go back."""
    cur = s.get(key)
    val = st.radio(label, options, index=options.index(cur) if cur in options else None)
    s[key] = val
    return val

def nav(ok):
    c1, c2 = st.columns(2)
    if s.step > 0 and c1.button("Back"):
        s.step -= 1
        st.rerun()
    label = "See my plan" if s.step == 4 else "Continue"
    if c2.button(label, type="primary", disabled=not ok):
        s.step += 1
        st.rerun()

def alloc():
    a = BASE[s.risk][:]
    def mv(f, t, n):
        n = min(n, a[f]); a[f] -= n; a[t] += n
    p = s.purpose
    if p == "Healthcare buffer": mv(3, 0, 10); mv(2, 0, 5)
    if p == "Preserve capital":  mv(3, 1, 10); mv(2, 1, 5)
    if p == "Retirement income": mv(3, 2, 10); mv(1, 2, 5)
    if p == "Legacy for family": mv(0, 3, 10); mv(1, 3, 5)
    if p == "Charitable giving": mv(3, 0, 5);  mv(2, 0, 5)
    if s.term == "Short term":   mv(3, 0, 10); mv(2, 1, 10)
    if s.bundle == "Single investment":
        t = {"Low": 1, "Medium": 2, "High": 3}[s.risk]
        a = [100 if i == t else 0 for i in range(5)]
    return a

def gbp(x):
    return f"£{x:,.0f}"

# ---------------- Onboarding ----------------
def onboarding():
    st.title("🛡️ Retirement Guardian")
    st.progress((s.step + 1) / 5, text=f"Step {s.step + 1} of 5")

    if s.step == 0:
        st.header("Let’s get to know you")
        s.name = st.text_input("Your first name", s.name)
        s.age = st.number_input("Your age", 18, 110, s.age)
        s.amount = st.number_input("How much would you like to invest? (£)",
                                   0, 10_000_000, s.amount, step=1000)
        nav(bool(s.name.strip()) and s.amount > 0)
    elif s.step == 1:
        st.header("Who are you investing for?")
        v = pick("Choose one", ["For myself", "For my children"], "who")
        nav(v is not None)
    elif s.step == 2:
        st.header("What is this money for?")
        v = pick("Choose one", PURPOSES, "purpose")
        nav(v is not None)
    elif s.step == 3:
        st.header("How do you feel about ups and downs?")
        v = pick("Choose one", ["Low", "Medium", "High"], "risk")
        st.caption("Low: steady, small swings. Medium: some swings for more growth. "
                   "High: bigger swings, more growth over time.")
        nav(v is not None)
    elif s.step == 4:
        st.header("Your preferences")
        b = pick("How should your money be held?", ["Mixed bundle", "Single investment"], "bundle")
        t = pick("For how long?", ["Long term", "Short term"], "term")
        nav(b is not None and t is not None)

# ---------------- Plan tab ----------------
def plan_tab(a, V):
    st.subheader("Your recommended plan")
    st.caption(f"{s.who} · {s.purpose} · {s.risk} risk · {s.bundle} · {s.term}")
    view = st.radio("View", ["Ring", "Bar"], horizontal=True)
    df = pd.DataFrame({"Asset": ASSETS, "Percent": a})
    df = df[df.Percent > 0]
    if view == "Ring":
        chart = alt.Chart(df).mark_arc(innerRadius=70).encode(
            theta="Percent:Q", color=alt.Color("Asset:N", legend=alt.Legend(orient="bottom")),
            tooltip=["Asset", "Percent"])
        st.altair_chart(chart, use_container_width=True)
    else:
        st.bar_chart(df.set_index("Asset")["Percent"])
    income = sum(V * p / 100 * y / 100 for p, y in zip(a, YIELD))
    st.metric("Estimated income each year", gbp(income),
              help="An estimate, not a promise.")

    st.subheader(f"Advice for {s.name}")
    st.write({"Low": "- Most of your money is in cash and bonds, so swings stay small.",
              "Medium": "- A balanced mix: bonds and cash for safety, shares for growth.",
              "High": "- More in shares and growth funds. Bigger swings, more potential."}[s.risk])
    st.write("- " + {"Retirement income": "Extra dividend shares help pay you a regular income.",
                     "Healthcare buffer": "A larger cash buffer means medical bills never force you to sell.",
                     "Preserve capital": "Extra bonds protect the money you have built up.",
                     "Legacy for family": "A slice stays invested for growth so there is more to pass on.",
                     "Charitable giving": "Cash is kept ready so you can give on your own schedule."}[s.purpose])
    if s.bundle == "Single investment":
        st.warning("Everything is in one holding. If it falls, all your money feels it. "
                   "A mixed bundle spreads that risk.")
    else:
        st.write("- A small share is inflation-linked, so your spending power does not shrink.")
    st.write("- " + ("You may need the money soon, so more is kept in cash and bonds."
                     if s.term == "Short term" else
                     "You can wait, so more of your money can stay invested for growth."))

# ---------------- Simulator tab ----------------
def simulate_tab(a, V):
    st.subheader("What if…?")
    sc = st.radio("Pick a scenario", ["📉 Market crash", "🛒 Prices rise",
                                      "🏥 Medical emergency", "⏳ Living longer"], horizontal=True)
    if "crash" in sc:
        shock = [0, -.05, -.25, -.4, -.05]
        v = sum(V * p / 100 * (1 + x) for p, x in zip(a, shock))
        st.metric("Value after a sharp fall", gbp(v), f"-{gbp(V - v)}")
        st.progress(max(0.0, min(1.0, v / V)))
        st.info("Your cash and bonds cushion the fall. You would not need to sell anything to cover bills.")
    elif "Prices" in sc:
        st.metric("Monthly spending needed in 10 years", gbp(2000 * 1.05 ** 10),
                  "to match today’s £2,000 at 5% inflation", delta_color="off")
        prot = a[4] + a[2]
        st.progress(min(1.0, prot * 2.2 / 100))
        st.info(f"About {prot}% of your plan is in assets that tend to rise with prices. "
                "Guardian would suggest reviewing your income each year.")
    elif "Medical" in sc:
        cash = V * a[0] / 100
        covered = min(30000, cash)
        st.metric("£30,000 bill covered by cash", gbp(covered))
        st.progress(covered / 30000)
        st.info("Your cash covers it in full." if covered >= 30000 else
                f"Cash covers part. {gbp(30000 - covered)} would come from bonds. "
                "Consider a bigger cash buffer.")
    else:
        r = {"Low": .035, "Medium": .045, "High": .055}[s.risk]
        v, w, y = V, V * .05, 0
        while v > 0 and y < 35:
            v = (v - w) * (1 + r); w *= 1.025; y += 1
        st.metric("Your money lasts", f"To age {s.age + y}" if y < 35 else f"Past {s.age + 35}",
                  f"spending {gbp(V * .05)} a year, rising 2.5% yearly", delta_color="off")
        st.progress(min(1.0, y / 35))
        st.info("Projected to last well into old age." if y >= 30 else
                "Your money may run out early. Spending a little less could help.")

# ---------------- Protect tab ----------------
def protect_tab():
    st.subheader("Protect what you’ve built")
    st.error("**High risk:** A caller asked you to move £8,000 to a “safe account”. Banks never ask this.")
    c1, c2 = st.columns(2)
    if c1.button("Block and report"): st.success("Reported.")
    if c2.button("Tell family"): st.success("Family notified.")
    st.warning("**Check:** An email promises 12% a year “with no risk”. "
               "This does not match any regulated product.")

    st.markdown("#### Check an offer")
    text = st.text_area("Paste a message, email or advert",
                        placeholder="e.g. Guaranteed 15% returns. Act now, keep this secret.")
    if st.button("Check for scam signs"):
        flags = {m for k, m in SCAM_SIGNS.items() if k in text.lower()}
        if flags:
            st.error(f"{len(flags)} warning sign(s) found")
            for f in flags: st.write("⚠️ " + f)
            st.write("**Do not send money.** Talk to someone you trust first.")
        else:
            st.success("No obvious signs. Still check the firm is on the FCA register.")

    st.markdown("#### Portfolio risk monitor")
    st.progress({"Low": 12, "Medium": 50, "High": 86}[s.risk] / 100)
    st.success(f"On track: your holdings match your {s.risk.lower()} comfort level.")

    st.markdown("#### Donation planning")
    don = st.slider("Monthly giving (£)", 0, 500, 50, step=10)
    st.write(f"{gbp(don * 12)} a year. With Gift Aid, charities can claim about "
             f"{gbp(don * 12 * .25)} more at no cost to you.")

    st.markdown("#### Estate goals")
    fam = st.slider("Share left to family (%)", 0, 100, 70, step=5)
    st.write(f"Family {fam}% · Charity {100 - fam}%")
    for item in ["Will is up to date", "Lasting power of attorney in place",
                 "Beneficiaries named on all accounts"]:
        st.checkbox(item)

# ---------------- Main ----------------
if s.step < 5:
    onboarding()
else:
    st.title(f"Hello, {s.name} 🛡️")
    if st.sidebar.button("Change my answers"):
        s.step = 1
        st.rerun()
    a, V = alloc(), s.amount
    t1, t2, t3 = st.tabs(["📊 Plan", "🔮 What if", "🛡️ Protect"])
    with t1: plan_tab(a, V)
    with t2: simulate_tab(a, V)
    with t3: protect_tab()
    