import streamlit as st
import os
import sys
import io
import re
import datetime
import PyPDF2
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Add the parent directory to sys.path to allow importing the 'runtime' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from runtime.pipeline import run_pipeline

st.set_page_config(page_title="CineSafe Agent", page_icon="🎬", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1a1c24;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 CineSafe Agent")
st.subheader("Your Git-Native AI Production Analyst")

# Sidebar for Config
with st.sidebar:
    st.header("⚙️ Configuration")
    scenario = st.selectbox(
        "Scenario Preset",
        ["standard", "budget_cut_20", "accelerate_timeline", "max_safety"],
        help="Test your production plan against specific constraints."
    )
    
    st.divider()
    st.info("Powered by **Gemini 2.5 Flash** and the GitAgent Standard.")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text

# Input Area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Screenplay Input")
    input_type = st.radio("Input Method", ["Upload File", "Paste Text"], horizontal=True)
    
    script_text = ""
    if input_type == "Upload File":
        uploaded_file = st.file_uploader("Upload your screenplay (.txt, .pdf)", type=["txt", "pdf"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".pdf"):
                script_text = extract_text_from_pdf(uploaded_file)
            else:
                script_text = uploaded_file.read().decode("utf-8")
    else:
        script_text = st.text_area("Paste your script content here...", height=300)

with col2:
    st.markdown("### 🚀 Action")
    if st.button("Run Production Analysis", type="primary", use_container_width=True):
        if not script_text:
            st.error("Please provide a screenplay first.")
        else:
            with st.spinner("Analyzing with Gemini..."):
                try:
                    # 1. Run Pipeline
                    report = run_pipeline(script_text, scenario_preset=scenario)
                    
                    if report.scene_count == 0:
                        st.warning("⚠️ No scene headings detected (INT. / EXT.). Showing text preview below.")
                        with st.expander("Extracted Text Preview (First 1000 chars)"):
                            st.text(script_text[:1000])
                    
                    st.session_state['report'] = report
                    st.success("Analysis Complete!")
                except Exception as e:
                    st.error(f"Error: {e}")

# Results Area
if 'report' in st.session_state:
    report = st.session_state['report']
    
    st.divider()
    
    # KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Total Scenes", report.scene_count)
    with kpi2:
        avg_risk = sum(r.overall_risk_score for r in report.top_risks) / len(report.top_risks) if report.top_risks else 0
        st.metric("Average Risk", f"{avg_risk:.1f}/10")
    with kpi3:
        st.metric("Scenario", scenario.replace("_", " ").title())

    # Full Report
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Markdown Report", "🔍 Intermediate Data", "📜 Production Logs", "📥 Download"])
    
    with tab1:
        st.markdown(report.markdown)
        
    with tab2:
        st.json({
            "top_risks": [vars(r) for r in report.top_risks],
            "budget_hotspots": [vars(b) for b in report.top_budget_hotspots]
        })
    
    with tab3:
        from runtime.utils.logger import logger
        log_text = "\n".join(logger.get_logs())
        st.text_area("Execution Details", log_text, height=400)
        
    with tab4:
        st.markdown("### 📄 Download Production Report as PDF")
        
        def generate_pdf(report_text, scene_count, avg_risk, scenario_preset):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                    rightMargin=20*mm, leftMargin=20*mm,
                                    topMargin=20*mm, bottomMargin=20*mm)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle('Title', parent=styles['Title'],
                                         fontSize=22, textColor=colors.HexColor('#e74c3c'),
                                         spaceAfter=6)
            story.append(Paragraph("🎬 CineSafe Production Report", title_style))
            story.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%B %d, %Y %H:%M')}",
                                   styles['Normal']))
            story.append(Spacer(1, 5*mm))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e74c3c')))
            story.append(Spacer(1, 5*mm))

            # Key Metrics
            metrics_style = ParagraphStyle('Metrics', parent=styles['Normal'],
                                           fontSize=11, spaceAfter=4)
            story.append(Paragraph(f"<b>Total Scenes:</b> {scene_count}", metrics_style))
            story.append(Paragraph(f"<b>Average Risk:</b> {avg_risk:.1f}/10", metrics_style))
            story.append(Paragraph(f"<b>Scenario Preset:</b> {scenario_preset.replace('_', ' ').title()}", metrics_style))
            story.append(Spacer(1, 5*mm))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
            story.append(Spacer(1, 5*mm))

            # Report Body - parse markdown to paragraphs
            body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, spaceAfter=3)
            heading1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14, spaceAfter=4)
            heading2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11, spaceAfter=3)

            for line in report_text.split('\n'):
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 2*mm))
                elif line.startswith('## '):
                    story.append(Paragraph(line[3:], heading1_style))
                elif line.startswith('### '):
                    story.append(Paragraph(line[4:], heading2_style))
                elif line.startswith('**') and line.endswith('**'):
                    story.append(Paragraph(f"<b>{line[2:-2]}</b>", body_style))
                elif line.startswith('- '):
                    # Strip markdown bold/italic for bullets
                    clean = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line[2:])
                    story.append(Paragraph(f"• {clean}", body_style))
                else:
                    clean = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                    if clean:
                        story.append(Paragraph(clean, body_style))

            doc.build(story)
            buffer.seek(0)
            return buffer

        avg_risk_val = sum(r.overall_risk_score for r in report.top_risks) / len(report.top_risks) if report.top_risks else 0
        pdf_buffer = generate_pdf(report.markdown, report.scene_count, avg_risk_val, scenario)

        st.download_button(
            label="⬇️ Download Full Report (PDF)",
            data=pdf_buffer,
            file_name="cinesafe_production_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
else:
    st.info("Provide a screenplay and click 'Run Production Analysis' to see results.")
