import streamlit as st
import requests
import json
import time

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    layout="wide",
    page_title="Smart Auto-Substitute | AI Engine",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS — Dark Ops aesthetic
# ==========================================
st.markdown("""
<style>
/* ── Import fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
    --bg-primary:    #0b0e14;
    --bg-card:       #141922;
    --bg-card-hover: #1c2333;
    --border:        #252d3d;
    --border-active: #3d4f6e;
    --accent-blue:   #4a8fff;
    --accent-green:  #2ef5a0;
    --accent-orange: #ffb340;
    --accent-red:    #ff4f6e;
    --text-primary:  #e8edf5;
    --text-muted:    #6b7a99;
    --text-dim:      #3d4f6e;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Streamlit containers ── */
.stApp { background-color: var(--bg-primary) !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }

/* ── Remove default Streamlit borders/bg ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* ── Headers ── */
h1 { font-family: 'Space Mono', monospace !important; font-size: 1.5rem !important; letter-spacing: -0.02em !important; }
h2, h3 { font-family: 'Space Mono', monospace !important; font-size: 1rem !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; color: var(--text-muted) !important; }

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border-active) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--bg-card-hover) !important;
    border-color: var(--accent-blue) !important;
    color: var(--accent-blue) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(74, 143, 255, 0.15) !important;
}

/* ── Alert / Info boxes ── */
.stAlert {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    background: var(--bg-card) !important;
}
[data-testid="stNotification"] { border-radius: 10px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--text-muted) !important; }

/* ── Text inputs ── */
[data-testid="stTextInput"] input {
    background: var(--bg-primary) !important;
    border: 1px solid var(--border-active) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px rgba(74, 143, 255, 0.15) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-primary) !important;
    border: 1px solid var(--border-active) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--bg-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary { color: var(--text-muted) !important; font-size: 0.8rem !important; }

/* ── JSON display ── */
[data-testid="stJson"] {
    background: var(--bg-primary) !important;
    border-radius: 8px !important;
    font-size: 0.75rem !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent-blue) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-active); border-radius: 2px; }

/* ── Custom components ── */
.header-badge {
    display: inline-block;
    background: rgba(74, 143, 255, 0.1);
    border: 1px solid rgba(74, 143, 255, 0.3);
    color: var(--accent-blue);
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    margin-left: 8px;
    vertical-align: middle;
}

.col-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim);
    padding: 0.4rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.col-header .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    display: inline-block;
}
.col-header.driver { color: var(--accent-orange); }
.col-header.ai     { color: var(--accent-blue);   }
.col-header.cust   { color: var(--accent-green);  }

.score-ring {
    text-align: center;
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    position: relative;
}
.score-ring .score-value {
    font-family: 'Space Mono', monospace;
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1;
    margin: 0;
}
.score-ring .score-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 4px;
}
.score-ring .score-path {
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    margin-top: 0.5rem;
    opacity: 0.8;
}

.score-green  { background: rgba(46, 245, 160, 0.06); border: 1px solid rgba(46, 245, 160, 0.25); }
.score-orange { background: rgba(255, 179, 64, 0.06);  border: 1px solid rgba(255, 179, 64, 0.25); }
.score-red    { background: rgba(255, 79, 110, 0.06);  border: 1px solid rgba(255, 79, 110, 0.25); }

.scenario-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s;
}
.scenario-card:hover { border-color: var(--border-active); }
.scenario-card .s-title { font-size: 0.78rem; font-weight: 600; color: var(--text-primary); }
.scenario-card .s-desc  { font-size: 0.72rem; color: var(--text-muted); margin-top: 2px; }

.phone-frame {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem;
    min-height: 380px;
    position: relative;
}
.phone-frame::before {
    content: '● ● ●';
    display: block;
    font-size: 0.45rem;
    letter-spacing: 4px;
    color: var(--border-active);
    text-align: center;
    margin-bottom: 1rem;
}

.status-idle {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--text-dim);
    font-size: 0.82rem;
    line-height: 1.8;
}

.action-auto {
    background: rgba(46, 245, 160, 0.07);
    border: 1px solid rgba(46, 245, 160, 0.25);
    border-radius: 10px;
    padding: 1rem;
}
.action-choice {
    background: rgba(255, 179, 64, 0.07);
    border: 1px solid rgba(255, 179, 64, 0.25);
    border-radius: 10px;
    padding: 1rem;
}
.action-fallback {
    background: rgba(255, 79, 110, 0.07);
    border: 1px solid rgba(255, 79, 110, 0.25);
    border-radius: 10px;
    padding: 1rem;
}

.tag-pill {
    display: inline-block;
    background: rgba(74, 143, 255, 0.1);
    border: 1px solid rgba(74, 143, 255, 0.2);
    color: var(--accent-blue);
    font-size: 0.65rem;
    padding: 1px 7px;
    border-radius: 20px;
    margin: 2px;
}

.reasoning-box {
    background: var(--bg-primary);
    border-left: 3px solid var(--accent-blue);
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    font-size: 0.82rem;
    line-height: 1.7;
    color: var(--text-muted);
}

.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 0.8rem 0;
}

.meta-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
}

.kv-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.3rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.78rem;
}
.kv-row:last-child { border-bottom: none; }
.kv-row .k { color: var(--text-muted); }
.kv-row .v { font-weight: 600; font-family: 'Space Mono', monospace; font-size: 0.72rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA
# ==========================================
MENU_DATABASE = [
    {"id": "m1", "name": "Pizza Bò bằm",      "price": 150000, "tags": ["mặn", "bò", "pizza"]},
    {"id": "m2", "name": "Pizza Gà cay",       "price": 145000, "tags": ["mặn", "gà", "pizza", "cay"]},
    {"id": "m3", "name": "Mỳ Ý sốt bò",        "price": 120000, "tags": ["mặn", "bò", "pasta"]},
    {"id": "m4", "name": "Salad chay",         "price":  80000, "tags": ["chay", "salad"]},
    {"id": "m5", "name": "Coca Cola",          "price":  20000, "tags": ["đồ uống", "soda", "ngọt"]},
    {"id": "m6", "name": "Pepsi",              "price":  20000, "tags": ["đồ uống", "soda", "ngọt"]},
    {"id": "m7", "name": "Gà rán (không cay)", "price":  40000, "tags": ["mặn", "gà", "chiên"]},
]

USER_PROFILES = {
    "user1": {
        "name": "Nguyễn Văn A",
        "dietary": "none",
        "frequent_tags": ["bò", "gà", "cay"],
        "avatar": "👤",
    },
    "user2": {
        "name": "Trần Thị B",
        "dietary": "vegan",
        "frequent_tags": ["salad", "healthy"],
        "avatar": "🌿",
    },
}

SCENARIOS = [
    {
        "id": 1,
        "badge": "AUTO",
        "badge_color": "#2ef5a0",
        "title": "Happy Path  ≥ 90",
        "desc": "Hết Coca Cola — tự động đổi sang Pepsi",
        "outOfStockId": "m5",
        "userId": "user1",
    },
    {
        "id": 2,
        "badge": "CHOICE",
        "badge_color": "#ffb340",
        "title": "Low Confidence  50–89",
        "desc": "Hết Pizza Bò — cho khách chọn món",
        "outOfStockId": "m1",
        "userId": "user1",
    },
    {
        "id": 3,
        "badge": "FALLBACK",
        "badge_color": "#ff4f6e",
        "title": "No Match  < 50",
        "desc": "Khách ăn chay, hết Salad",
        "outOfStockId": "m4",
        "userId": "user2",
    },
]

SYSTEM_PROMPT = """Bạn là AI Xử lý sự cố đơn hàng Food Delivery.
Nhiệm vụ: tìm món thay thế tối ưu cho món bị hết hàng.

Tiêu chí tính Confidence_Score (0–100):
• +40 điểm: cùng nhóm món ăn (tag)
• +30 điểm: khớp sở thích frequent_tags của user
• +30 điểm: chênh lệch giá < 15%
• VETO (–100): vi phạm dietary — ví dụ khách dietary='vegan' mà gợi ý đồ có tag 'bò' hoặc 'gà'

Quy tắc rẽ nhánh (action_path):
• score ≥ 90  → "auto_swap"      (trả 1 món tốt nhất)
• 50 ≤ score < 90 → "user_choice"   (trả 1–2 lựa chọn)
• score < 50  → "manual_fallback" (suggested_substitutes = [])

TRẢ VỀ DUY NHẤT JSON, không kèm markdown hay text ngoài:
{
  "reasoning": "Giải thích ngắn gọn cách tính điểm",
  "confidence_score": 85,
  "action_path": "auto_swap",
  "suggested_substitutes": [
    {"id": "mX", "name": "Tên món", "price_diff": -5000}
  ]
}"""


# ==========================================
# API CALL
# ==========================================
def call_openrouter(api_key: str, model: str, scenario: dict) -> dict:
    out_item = next(m for m in MENU_DATABASE if m["id"] == scenario["outOfStockId"])
    available = [m for m in MENU_DATABASE if m["id"] != scenario["outOfStockId"]]
    user = USER_PROFILES[scenario["userId"]]

    payload_data = {
        "order_context": {"out_of_stock_item": out_item, "user_preferences": user},
        "available_menu": available,
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Dữ liệu:\n{json.dumps(payload_data, ensure_ascii=False, indent=2)}"},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://hackathon-demo.com",
        "X-Title": "Smart Auto-Substitute Demo",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=body,
        timeout=30,
    )

    if resp.status_code != 200:
        raise ValueError(f"API {resp.status_code}: {resp.text[:300]}")

    raw = resp.json()["choices"][0]["message"]["content"]
    raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(raw)


# ==========================================
# SESSION STATE
# ==========================================
if "active_scenario" not in st.session_state:
    st.session_state.active_scenario = None
if "ai_result" not in st.session_state:
    st.session_state.ai_result = None
if "latency_ms" not in st.session_state:
    st.session_state.latency_ms = None

# Customer app state machine
# States: None | "auto_swapped" | "undo_pending" | "confirmed" | "refunded" | "choice_made"
if "cust_state" not in st.session_state:
    st.session_state.cust_state = None
if "cust_chosen_item" not in st.session_state:
    st.session_state.cust_chosen_item = None  # dict of the chosen substitute


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.2rem;">
        <div style="font-family:'Space Mono',monospace; font-size:0.65rem;
                    letter-spacing:0.12em; color:#3d4f6e; text-transform:uppercase;">
            Configuration
        </div>
        <div style="font-size:1.1rem; font-weight:600; margin-top:4px;">
            OpenRouter Settings
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-or-v1-…",
        help="Lấy key tại openrouter.ai/keys",
    )

    model_choice = st.selectbox(
        "Model",
        options=[
            "openai/gpt-4o-mini",
            "google/gemini-2.5-flash-preview",
            "meta-llama/llama-3-8b-instruct:free",
            "anthropic/claude-3-haiku",
        ],
        help="Model rẻ và nhanh phù hợp để demo",
    )

    st.markdown("<hr style='border-color:#252d3d; margin:1rem 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.75rem; color:#6b7a99; line-height:1.8;">
        <b style="color:#e8edf5;">Logic phân luồng:</b><br>
        🟢 ≥ 90 → auto_swap<br>
        🟡 50–89 → user_choice<br>
        🔴 &lt;50 → manual_fallback
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.latency_ms:
        st.markdown(f"""
        <div style="margin-top:1rem; font-size:0.72rem; color:#3d4f6e;">
            ⚡ Latency: <b style="color:#4a8fff;">{st.session_state.latency_ms} ms</b>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div style="display:flex; align-items:baseline; gap:12px; margin-bottom:1.5rem;">
    <h1 style="margin:0; color:#e8edf5; font-size:1.4rem;">
        ⚡ Smart Auto-Substitute
    </h1>
    <span class="header-badge">AI Engine v2</span>
</div>
<p style="color:#6b7a99; font-size:0.85rem; margin-top:-0.8rem; margin-bottom:1.5rem;">
    Hệ thống ra quyết định tự động cho sự cố hết hàng trong Food Delivery — 3 luồng dựa trên <b style="color:#e8edf5;">Confidence Score</b>
</p>
""", unsafe_allow_html=True)


# ==========================================
# 3-COLUMN LAYOUT
# ==========================================
col_driver, col_ai, col_customer = st.columns([1, 1.1, 1], gap="medium")


# ──────────────────────────────────────────
# COL 1: DRIVER APP
# ──────────────────────────────────────────
with col_driver:
    st.markdown("""
    <div class="col-header driver">
        <span class="dot"></span> App Tài Xế
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.78rem; color:#6b7a99; margin-bottom:1rem; line-height:1.6;">
        Quán báo hết món. Chọn kịch bản để trigger AI engine:
    </div>
    """, unsafe_allow_html=True)

    for sc in SCENARIOS:
        out_item = next(m for m in MENU_DATABASE if m["id"] == sc["outOfStockId"])
        user = USER_PROFILES[sc["userId"]]
        is_active = (
            st.session_state.active_scenario is not None
            and st.session_state.active_scenario["id"] == sc["id"]
        )

        st.markdown(f"""
        <div class="scenario-card" style="{'border-color:var(--border-active);' if is_active else ''}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="s-title">{sc['title']}</span>
                <span style="font-size:0.6rem; font-family:'Space Mono',monospace;
                             color:{sc['badge_color']}; background:rgba(255,255,255,0.04);
                             border:1px solid {sc['badge_color']}44; padding:1px 6px; border-radius:4px;">
                    {sc['badge']}
                </span>
            </div>
            <div class="s-desc">{sc['desc']}</div>
            <div class="meta-row" style="margin-top:6px;">
                <span>{user['avatar']} {user['name']}</span>
                <span>🏷️ {out_item['price']:,}đ</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        btn_label = (
            f"✓ Đang xử lý..." if is_active and st.session_state.ai_result is None
            else f"🚨 Báo hết: {out_item['name']}"
        )

        if st.button(btn_label, key=f"btn_sc_{sc['id']}", use_container_width=True):
            if not api_key:
                st.error("⚠️ Vui lòng nhập OpenRouter API Key trong sidebar.")
            else:
                st.session_state.active_scenario = sc
                st.session_state.ai_result = None
                st.session_state.latency_ms = None
                st.session_state.cust_state = None
                st.session_state.cust_chosen_item = None
                st.rerun()

        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)


