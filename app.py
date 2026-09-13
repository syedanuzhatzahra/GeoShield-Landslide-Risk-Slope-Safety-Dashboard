import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import math

# Page Setup
st.set_page_config(page_title="GeoShield Dashboard", layout="wide")

# ==============================================================================
# 1. PDF REPORT GENERATOR
# ==============================================================================
def generate_pdf_report(title, mode_name, status_text, recs_text, inputs_dict):
    filename = f"GeoShield_{mode_name.replace(' ', '_')}_Report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    header_style = ParagraphStyle('HeaderStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1A365D'), spaceAfter=6)
    sub_header_style = ParagraphStyle('SubHeaderStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#4A5568'), spaceAfter=15)

    story.append(Paragraph("<b>GeoShield: Geological Hazard & Slope Safety Report</b>", header_style))
    story.append(Paragraph(f"<b>Assessment Level:</b> {title} | <b>Generated Mode:</b> {mode_name}", sub_header_style))
    story.append(Spacer(1, 10))

    status_style = ParagraphStyle('StatusStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#2B6CB0'))
    story.append(Paragraph(f"<b>Assessment Result:</b> {status_text}", status_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Field Parameters & Calculations Summary:</b>", styles['Heading3']))
    table_data = [["Parameter", "Input Value / Evaluated Metric"]]
    for key, value in inputs_dict.items():
        table_data.append([str(key), str(value)])

    param_table = Table(table_data, colWidths=[220, 250])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2B6CB0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(param_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Actionable Recommendations & Mitigation Plan:</b>", styles['Heading3']))
    formatted_recs = recs_text.replace('\n', '<br/>')
    story.append(Paragraph(formatted_recs, styles['Normal']))

    doc.build(story)
    return filename

# Header
st.title("🛡️ GeoShield: Landslide Risk & Slope Safety Dashboard")
st.caption("An automated geological hazard screening and slope stability evaluation tool.")

tab1, tab2 = st.tabs(["🧑‍🌾 Tier-1: Rapid Field Screening", "👷 Tier-2: Advanced Geotechnical Analysis"])

# ==============================================================================
# TAB 1: TIER-1 RAPID FIELD SCREENING
# ==============================================================================
with tab1:
    st.subheader("Rapid Observation-Based Hazard Index")
    col1, col2 = st.columns(2)
    with col1:
        slope_b = st.selectbox("1. Slope Geometry", ["Flat / Gentle Slope (<15°)", "Moderate Slope (15°-35°)", "Steep Slope / Cliff (>35°)"])
        cracks_b = st.radio("3. Visible Ground Cracks?", ["No", "Yes"])
    with col2:
        veg_b = st.selectbox("2. Vegetation Cover", ["Dense Trees / Vegetation", "Sparse Grass / Shrubs", "Bare Soil / Barren Rock"])
        seepage_b = st.radio("4. Active Water Seepage?", ["No", "Yes"])

    rain_b = st.radio("5. Rainfall Condition", ["No / Light Rain", "Moderate Rain", "Heavy / Continuous Rain"])

    if st.button("Evaluate Tier-1 Risk & Generate Report", type="primary"):
        score = 0
        if slope_b == "Flat / Gentle Slope (<15°)": score += 5
        elif slope_b == "Moderate Slope (15°-35°)": score += 20
        elif slope_b == "Steep Slope / Cliff (>35°)": score += 35

        if veg_b == "Dense Trees / Vegetation": score -= 10
        elif veg_b == "Sparse Grass / Shrubs": score += 10
        elif veg_b == "Bare Soil / Barren Rock": score += 20

        if cracks_b == "Yes": score += 25
        if seepage_b == "Yes": score += 15

        if rain_b == "Heavy / Continuous Rain": score += 25
        elif rain_b == "Moderate Rain": score += 15

        score = max(0, min(100, score))

        inputs_dict = {
            "Slope Geometry": slope_b, "Vegetation Cover": veg_b,
            "Visible Ground Cracks": cracks_b, "Water Seepage / Wetness": seepage_b,
            "Rainfall Condition": rain_b, "Landslide Risk Score": f"{score} / 100"
        }

        if score < 35:
            status = f"🟢 Low Hazard Risk (Score: {score}/100)"
            recs = "• Site is currently STABLE under observation.\n• Keep surface drainage channels clear of debris.\n• Avoid deforestation or cutting vegetation along slope toe."
            st.success(status)
        elif score < 65:
            status = f"🟡 Moderate Hazard Risk (Score: {score}/100)"
            recs = "• CAUTION: Slope is vulnerable during active precipitation.\n• Monitor tension cracks and water seepage points daily.\n• Clear drainage outlets to avoid water accumulation behind slope.\n• Prepare field evacuation protocol if rain persists."
            st.warning(status)
        else:
            status = f"🔴 High Hazard Risk (Score: {score}/100)"
            recs = "⚠️ HIGH DANGER / IMMINENT FAILURE HAZARD!\n• Immediately evacuate toe and crest zones.\n• Restrict traffic and infrastructure access near slope.\n• Notify local disaster management & response authorities instantly."
            st.error(status)

        st.info(recs)
        pdf_file = generate_pdf_report("Tier-1 Rapid Screening", "Field_Screening", status, recs, inputs_dict)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Tier-1 PDF Report", f, file_name=pdf_file, mime="application/pdf")

# ==============================================================================
# TAB 2: TIER-2 ADVANCED GEOTECHNICAL ANALYSIS
# ==============================================================================
with tab2:
    st.subheader("Material-Specific Quantitative Slope Stability")
    mat_type = st.radio("1. Material Type", ["Soil Slope", "Rock Slope"])
    
    col_a, col_b, col_c = st.columns(3)
    with col_a: H = st.number_input("Slope Height, H (m)", value=12.0)
    with col_b: beta_deg = st.number_input("Slope Angle, β (degrees)", value=32.0)
    with col_c: surcharge = st.number_input("Building / Road Surcharge, q (kPa)", value=10.0)

    if mat_type == "Soil Slope":
        st.markdown("#### 🔹 Soil Parameters")
        c1, c2 = st.columns(2)
        with c1:
            c = st.number_input("Cohesion, c' (kPa)", value=15.0)
            gamma = st.number_input("Unit Weight, γ (kN/m³)", value=19.0)
        with c2:
            phi_deg = st.number_input("Friction Angle, ϕ' (degrees)", value=28.0)
            ru = st.slider("Pore Water Pressure Ratio, ru", 0.0, 0.5, 0.2, 0.05)
    else:
        st.markdown("#### 🔸 Rock Mass Parameters")
        rmr = st.slider("Basic Rock Mass Rating (RMR)", 0, 100, 50)
        joint_orientation = st.selectbox("Discontinuity / Joint Dip Orientation", ["Favorable (Dipping Into Slope)", "Fair / Random", "Adverse (Dipping Out of Slope)"])

    if st.button("Calculate Geotechnical Stability & Generate Report", type="primary"):
        inputs_dict = {"Material Classification": mat_type, "Slope Height (H)": f"{H} m", "Slope Angle (β)": f"{beta_deg}°", "Surcharge Load (q)": f"{surcharge} kPa"}
        
        if mat_type == "Soil Slope":
            beta = math.radians(beta_deg)
            phi = math.radians(phi_deg)
            W = 0.5 * gamma * (H**2) / math.tan(beta)
            N = (W + surcharge) * math.cos(beta)
            T = (W + surcharge) * math.sin(beta)
            pore_pressure = ru * gamma * H
            effective_N = max(0, N - pore_pressure)
            resisting_force = (c * (H / math.sin(beta))) + (effective_N * math.tan(phi))
            FS = round(resisting_force / T, 3) if T > 0 else 0.0

            inputs_dict.update({"Cohesion (c')": f"{c} kPa", "Internal Friction Angle (ϕ')": f"{phi_deg}°", "Soil Unit Weight (γ)": f"{gamma} kN/m³", "Pore Water Pressure Ratio (ru)": ru, "Factor of Safety (FS)": FS})

            if FS > 1.5:
                status = f"🟢 Stable Soil Slope (Factor of Safety, FS = {FS})"
                recs = "• Slope is geotechnically STABLE under current static loads.\n• Maintain current drainage system and routine inspections."
                st.success(status)
            elif 1.0 <= FS <= 1.5:
                status = f"🟡 Marginally Stable Soil Slope (Factor of Safety, FS = {FS})"
                recs = "• MARGINALLY STABLE: Susceptible to failure during heavy rain/seismic events.\n• Install sub-surface horizontal drain pipes.\n• Apply bio-engineering solutions (e.g., Vetiver grass planting)."
                st.warning(status)
            else:
                status = f"🔴 Critical / Unstable Soil Slope (Factor of Safety, FS = {FS})"
                recs = "⚠️ CRITICAL STABILITY FAILURE (FS < 1.0)!\n• Construct retaining structures (Gabion walls / MSE walls).\n• Install structural soil nails or tie-back anchor bolts."
                st.error(status)
        else:
            joint_penalty = -25 if joint_orientation == "Adverse (Dipping Out of Slope)" else (-5 if joint_orientation == "Fair / Random" else 0)
            adjusted_rmr = rmr + joint_penalty
            inputs_dict.update({"Basic RMR Score": rmr, "Discontinuity / Joint Condition": joint_orientation, "Adjusted Rock Mass Rating": adjusted_rmr})

            if adjusted_rmr > 60:
                status = f"🟢 Good Rock Mass - Class I/II (Adjusted RMR = {adjusted_rmr})"
                recs = "• Rock mass is structurally STABLE.\n• Install spot rock bolting for isolated loose blocks."
                st.success(status)
            elif 40 <= adjusted_rmr <= 60:
                status = f"🟡 Fair Rock Mass - Class III (Adjusted RMR = {adjusted_rmr})"
                recs = "• MODERATE RISK: Potential Planar/Wedge failure along joint sets.\n• Install systematic pattern rock bolts.\n• Apply shotcrete reinforced with wire mesh."
                st.warning(status)
            else:
                status = f"🔴 Poor Rock Mass - Class IV/V (Adjusted RMR = {adjusted_rmr})"
                recs = "⚠️ HIGH ROCKFALL / TOPPLING FAILURE RISK!\n• Install heavy cable anchors and catch fencing.\n• Drill horizontal weep holes to relieve groundwater head."
                st.error(status)

        st.info(recs)
        pdf_file = generate_pdf_report("Tier-2 Geotechnical Analysis", "Geotechnical_Analysis", status, recs, inputs_dict)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Tier-2 PDF Report", f, file_name=pdf_file, mime="application/pdf")
