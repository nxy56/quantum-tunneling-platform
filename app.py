import html
import os

import numpy as np
import plotly.graph_objects as go
import requests
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="量子隧穿效应交互平台",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="auto",
)

# =========================================================
# 全局样式：紧凑、顶部对齐、适配常见桌面分辨率
# =========================================================
st.markdown(
    """
<style>
:root {
    --bg-main: #080d16;
    --bg-deep: #030812;
    --panel: rgba(13, 29, 58, 0.82);
    --panel-strong: rgba(12, 27, 60, 0.96);
    --cyan: #50e7ff;
    --green: #39ff14;
    --muted: #8fb8ca;
    --border: rgba(68, 205, 255, 0.18);
}

html, body, [class*="css"] {
    background: radial-gradient(circle at top left, #0a1629 0%, #070c15 55%, #03060c 100%);
    color: #d9f6ff;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #0a1629 0%, #070c15 55%, #03060c 100%);
}

[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}

.block-container {
    max-width: 1580px;
    padding-top: 0.35rem;
    padding-right: 1rem;
    padding-bottom: 0.45rem;
    padding-left: 1rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #202432 0%, #161c28 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding-top: 0.35rem;
}

section[data-testid="stSidebar"] * {
    color: #e9f7ff;
}

h1, h2, h3 {
    color: var(--cyan) !important;
}

.dashboard-title {
    margin: 0;
    padding: 0;
    font-size: clamp(2rem, 2.7vw, 2.85rem);
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: var(--cyan);
}

.side-title {
    margin: 0;
    padding: 0;
    font-size: clamp(1.75rem, 2.2vw, 2.35rem);
    line-height: 1.05;
    font-weight: 800;
    color: var(--cyan);
}

.sidebar-title {
    margin: 0 0 0.35rem 0;
    font-size: 1.35rem;
    line-height: 1.1;
    font-weight: 800;
    color: #ecf8ff;
}

.dashboard-subtitle {
    margin: 0.28rem 0 0.45rem 0;
    color: var(--muted);
    font-size: 0.98rem;
    line-height: 1.35;
}

.main-top-offset {
    height: 2.75rem;
}

.side-top-offset {
    height: 2.75rem;
}

[data-testid="stMetric"] {
    min-height: 82px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 0.55rem 0.75rem;
}

[data-testid="stMetricLabel"] {
    font-size: 0.87rem;
}

[data-testid="stMetricValue"] {
    color: var(--green);
    font-size: clamp(1.55rem, 2vw, 2rem);
}

[data-testid="stPlotlyChart"] {
    margin-top: -0.15rem;
    margin-bottom: -0.2rem;
}

[data-testid="stSlider"] {
    margin-top: -0.2rem;
    margin-bottom: -0.25rem;
}

[data-testid="stToggle"] {
    margin-top: -0.15rem;
    margin-bottom: -0.1rem;
}

.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #00d8ff, #23a6ff) !important;
}

.compact-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.65rem 0.8rem;
    margin: 0.35rem 0 0.55rem 0;
}

.param-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.42rem;
    margin: 0.4rem 0 0.55rem 0;
}

.param-chip {
    background: rgba(8, 19, 40, 0.86);
    border: 1px solid rgba(74, 202, 255, 0.13);
    border-radius: 10px;
    padding: 0.48rem 0.6rem;
    font-size: 0.9rem;
}

.param-chip code {
    color: #66f29a;
}

.tip-box {
    background: rgba(37, 91, 145, 0.35);
    border-left: 4px solid #35b7ff;
    border-radius: 10px;
    padding: 0.62rem 0.72rem;
    margin: 0.35rem 0 0.55rem 0;
    color: #a8dcff;
    line-height: 1.45;
    font-size: 0.91rem;
}

.section-label {
    color: var(--cyan);
    font-size: clamp(1.75rem, 2.2vw, 2.35rem);
    line-height: 1.05;
    font-weight: 800;
    margin: 0.72rem 0 0.38rem 0;
}

.observation-list {
    margin: 0.1rem 0 0 1rem;
    padding: 0;
    line-height: 1.55;
    font-size: 0.92rem;
}

.chat-title {
    color: var(--cyan);
    font-size: 1.22rem;
    font-weight: 800;
    margin: 0.15rem 0 0 0;
}

.chat-bubble-user {
    width: fit-content;
    max-width: 86%;
    margin: 0.28rem 0 0.28rem auto;
    padding: 0.48rem 0.7rem;
    background: #15377f;
    border-radius: 13px 13px 3px 13px;
    color: #f1f6ff;
    line-height: 1.45;
    font-size: 0.91rem;
}

.chat-bubble-ai {
    width: fit-content;
    max-width: 92%;
    margin: 0.28rem auto 0.28rem 0;
    padding: 0.48rem 0.7rem;
    background: #0d2156;
    border: 1px solid rgba(122, 170, 255, 0.15);
    border-radius: 13px 13px 13px 3px;
    color: #dbe8ff;
    line-height: 1.45;
    font-size: 0.91rem;
}

div[data-testid="stForm"] {
    border: 0;
    padding: 0;
    margin-top: 0.2rem;
}

div[data-testid="stTextInput"] {
    margin-bottom: 0;
}

div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    min-height: 2.35rem;
    border-radius: 9px;
}

hr {
    border: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    margin: 0.55rem 0;
}

@media (max-width: 1100px) {
    .block-container {
        padding-left: 0.65rem;
        padding-right: 0.65rem;
    }

    .dashboard-title,
    .side-title,
    .section-label {
        font-size: 1.85rem;
    }

    .main-top-offset {
        height: 0.75rem;
    }

    .side-top-offset {
        height: 0.75rem;
    }
}

/* 手机端采用真实响应式布局，不再遮挡页面，也不再整体缩放 */
.mobile-layout-note {
    display: none;
}

@media screen and (max-width: 900px) {
    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

    .block-container {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0.35rem 0.55rem 1rem 0.55rem !important;
        transform: none !important;
    }

    /* 手机端让各组列自然纵向排列，所有内容都能通过滚动查看 */
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        flex-wrap: nowrap !important;
        gap: 0.45rem !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    .main-top-offset,
    .side-top-offset {
        height: 0 !important;
    }

    .dashboard-title {
        font-size: clamp(1.9rem, 8vw, 2.65rem) !important;
        line-height: 1.08 !important;
        letter-spacing: -0.035em !important;
    }

    .side-title,
    .section-label {
        font-size: clamp(1.45rem, 6vw, 2rem) !important;
        line-height: 1.1 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.28rem !important;
    }

    .dashboard-subtitle {
        margin: 0.28rem 0 0.5rem 0 !important;
        font-size: 0.92rem !important;
        line-height: 1.55 !important;
    }

    [data-testid="stMetric"] {
        width: 100% !important;
        min-height: 72px !important;
        padding: 0.48rem 0.65rem !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
    }

    .param-grid {
        grid-template-columns: 1fr 1fr !important;
        gap: 0.38rem !important;
    }

    .param-chip {
        padding: 0.42rem 0.52rem !important;
    }

    .tip-box,
    .compact-card {
        font-size: 0.88rem !important;
        line-height: 1.5 !important;
    }

    .observation-list {
        font-size: 0.9rem !important;
        line-height: 1.55 !important;
    }

    .chat-title {
        font-size: 1.2rem !important;
    }

    .chat-bubble-ai,
    .chat-bubble-user {
        max-width: 96% !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stPlotlyChart"] {
        width: 100% !important;
        overflow: hidden !important;
    }

    .modebar {
        display: none !important;
    }

    .mobile-layout-note {
        display: block;
        margin: 0.2rem 0 0.55rem 0;
        padding: 0.52rem 0.65rem;
        color: #a8dcff;
        background: rgba(18, 48, 84, 0.72);
        border-left: 3px solid #50e7ff;
        border-radius: 8px;
        font-size: 0.82rem;
        line-height: 1.45;
    }
}

/* 横屏手机仍使用响应式页面；增加可用宽度，但允许正常上下滚动 */
@media screen and (orientation: landscape) and (max-height: 700px) and (max-width: 1200px) {
    [data-testid="stHeader"] {
        height: 2rem !important;
        min-height: 2rem !important;
    }

    .block-container {
        padding-top: 0.15rem !important;
    }

    .dashboard-title {
        font-size: 1.75rem !important;
    }

    .side-title,
    .section-label {
        font-size: 1.35rem !important;
    }

    .dashboard-subtitle {
        font-size: 0.8rem !important;
        margin-bottom: 0.3rem !important;
    }

    [data-testid="stMetric"] {
        min-height: 62px !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 物理模型
# =========================================================
HBAR = 1.0


def transmission(E: float, V0: float, a: float, m: float) -> float:
    """计算矩形势垒的近似透射率。"""
    if E < V0:
        kappa = np.sqrt(2.0 * m * (V0 - E)) / HBAR
        value = np.exp(-2.0 * kappa * a)
    else:
        k2 = np.sqrt(max(2.0 * m * (E - V0), 1e-9)) / HBAR
        denominator = 1.0 + 0.08 * (V0**2 / max(E, 1e-9)) * (
            np.sin(k2 * a) ** 2
        )
        value = 1.0 / denominator

    return float(np.clip(value, 0.0, 1.0))


def calculate_wave_data(
    E: float,
    V0: float,
    a: float,
    m: float,
    show_prob: bool = False,
) -> dict:
    """
    生成三段连续的波函数可视化数据。

    E < V0 时：
    - 入射区使用余弦波，使 x=0 处振幅为 A；
    - 势垒区使用 A·exp(-κx)；
    - 透射区振幅为 A·sqrt(T)。

    因为 T = exp(-2κa)，所以势垒右边界振幅
    A·exp(-κa) 与 A·sqrt(T) 完全一致，三段曲线连续。
    """
    T = transmission(E, V0, a, m)
    R = 1.0 - T

    x_min, x_max = -2.0, 5.0
    x1, x2 = 0.0, float(a)

    x_left = np.linspace(x_min, x1, 420, endpoint=True)
    x_mid = np.linspace(x1, x2, max(100, int(150 * a)), endpoint=True)
    x_right = np.linspace(x2, x_max, 720, endpoint=True)

    baseline = float(E)
    amplitude_left = 1.75
    amplitude_right = amplitude_left * np.sqrt(max(T, 1e-12))
    k_visible = 2.8 * np.pi

    psi_left = amplitude_left * np.cos(k_visible * (x_left - x1))

    if E < V0:
        kappa = np.sqrt(2.0 * m * (V0 - E)) / HBAR
        psi_mid = amplitude_left * np.exp(-kappa * (x_mid - x1))
        psi_right = amplitude_right * np.cos(k_visible * (x_right - x2))
    else:
        kappa = 0.0
        k_inside = max(
            0.85 * np.pi,
            2.0 * np.pi * np.sqrt(max(E - V0, 1e-9) / max(E, 1e-9)),
        )
        progress = (x_mid - x1) / max(x2 - x1, 1e-9)
        envelope_mid = amplitude_left + (
            amplitude_right - amplitude_left
        ) * progress
        psi_mid = envelope_mid * np.cos(k_inside * (x_mid - x1))
        phase_at_exit = k_inside * (x2 - x1)
        psi_right = amplitude_right * np.cos(
            k_visible * (x_right - x2) + phase_at_exit
        )

    y_left = baseline + psi_left
    y_mid = baseline + psi_mid
    y_right = baseline + psi_right

    result = {
        "T": T,
        "R": R,
        "x_min": x_min,
        "x_max": x_max,
        "x1": x1,
        "x2": x2,
        "x_left": x_left,
        "x_mid": x_mid,
        "x_right": x_right,
        "y_left": y_left,
        "y_mid": y_mid,
        "y_right": y_right,
        "kappa": kappa,
    }

    if show_prob:
        probability_scale = 0.22
        result["p_left"] = baseline + probability_scale * psi_left**2
        result["p_mid"] = baseline + probability_scale * psi_mid**2
        result["p_right"] = baseline + probability_scale * psi_right**2

    return result


# =========================================================
# 本地助教与可选 API
# =========================================================
def local_tutor_reply(
    question: str,
    E: float,
    V0: float,
    a: float,
    m: float,
    T: float,
) -> str:
    q = question.strip().lower()

    if not q:
        return "可以询问量子隧穿、势垒高度、势垒宽度、粒子质量或当前透射率。"

    if "什么是隧穿" in question or "量子隧穿" in question:
        return (
            "量子隧穿来源于微观粒子的波动性。即使粒子能量低于势垒高度，"
            "波函数仍会进入势垒并指数衰减，因此势垒另一侧仍存在有限的透射概率。"
        )

    if "宽" in question or "宽度" in question:
        return (
            f"当前势垒宽度 a={a:.2f}。在 E<V₀ 时，T≈exp(-2κa)，"
            "宽度增大会直接增加指数衰减距离，因此透射率快速下降。"
        )

    if "高" in question or "高度" in question or "v0" in q:
        return (
            f"当前 E={E:.2f}、V₀={V0:.2f}。V₀-E 增大时 κ 增大，"
            "势垒内波函数衰减更快，透射率随之下降。"
        )

    if "质量" in question or q == "m":
        return (
            f"当前质量 m={m:.2f}。κ 与 √m 成正比，因此质量越大，"
            "势垒内衰减越快，量子隧穿越困难。"
        )

    if "透射率" in question and ("怎么算" in question or "计算" in question):
        return (
            "当 E<V₀ 时，本平台采用 T≈exp(-2κa)，"
            "其中 κ=√[2m(V₀-E)]/ℏ。"
        )

    if "当前" in question or "现在" in question:
        region = "典型量子隧穿区间" if E < V0 else "高于势垒的传播区间"
        return (
            f"当前 E={E:.2f}、V₀={V0:.2f}、a={a:.2f}、m={m:.2f}，"
            f"属于{region}，透射率约为 {T * 100:.4f}%。"
        )

    return (
        "可询问：量子隧穿的含义、势垒高度或宽度的影响、"
        "粒子质量的作用，以及当前参数对应的物理状态。"
    )


def call_openai_compatible(messages: list[dict[str, str]]) -> str:
    api_base = os.getenv("OPENAI_API_BASE", "").rstrip("/")
    api_key = os.getenv("OPENAI_API_KEY", "")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_base or not api_key:
        raise RuntimeError("未配置 OPENAI_API_BASE 或 OPENAI_API_KEY")

    response = requests.post(
        f"{api_base}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": 0.4,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"]


def tutor_reply(
    question: str,
    E: float,
    V0: float,
    a: float,
    m: float,
    T: float,
    use_api: bool,
    history: list[dict[str, str]],
) -> str:
    system_prompt = (
        "你是一名面向中学生和大学低年级学生的量子力学助教。"
        "请使用中文，结合当前参数清晰、直观、简洁地解释量子隧穿。"
        f"当前参数：E={E:.3f}, V0={V0:.3f}, a={a:.3f}, "
        f"m={m:.3f}, T={T:.6f}。"
    )

    if use_api:
        try:
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history[-6:])
            messages.append({"role": "user", "content": question})
            return call_openai_compatible(messages)
        except Exception:
            pass

    return local_tutor_reply(question, E, V0, a, m, T)


# =========================================================
# 会话状态
# =========================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "你好，我是量子助教·Q。可以询问量子隧穿、势垒参数、"
                "透射率或当前图像所表示的物理状态。"
            ),
        }
    ]


# =========================================================
# 侧边栏：参数设置
# =========================================================
with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">参数设置</div>',
        unsafe_allow_html=True,
    )

    E = st.slider("粒子能量 E", 0.2, 12.0, 3.4, 0.1)
    V0 = st.slider("势垒高度 V₀", 0.5, 20.0, 14.4, 0.1)
    a = st.slider("势垒宽度 a", 0.05, 2.0, 0.69, 0.01)
    m = st.slider("粒子质量 m", 0.2, 5.0, 0.4, 0.1)

    show_prob = st.toggle("显示 |ψ|²", value=False)
    use_api = st.toggle("AI 助教使用真实 API（已配置时）", value=False)

    components.html(
        """
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
html, body {
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.wrap {
    display: grid;
    gap: 6px;
}
button {
    width: 100%;
    min-height: 38px;
    border: 1px solid rgba(80, 231, 255, 0.42);
    border-radius: 9px;
    color: #e9fbff;
    background: linear-gradient(135deg, #102a58, #0b1733);
    font-size: 14px;
    cursor: pointer;
}
button:active {
    transform: scale(0.99);
}
#status {
    min-height: 17px;
    color: #9fd8ff;
    font-size: 11px;
    line-height: 1.35;
}
</style>
</head>
<body>
<div class="wrap">
    <button id="landscapeButton">手机端：尝试全屏横屏</button>
    <div id="status">部分应用内置浏览器不支持锁定方向，失败时页面仍可竖屏滚动使用。</div>
</div>
<script>
const button = document.getElementById("landscapeButton");
const status = document.getElementById("status");

button.addEventListener("click", async () => {
    status.textContent = "正在请求全屏和横屏…";

    try {
        const parentDocument = window.parent.document;
        const root = parentDocument.documentElement;

        if (root.requestFullscreen) {
            await root.requestFullscreen();
        } else if (root.webkitRequestFullscreen) {
            root.webkitRequestFullscreen();
        }

        const orientation =
            window.parent.screen?.orientation ||
            window.screen?.orientation;

        if (orientation?.lock) {
            await orientation.lock("landscape");
            status.textContent = "已请求横屏。若未旋转，请手动旋转手机。";
        } else {
            status.textContent = "当前浏览器不支持自动锁定横屏，请手动旋转手机。";
        }
    } catch (error) {
        status.textContent =
            "浏览器拒绝自动横屏。请使用系统浏览器打开，或直接竖屏滚动查看。";
    }
});
</script>
</body>
</html>
""",
        height=72,
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-label" style="font-size:1.05rem;">教学提示</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
- 增大 **V₀**：衰减更快  
- 增大 **a**：衰减距离更长  
- 增大 **m**：隧穿更困难  
- 增大 **E**：透射率通常升高
"""
    )


# =========================================================
# 数据计算
# =========================================================
wave = calculate_wave_data(E, V0, a, m, show_prob)
T = wave["T"]
R = wave["R"]


# =========================================================
# 主体：左侧图表与右侧控制面板从同一顶部开始
# =========================================================
main_col, side_col = st.columns([2.72, 1.08], gap="small")

with main_col:
    st.markdown(
        '<div class="main-top-offset"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="dashboard-title">量子隧穿效应 可视化</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="dashboard-subtitle">
调节参数，观察波函数与透射率如何随势垒高度、宽度、粒子能量和质量变化。
</div>
<div class="mobile-layout-note">
手机竖屏和横屏均可直接使用。页面内容会按顺序排列，可上下滚动查看；
需要横屏时可在参数侧栏点击“尝试全屏横屏”。
</div>
""",
        unsafe_allow_html=True,
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[
                wave["x_min"],
                wave["x1"],
                wave["x1"],
                wave["x2"],
                wave["x2"],
                wave["x_max"],
            ],
            y=[0, 0, V0, V0, 0, 0],
            mode="lines",
            line=dict(color="#00d9ff", width=3.5),
            name="势垒 (V₀)",
            hovertemplate="x=%{x:.2f}<br>V=%{y:.2f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[wave["x_min"], wave["x_max"]],
            y=[E, E],
            mode="lines",
            line=dict(color="#ff2f92", width=2.5, dash="dash"),
            name="粒子能量 (E)",
            hovertemplate=f"E={E:.2f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=wave["x_left"],
            y=wave["y_left"],
            mode="lines",
            line=dict(color="#39ff14", width=3),
            name="Re(ψ)",
            hovertemplate="x=%{x:.2f}<br>Re(ψ)=%{y:.3f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=wave["x_mid"],
            y=wave["y_mid"],
            mode="lines",
            line=dict(color="#ff414d", width=3),
            name="势垒内衰减波",
            hovertemplate="x=%{x:.2f}<br>Re(ψ)=%{y:.3f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=wave["x_right"],
            y=wave["y_right"],
            mode="lines",
            line=dict(color="#39ff14", width=3),
            showlegend=False,
            hovertemplate="x=%{x:.2f}<br>Re(ψ)=%{y:.3f}<extra></extra>",
        )
    )

    if show_prob:
        fig.add_trace(
            go.Scatter(
                x=wave["x_left"],
                y=wave["p_left"],
                mode="lines",
                line=dict(color="#ffd400", width=2, dash="dot"),
                name="|ψ|²",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=wave["x_mid"],
                y=wave["p_mid"],
                mode="lines",
                line=dict(color="#ffd400", width=2, dash="dot"),
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=wave["x_right"],
                y=wave["p_right"],
                mode="lines",
                line=dict(color="#ffd400", width=2, dash="dot"),
                showlegend=False,
            )
        )

    annotation_offset = max(1.15, min(2.0, V0 * 0.12))
    fig.add_annotation(
        x=-1.15,
        y=E + annotation_offset,
        text="入射区",
        showarrow=False,
        font=dict(color="white", size=16),
    )
    fig.add_annotation(
        x=(wave["x1"] + wave["x2"]) / 2.0,
        y=V0 + max(0.45, V0 * 0.035),
        text="势垒区",
        showarrow=False,
        font=dict(color="#ff5b61", size=16),
    )
    fig.add_annotation(
        x=3.7,
        y=E + annotation_offset,
        text="透射区",
        showarrow=False,
        font=dict(color="white", size=16),
    )

    y_min = min(0.0, E - 2.35)
    y_max = max(V0 + 1.15, E + 2.35)

    fig.update_layout(
        height=405,
        margin=dict(l=12, r=12, t=8, b=8),
        paper_bgcolor="rgba(5,10,20,1)",
        plot_bgcolor="rgba(3,8,18,1)",
        font=dict(color="#dffcff", size=13),
        hovermode="x unified",
        legend=dict(
            x=0.985,
            y=0.985,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(13,26,42,0.82)",
            bordercolor="rgba(0,255,255,0.22)",
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(
            title="位置 x",
            range=[wave["x_min"], wave["x_max"]],
            showgrid=True,
            gridcolor="rgba(0,255,255,0.07)",
            zeroline=False,
        ),
        yaxis=dict(
            title="能量 / 波函数幅值",
            range=[y_min, y_max],
            showgrid=True,
            gridcolor="rgba(0,255,255,0.055)",
            zeroline=False,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToRemove": [
                "lasso2d",
                "select2d",
                "autoScale2d",
            ],
        },
    )

    chat_header_col, clear_col = st.columns([5.4, 1.0])
    with chat_header_col:
        st.markdown(
            '<div class="chat-title">量子助教 · Q</div>',
            unsafe_allow_html=True,
        )
    with clear_col:
        if st.button("清空", use_container_width=True):
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": (
                        "你好，我是量子助教·Q。可以询问量子隧穿、势垒参数、"
                        "透射率或当前图像所表示的物理状态。"
                    ),
                }
            ]
            st.rerun()

    with st.container(height=126, border=True):
        for message in st.session_state.chat_history[-5:]:
            safe_content = html.escape(message["content"]).replace("\n", "<br>")
            css_class = (
                "chat-bubble-user"
                if message["role"] == "user"
                else "chat-bubble-ai"
            )
            st.markdown(
                f'<div class="{css_class}">{safe_content}</div>',
                unsafe_allow_html=True,
            )

    with st.form("chat_form", clear_on_submit=True):
        input_col, send_col = st.columns([6.0, 1.0])
        with input_col:
            question = st.text_input(
                "向 AI 助教提问",
                placeholder="例如：为什么势垒越宽，透射率越低？",
                label_visibility="collapsed",
            )
        with send_col:
            submitted = st.form_submit_button(
                "发送",
                use_container_width=True,
            )

    if submitted and question.strip():
        clean_question = question.strip()
        previous_history = list(st.session_state.chat_history)
        st.session_state.chat_history.append(
            {"role": "user", "content": clean_question}
        )
        answer = tutor_reply(
            clean_question,
            E,
            V0,
            a,
            m,
            T,
            use_api,
            previous_history,
        )
        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )
        st.rerun()


with side_col:
    st.markdown(
        '<div class="side-top-offset"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="side-title">可视化控制面板</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="height:0.62rem;"></div>',
        unsafe_allow_html=True,
    )

    metric_col_1, metric_col_2 = st.columns(2)
    with metric_col_1:
        st.metric("透射率 T", f"{T * 100:.3f}%")
    with metric_col_2:
        st.metric("反射率 R", f"{R * 100:.3f}%")

    st.markdown(
        '<div class="section-label">当前参数</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class="param-grid">
    <div class="param-chip">E<br><code>{E:.2f}</code></div>
    <div class="param-chip">V₀<br><code>{V0:.2f}</code></div>
    <div class="param-chip">a<br><code>{a:.2f}</code></div>
    <div class="param-chip">m<br><code>{m:.2f}</code></div>
</div>
""",
        unsafe_allow_html=True,
    )

    if E < V0:
        st.markdown(
            """
<div class="tip-box">
当前处于 <b>E &lt; V₀</b> 区域。红色曲线在势垒内指数衰减，
右侧仍保留振幅较小的透射波。
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
<div class="tip-box">
当前处于 <b>E ≥ V₀</b> 区域。势垒内波函数保持振荡，
粒子更容易越过势垒。
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-label">教学观察点</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<ol class="observation-list">
    <li>势垒越高，透射波越弱</li>
    <li>势垒越宽，衰减越明显</li>
    <li>粒子质量越大，越难隧穿</li>
    <li>粒子能量越高，通常越容易透射</li>
</ol>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">结论速览</div>',
        unsafe_allow_html=True,
    )

    if E < V0:
        st.markdown(
            f"""
<div class="compact-card" style="font-size:0.9rem; line-height:1.48;">
当前属于 <b>量子隧穿情形</b>：粒子能量
<code>E = {E:.2f}</code> 小于势垒高度
<code>V₀ = {V0:.2f}</code>，但粒子仍有约
<b style="color:#39ff14;">{T * 100:.4f}%</b> 的概率通过势垒。
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
<div class="compact-card" style="font-size:0.9rem; line-height:1.48;">
当前粒子能量 <code>E = {E:.2f}</code> 已经不小于势垒高度
<code>V₀ = {V0:.2f}</code>，粒子更容易通过势垒，
当前透射率约为
<b style="color:#39ff14;">{T * 100:.4f}%</b>。
</div>
""",
            unsafe_allow_html=True,
        )