# ──────────────────────────────────────────
# COL 2: AI ENGINE
# ──────────────────────────────────────────
with col_ai:
    st.markdown("""
    <div class="col-header ai">
        <span class="dot"></span> AI Decision Engine
    </div>
    """, unsafe_allow_html=True)

    sc = st.session_state.active_scenario

    if sc is None:
        st.markdown("""
        <div style="text-align:center; padding:3rem 0; color:#3d4f6e; font-size:0.82rem; line-height:2;">
            ⬡<br>Chờ trigger từ<br>App Tài Xế
        </div>
        """, unsafe_allow_html=True)

    else:
        # Auto-call API if no result yet
        if st.session_state.ai_result is None:
            with st.spinner("Đang phân tích & tính Confidence Score…"):
                try:
                    t0 = time.monotonic()
                    result = call_openrouter(api_key, model_choice, sc)
                    st.session_state.latency_ms = int((time.monotonic() - t0) * 1000)
                    st.session_state.ai_result = result
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi API: {e}")

        result = st.session_state.ai_result
        if result:
            score = result.get("confidence_score", 0)
            path = result.get("action_path", "manual_fallback")

            if score >= 90:
                ring_cls, color = "score-green", "#2ef5a0"
                path_icon = "🟢"
            elif score >= 50:
                ring_cls, color = "score-orange", "#ffb340"
                path_icon = "🟡"
            else:
                ring_cls, color = "score-red", "#ff4f6e"
                path_icon = "🔴"

            # Score ring
            st.markdown(f"""
            <div class="score-ring {ring_cls}">
                <div class="score-value" style="color:{color};">{score}</div>
                <div class="score-label">Confidence Score</div>
                <div class="score-path" style="color:{color};">
                    {path_icon} {path.replace('_', ' ').upper()}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Key metrics
            out_item = next(m for m in MENU_DATABASE if m["id"] == sc["outOfStockId"])
            user = USER_PROFILES[sc["userId"]]
            subs = result.get("suggested_substitutes", [])

            st.markdown(f"""
            <div style="margin-bottom:0.8rem;">
                <div class="kv-row">
                    <span class="k">Món hết</span>
                    <span class="v">{out_item['name']}</span>
                </div>
                <div class="kv-row">
                    <span class="k">Khách hàng</span>
                    <span class="v">{user['avatar']} {user['name']}</span>
                </div>
                <div class="kv-row">
                    <span class="k">Dietary</span>
                    <span class="v">{user['dietary']}</span>
                </div>
                <div class="kv-row">
                    <span class="k">Đề xuất</span>
                    <span class="v">{len(subs)} món</span>
                </div>
                {"" if not st.session_state.latency_ms else f'<div class="kv-row"><span class="k">Latency</span><span class="v" style="color:#4a8fff;">{st.session_state.latency_ms} ms</span></div>'}
            </div>
            """, unsafe_allow_html=True)

            # Reasoning
            with st.expander("📝 AI Reasoning", expanded=True):
                st.markdown(f"""
                <div class="reasoning-box">{result.get('reasoning', '—')}</div>
                """, unsafe_allow_html=True)

            # Raw JSON
            with st.expander("🔍 Raw JSON"):
                st.json(result)


# ──────────────────────────────────────────
# COL 3: CUSTOMER APP  (state machine)
# ──────────────────────────────────────────

def fmt_diff(diff: int) -> str:
    if diff > 0:  return f"+{diff:,}đ"
    if diff < 0:  return f"{diff:,}đ"
    return "cùng giá"

with col_customer:
    st.markdown("""
    <div class="col-header cust">
        <span class="dot"></span> App Khách Hàng
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="phone-frame">', unsafe_allow_html=True)

    result = st.session_state.ai_result
    sc     = st.session_state.active_scenario
    cstate = st.session_state.cust_state   # shorthand

    # ── IDLE ──────────────────────────────
    if not result or not sc:
        st.markdown("""
        <div class="status-idle">
            📦<br><br>
            Đang theo dõi đơn hàng…<br>
            <span style="font-size:0.7rem;">Tài xế đang trên đường tới quán</span>
        </div>
        """, unsafe_allow_html=True)

    else:
        path     = result.get("action_path")
        out_item = next(m for m in MENU_DATABASE if m["id"] == sc["outOfStockId"])
        out_name = out_item["name"]
        out_price = out_item["price"]
        user     = USER_PROFILES[sc["userId"]]
        subs     = result.get("suggested_substitutes", [])

        # Initialize cust_state on first render after AI result arrives
        if cstate is None:
            if path == "auto_swap" and subs:
                st.session_state.cust_state = "auto_swapped"
            elif path == "user_choice":
                st.session_state.cust_state = "awaiting_choice"
            elif path == "manual_fallback":
                st.session_state.cust_state = "manual_fallback"
            st.rerun()

        cstate = st.session_state.cust_state  # re-read after possible update

        # ════════════════════════════════════════
        # STATE: auto_swapped  — "Đã đổi tự động"
        # ════════════════════════════════════════
        if cstate == "auto_swapped":
            new_item = subs[0]
            diff_text = fmt_diff(new_item.get("price_diff", 0))

            st.markdown(f"""
            <div class="action-auto">
                <div style="font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase;
                            color:#2ef5a0; margin-bottom:0.5rem;">✅ Tự động đổi món</div>
                <div style="font-size:0.85rem; line-height:1.7; color:#e8edf5;">
                    Món <b>{out_name}</b> đã hết.<br>
                    Hệ thống đã đổi sang <b>{new_item['name']}</b>
                    <span style="color:#2ef5a0; font-size:0.75rem;"> ({diff_text})</span>
                    dựa trên lịch sử của bạn.
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

            if st.button("↩ Hủy đổi món", key="undo_btn", use_container_width=True):
                st.session_state.cust_state = "undo_pending"
                st.rerun()

            st.markdown(f"""
            <div style="font-size:0.7rem; color:#3d4f6e; text-align:center; margin-top:6px;">
                {user['avatar']} {user['name']} · {user['dietary']}
            </div>""", unsafe_allow_html=True)

        # ════════════════════════════════════════
        # STATE: undo_pending — "Đã hủy đổi món, chọn lại"
        # ════════════════════════════════════════
        elif cstate == "undo_pending":
            new_item = subs[0]

            st.markdown(f"""
            <div style="background:rgba(255,179,64,0.07); border:1px solid rgba(255,179,64,0.3);
                        border-radius:10px; padding:0.9rem;">
                <div style="font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase;
                            color:#ffb340; margin-bottom:0.4rem;">↩ Đã hủy đổi món</div>
                <div style="font-size:0.83rem; line-height:1.7; color:#e8edf5;">
                    Bạn đã hủy việc đổi sang <b>{new_item['name']}</b>.<br>
                    Chọn cách xử lý đơn hàng của bạn:
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

            # List all other available items (excluding original out-of-stock)
            manual_options = [m for m in MENU_DATABASE if m["id"] != sc["outOfStockId"]]
            st.markdown("""
            <div style="font-size:0.72rem; color:#6b7a99; margin-bottom:0.4rem; letter-spacing:0.05em;">
                CHỌN MÓN KHÁC TỪ MENU
            </div>""", unsafe_allow_html=True)

            for opt in manual_options:
                price_diff = opt["price"] - out_price
                label = f"{opt['name']}  ·  {fmt_diff(price_diff)}"
                if st.button(label, key=f"manual_{opt['id']}", use_container_width=True):
                    st.session_state.cust_state = "choice_made"
                    st.session_state.cust_chosen_item = {**opt, "price_diff": price_diff}
                    st.rerun()

            st.markdown("<div style='height:0.4rem;'></div>", unsafe_allow_html=True)
            if st.button("💸 Hoàn tiền món này", key="refund_from_undo", use_container_width=True):
                st.session_state.cust_state = "refunded"
                st.rerun()

        # ════════════════════════════════════════
        # STATE: awaiting_choice — user_choice path
        # ════════════════════════════════════════
        elif cstate == "awaiting_choice":
            st.markdown(f"""
            <div class="action-choice">
                <div style="font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase;
                            color:#ffb340; margin-bottom:0.4rem;">⏱ Cần xác nhận</div>
                <div style="font-size:0.83rem; line-height:1.7; color:#e8edf5;">
                    Món <b>{out_name}</b> đã hết.<br>
                    Chọn món thay thế hoặc hoàn tiền.
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

            if subs:
                st.markdown("""
                <div style="font-size:0.72rem; color:#6b7a99; margin-bottom:0.4rem; letter-spacing:0.05em;">
                    GỢI Ý TỪ AI
                </div>""", unsafe_allow_html=True)
                for sub in subs:
                    diff_txt = fmt_diff(sub.get("price_diff", 0))
                    if st.button(f"✓ {sub['name']}  ·  {diff_txt}", key=f"choice_{sub['id']}", use_container_width=True):
                        st.session_state.cust_state = "choice_made"
                        st.session_state.cust_chosen_item = sub
                        st.rerun()

            st.markdown("<div style='height:0.3rem;'></div>", unsafe_allow_html=True)
            if st.button("💸 Hoàn tiền món này", key="refund_btn", use_container_width=True):
                st.session_state.cust_state = "refunded"
                st.rerun()

        # ════════════════════════════════════════
        # STATE: choice_made — Confirmed substitute
        # ════════════════════════════════════════
        elif cstate == "choice_made":
            chosen = st.session_state.cust_chosen_item or {}
            diff_text = fmt_diff(chosen.get("price_diff", 0))

            st.markdown(f"""
            <div style="background:rgba(46,245,160,0.07); border:1px solid rgba(46,245,160,0.3);
                        border-radius:10px; padding:0.9rem; margin-bottom:0.75rem;">
                <div style="font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase;
                            color:#2ef5a0; margin-bottom:0.5rem;">🎉 Đã xác nhận</div>
                <div style="font-size:0.83rem; line-height:1.7; color:#e8edf5;">
                    Đơn hàng đã cập nhật.<br>
                    Bạn sẽ nhận <b>{chosen.get('name', '—')}</b>
                    <span style="color:#2ef5a0; font-size:0.75rem;"> ({diff_text})</span>
                    thay cho <b>{out_name}</b>.
                </div>
            </div>
            <div style="display:flex; gap:8px; font-size:0.72rem; color:#6b7a99;">
                <div style="flex:1; background:var(--bg-primary); border-radius:8px; padding:0.6rem; text-align:center;">
                    <div style="color:#3d4f6e; margin-bottom:2px;">MÓN GỐC</div>
                    <div style="color:#6b7a99; font-size:0.75rem; text-decoration:line-through;">{out_name}</div>
                </div>
                <div style="display:flex; align-items:center; color:#3d4f6e; font-size:1rem;">→</div>
                <div style="flex:1; background:rgba(46,245,160,0.05); border:1px solid rgba(46,245,160,0.2);
                            border-radius:8px; padding:0.6rem; text-align:center;">
                    <div style="color:#3d4f6e; margin-bottom:2px;">MÓN MỚI</div>
                    <div style="color:#2ef5a0; font-size:0.75rem;">{chosen.get('name', '—')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align:center; font-size:0.75rem; color:#6b7a99; padding:0.5rem;
                        background:var(--bg-primary); border-radius:8px;">
                🛵 Tài xế đang trên đường giao hàng…
            </div>""", unsafe_allow_html=True)

        # ════════════════════════════════════════
        # STATE: refunded — Hoàn tiền
        # ════════════════════════════════════════
        elif cstate == "refunded":
            st.markdown(f"""
            <div style="background:rgba(107,122,153,0.08); border:1px solid rgba(107,122,153,0.25);
                        border-radius:10px; padding:0.9rem; margin-bottom:0.75rem;">
                <div style="font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase;
                            color:#6b7a99; margin-bottom:0.5rem;">💸 Đã yêu cầu hoàn tiền</div>
                <div style="font-size:0.83rem; line-height:1.7; color:#e8edf5;">
                    Món <b>{out_name}</b> sẽ được hoàn tiền về ví của bạn<br>
                    trong <b>5–15 phút</b>.
                </div>
            </div>
            <div style="font-size:0.72rem; color:#6b7a99; line-height:1.8; padding:0.5rem 0.75rem;
                        background:var(--bg-primary); border-radius:8px;">
                <div style="display:flex; justify-content:space-between; padding:3px 0; border-bottom:1px solid var(--border);">
                    <span>Món hủy</span><span style="color:#e8edf5;">{out_name}</span>
                </div>
                <div style="display:flex; justify-content:space-between; padding:3px 0; border-bottom:1px solid var(--border);">
                    <span>Số tiền hoàn</span><span style="color:#2ef5a0;">{out_price:,}đ</span>
                </div>
                <div style="display:flex; justify-content:space-between; padding:3px 0;">
                    <span>Trạng thái</span><span style="color:#ffb340;">Đang xử lý…</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align:center; font-size:0.73rem; color:#3d4f6e;">
                Phần còn lại của đơn hàng vẫn tiếp tục giao.
            </div>""", unsafe_allow_html=True)

        # ════════════════════════════════════════
        # STATE: manual_fallback
        # ════════════════════════════════════════
        elif cstate == "manual_fallback":
            st.markdown(f"""
            <div class="action-fallback">
                <div style="font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase;
                            color:#ff4f6e; margin-bottom:0.5rem;">📞 Cần hỗ trợ thủ công</div>
                <div style="font-size:0.83rem; line-height:1.7; color:#e8edf5;">
                    Món <b>{out_name}</b> đã hết nhưng AI không tìm thấy lựa chọn an toàn
                    do chế độ ăn <b>{user['dietary']}</b>.
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

            st.markdown("""
            <div style="text-align:center; padding:0.8rem; background:rgba(255,79,110,0.05);
                        border-radius:8px; font-size:0.8rem; color:#ff4f6e; margin-bottom:0.75rem;">
                🔔 Tài xế đang gọi cho bạn…
            </div>""", unsafe_allow_html=True)

            if st.button("📞 Nhận cuộc gọi", key="call_btn", use_container_width=True):
                st.session_state.cust_state = "refunded"  # after call → refund flow
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # /phone-frame