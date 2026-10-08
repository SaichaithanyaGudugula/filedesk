import html
from datetime import datetime
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------- setup
st.set_page_config(page_title="FileDesk", page_icon="🗂️", layout="wide")

WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

INK = "#14213D"
BLUE = "#2F5DFF"
AMBER = "#FFB703"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, .stApp {{ font-family: 'Manrope', sans-serif; }}
    .stApp {{ background: #EEF2F7; color: {INK}; }}
    #MainMenu, footer {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{ background: transparent; }}
    .block-container {{ padding-top: 2rem; max-width: 1150px; }}

    /* sidebar */
    section[data-testid="stSidebar"] {{ background: {INK}; }}
    section[data-testid="stSidebar"] * {{ color: #E6ECF7; }}
    .brand {{ font-size: 1.5rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.2rem; }}
    .brand-sub {{ font-size: 0.85rem; opacity: 0.7; margin-bottom: 1.2rem; }}

    /* hero: folder-tab motif */
    .hero-wrap {{ margin-bottom: 1.4rem; }}
    .hero-tab {{
        display: inline-block; background: {AMBER}; color: {INK};
        font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 500;
        padding: 6px 18px; border-radius: 10px 10px 0 0;
    }}
    .hero {{
        background: {INK}; color: #fff; padding: 28px 32px;
        border-radius: 0 16px 16px 16px;
    }}
    .hero h1 {{ margin: 0; font-size: 2.3rem; font-weight: 800; letter-spacing: -0.03em; color: #fff; }}
    .hero p {{ margin: 6px 0 0 0; opacity: 0.75; font-size: 1rem; }}

    /* metrics */
    div[data-testid="stMetric"] {{
        background: #fff; border: 1px solid #D8E0EC; border-radius: 12px; padding: 14px 18px;
    }}

    /* buttons */
    div.stButton > button, div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stDownloadButton"] > button {{
        background: {BLUE}; color: #fff; border: none; border-radius: 10px;
        font-weight: 600; padding: 0.55rem 1.3rem;
    }}
    div.stButton > button p, div[data-testid="stFormSubmitButton"] > button p,
    div[data-testid="stDownloadButton"] > button p {{ color: #fff; }}
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {{ background: #1F46D6; }}
    div.stButton > button:focus-visible, div[data-testid="stFormSubmitButton"] > button:focus-visible {{
        outline: 3px solid {AMBER}; outline-offset: 2px;
    }}

    /* forms and panels */
    div[data-testid="stForm"] {{
        background: #fff; border: 1px solid #D8E0EC; border-radius: 14px; padding: 20px;
    }}
    .panel-title {{ font-size: 1.25rem; font-weight: 800; letter-spacing: -0.01em; margin-bottom: 0.2rem; }}
    .panel-sub {{ color: #5B6B88; margin-bottom: 1rem; }}

    /* file list */
    .files {{ background: #fff; border: 1px solid #D8E0EC; border-radius: 14px; padding: 8px 6px; }}
    .files-head {{ font-weight: 800; padding: 10px 14px 6px 14px; }}
    .frow {{
        display: flex; justify-content: space-between; gap: 10px;
        padding: 9px 14px; border-top: 1px solid #EEF2F7;
    }}
    .fname {{ font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; overflow-wrap: anywhere; }}
    .fmeta {{ color: #5B6B88; font-size: 0.8rem; white-space: nowrap; }}
    .empty {{ color: #5B6B88; padding: 14px; }}

    @media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- helpers
def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def safe_path(name: str):
    """Keep every file inside the workspace folder (blocks ../ tricks)."""
    name = Path(name.strip()).name
    if not name:
        return None
    if not Path(name).suffix:
        name += ".txt"
    return WORKSPACE / name


def list_files():
    return sorted((p for p in WORKSPACE.iterdir() if p.is_file()), key=lambda p: p.name.lower())


def flash(message: str, icon: str = "✅"):
    st.session_state["flash"] = (message, icon)


def panel(title: str, subtitle: str):
    st.markdown(
        f'<div class="panel-title">{title}</div><div class="panel-sub">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def empty_state(action: str):
    st.info(f"No files yet. {action}")


# ---------------------------------------------------------------- actions
def create_view():
    panel("Create a file", "Name it, write something, and save it to your workspace.")
    with st.form("create_form", clear_on_submit=True):
        name = st.text_input("File name", placeholder="notes.txt")
        data = st.text_area("Content", height=180, placeholder="Start writing...")
        submitted = st.form_submit_button("Create file")
    if submitted:
        path = safe_path(name)
        if path is None:
            st.error("Enter a file name to continue.")
        elif path.exists():
            st.error(f"{path.name} already exists. Choose another name, or use Update to change it.")
        else:
            try:
                path.write_text(data, encoding="utf-8")
                flash(f"Created {path.name}")
                st.rerun()
            except Exception as err:
                st.error(f"Could not create the file: {err}")


def read_view():
    panel("Read a file", "Pick a file to see what is inside.")
    files = list_files()
    if not files:
        return empty_state("Use Create to add your first file.")
    choice = st.selectbox("File", [p.name for p in files])
    path = WORKSPACE / choice
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as err:
        return st.error(f"Could not read {choice}: {err}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Characters", len(content))
    c2.metric("Words", len(content.split()))
    c3.metric("Lines", len(content.splitlines()))
    if content:
        st.code(content, language=None, wrap_lines=True)
    else:
        st.warning("This file is empty.")
    st.download_button("Download file", content, file_name=choice)


def update_view():
    panel("Update a file", "Rename it, add to the end, or replace everything.")
    files = list_files()
    if not files:
        return empty_state("Use Create to add a file first.")
    choice = st.selectbox("File", [p.name for p in files])
    path = WORKSPACE / choice

    tab_rename, tab_append, tab_over = st.tabs(["Rename", "Append", "Overwrite"])

    with tab_rename:
        with st.form("rename_form"):
            new_name = st.text_input("New file name", value=choice)
            go = st.form_submit_button("Rename file")
        if go:
            new_path = safe_path(new_name)
            if new_path is None:
                st.error("Enter a new file name.")
            elif new_path.exists():
                st.error(f"{new_path.name} already exists. Choose a different name.")
            else:
                path.rename(new_path)
                flash(f"Renamed to {new_path.name}")
                st.rerun()

    with tab_append:
        with st.form("append_form", clear_on_submit=True):
            extra = st.text_area("Text to add at the end", height=130)
            go = st.form_submit_button("Append text")
        if go:
            with open(path, "a", encoding="utf-8") as fs:
                fs.write(" " + extra)
            flash(f"Appended to {choice}")
            st.rerun()

    with tab_over:
        current = path.read_text(encoding="utf-8", errors="replace")
        with st.form("overwrite_form"):
            new_text = st.text_area("New content (replaces the old content)", value=current, height=180)
            go = st.form_submit_button("Overwrite file")
        if go:
            path.write_text(new_text, encoding="utf-8")
            flash(f"Overwrote {choice}")
            st.rerun()


def delete_view():
    panel("Delete a file", "This removes the file for good.")
    files = list_files()
    if not files:
        return empty_state("There is nothing to delete.")
    choice = st.selectbox("File", [p.name for p in files])
    sure = st.checkbox(f"Yes, delete {choice}")
    if st.button("Delete file", disabled=not sure):
        (WORKSPACE / choice).unlink()
        flash(f"Deleted {choice}", "🗑️")
        st.rerun()


# ---------------------------------------------------------------- layout
if "flash" in st.session_state:
    msg, icon = st.session_state.pop("flash")
    st.toast(msg, icon=icon)

with st.sidebar:
    st.markdown('<div class="brand">FileDesk</div><div class="brand-sub">Manage text files from your browser</div>', unsafe_allow_html=True)
    page = st.radio(
        "Action",
        ["Create", "Read", "Update", "Delete"],
        label_visibility="collapsed",
    )

st.markdown(
    """
    <div class="hero-wrap">
      <span class="hero-tab">workspace/</span>
      <div class="hero">
        <h1>FileDesk</h1>
        <p>Create, read, update and delete files without touching the terminal.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

files = list_files()
total = sum(p.stat().st_size for p in files)
latest = max((p.stat().st_mtime for p in files), default=None)

m1, m2, m3 = st.columns(3)
m1.metric("Files", len(files))
m2.metric("Total size", human_size(total))
m3.metric("Last change", datetime.fromtimestamp(latest).strftime("%d %b, %H:%M") if latest else "None yet")

st.write("")
main, side = st.columns([2, 1], gap="large")

with main:
    {"Create": create_view, "Read": read_view, "Update": update_view, "Delete": delete_view}[page]()

with side:
    rows = "".join(
        f'<div class="frow"><span class="fname">{html.escape(p.name)}</span>'
        f'<span class="fmeta">{human_size(p.stat().st_size)}</span></div>'
        for p in list_files()
    ) or '<div class="empty">Your files will appear here.</div>'
    st.markdown(f'<div class="files"><div class="files-head">Your files</div>{rows}</div>', unsafe_allow_html=True)
