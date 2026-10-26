import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_path = os.path.join("doc_files", "Sustainable_Farming_and_Agronomy_Handbook.pdf")

doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    textColor=colors.HexColor('#1b4332'),
    alignment=1,
    spaceAfter=15
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=12,
    leading=16,
    textColor=colors.HexColor('#2d6a4f'),
    alignment=1,
    spaceAfter=25
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=colors.HexColor('#1b4332'),
    spaceBefore=14,
    spaceAfter=8
)

body_style = ParagraphStyle(
    'DocBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#222222'),
    spaceAfter=8
)

bullet_style = ParagraphStyle(
    'DocBullet',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#333333'),
    leftIndent=15,
    spaceAfter=4
)

story = []

# Title & Metadata
story.append(Paragraph("Sustainable Agriculture, Soil Management & Crop Science Handbook", title_style))
story.append(Paragraph("A Comprehensive Practical Reference Guide for Smart Farming & Agronomy", subtitle_style))
story.append(Spacer(1, 10))

# Section 1: Soil Macronutrients & Health
story.append(Paragraph("1. Soil Chemistry & Macronutrient Diagnostics", h1_style))
story.append(Paragraph(
    "Soil fertility is primarily determined by three primary macronutrients: Nitrogen (N), Phosphorus (P), and Potassium (K), alongside optimal soil reaction (pH) and organic matter content. Maintaining balanced stoichiometric ratios ensures robust root architecture, photosynthetic efficiency, and disease resistance.",
    body_style
))
story.append(Paragraph("<b>• Nitrogen (N) Dynamics:</b> Nitrogen is the fundamental constituent of amino acids, proteins, and chlorophyll. Deficiency manifests as chlorosis (general yellowing of older lower leaves) and stunted vegetative growth. Excessive nitrogen promotes overly succulent foliage, delayed maturity, and vulnerability to fungal lodging. Recommended application relies on split doses: 50% basal and 50% top-dressing at active tillering.", bullet_style))
story.append(Paragraph("<b>• Phosphorus (P) Dynamics:</b> Critical for cellular energy transfer (ATP), rapid root proliferation, and early crop establishment. Deficiencies cause reddish-purple discoloration on leaf undersides and poor panicle/grain filling. DAP (Di-Ammonium Phosphate 18% N, 46% P2O5) or Single Super Phosphate (SSP 16% P2O5) should always be placed deep into root zones at basal sowing.", bullet_style))
story.append(Paragraph("<b>• Potassium (K) Dynamics:</b> Regulates stomatal aperture, cellular turgor, enzymatic activation, and drought tolerance. Deficiency causes marginal leaf scorching, weak stems, and poor grain luster. Muriate of Potash (MOP 60% K2O) provides immediate potassium bio-availability.", bullet_style))
story.append(Paragraph("<b>• Soil pH Amelioration:</b> Ideal agronomic pH is between 6.0 and 7.5. For acidic soils (pH < 6.0), agricultural lime (CaCO3) at 1 to 2 tonnes/acre neutralizes free aluminum and manganese toxicity. For alkaline/sodic soils (pH > 8.0), agricultural gypsum (CaSO4.2H2O) at 500-1000 kg/acre promotes sodium displacement and soil aggregation.", bullet_style))
story.append(Spacer(1, 10))

# Section 2: Crop-Specific Cultivation Protocols
story.append(Paragraph("2. Agronomic Protocols for Major Food & Cash Crops", h1_style))

crop_table_data = [
    ["Crop", "Optimal Soil & Climate", "NPK Benchmark", "Water & Irrigation Management"],
    ["Rice (Paddy)", "Clayey / Alluvial, 20-35°C, pH 5.5-7.2", "N: 80-120, P: 35-50, K: 35-50", "Continuous flooding (5cm) or Alternate Wetting & Drying (AWD)"],
    ["Wheat", "Well-drained Loam, 12-25°C, pH 6.0-7.5", "N: 100-140, P: 45-60, K: 40-50", "4-6 critical irrigations: CRI stage (21 DAS), tillering, flowering"],
    ["Cotton", "Deep Black Cotton Soil, 22-34°C, pH 6.0-8.2", "N: 100-140, P: 40-60, K: 40-60", "Moderate rainfall (600-1000mm) or drip irrigation at boll formation"],
    ["Maize", "Rich Loam / Sandy Loam, 18-30°C, pH 5.8-7.5", "N: 70-100, P: 40-55, K: 30-45", "Critical irrigation at knee-high, tasseling, and silking stages"],
    ["Apple", "Deep Loamy / Hilly Soil, 10-24°C, pH 5.5-6.8", "N: 20-40, P: 120-145, K: 190-205", "High chilling hours (800-1000 hrs < 7°C), drip fertigation"],
    ["Coffee", "Rich Volcanic / Red Loam, 15-28°C, pH 6.0-6.5", "N: 90-110, P: 25-40, K: 25-40", "High humidity (70-90%), partial shade canopy, sprinkler blossom shower"]
]

t = Table(crop_table_data, colWidths=[90, 140, 120, 180])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d6a4f')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 8.5),
    ('BOTTOMPADDING', (0,0), (-1,0), 6),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f7fbf8')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d8f3dc')),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 8),
    ('TOPPADDING', (0,1), (-1,-1), 5),
    ('BOTTOMPADDING', (0,1), (-1,-1), 5),
]))
story.append(t)
story.append(Spacer(1, 15))

# Section 3: Integrated Pest Management & Organic Amelioration
story.append(Paragraph("3. Integrated Pest Management (IPM) & Organic Practices", h1_style))
story.append(Paragraph(
    "Sustainable agriculture reduces synthetic pesticide dependence through biological controls, trap crops, and botanical extracts. Neem oil (Azadirachtin 1500 ppm) at 5ml/liter acts as an effective repellent and anti-feedant for sucking pests including aphids, jassids, and whiteflies.",
    body_style
))
story.append(Paragraph("<b>• Trichoderma viride:</b> Bio-fungicide applied as seed treatment (10g/kg seed) to prevent damping off, root rot, and Fusarium wilt in pulses and vegetables.", bullet_style))
story.append(Paragraph("<b>• Crop Rotation & Legume Cover:</b> Rotating cereal crops (Maize/Rice) with nitrogen-fixing pulses (Chickpea/Lentil) sequesters up to 40 kg atmospheric N/ha organically and breaks weed propagation cycles.", bullet_style))
story.append(Paragraph("<b>• Vermicompost & Farmyard Manure (FYM):</b> Applying 3-5 tonnes/acre of decomposed FYM improves cation exchange capacity (CEC), microbial diversity, and soil moisture retention during dry spells.", bullet_style))

doc.build(story)
print("Successfully generated:", pdf_path)
