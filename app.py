import streamlit as st
import math

# Page configuration
st.set_page_config(
    page_title="RC Section Design - ACI",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .calc-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .calc-table th {
        background-color: #1f77b4;
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: bold;
    }
    .calc-table td {
        padding: 10px;
        border-bottom: 1px solid #ddd;
    }
    .calc-table tr:hover {
        background-color: #f5f5f5;
    }
    .formula-col {
        background-color: #e3f2fd;
        font-family: 'Courier New', monospace;
    }
    .substitution-col {
        background-color: #fff3e0;
        font-family: 'Courier New', monospace;
    }
    .result-col {
        background-color: #e8f5e9;
        font-weight: bold;
        text-align: center;
    }
    .safe {
        color: #28a745;
        font-weight: bold;
        font-size: 1.3rem;
    }
    .unsafe {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.3rem;
    }
    .warning {
        color: #ffc107;
        font-weight: bold;
    }
    .summary-box {
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🏗️ Reinforced Concrete Section Design (ACI)</h1>', unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("📊 Input Parameters")

# Input method selection
input_method = st.sidebar.radio("Input Method", ["Sliders", "Manual Input"])

st.sidebar.markdown("---")
st.sidebar.subheader("Material Properties")

# Material properties inputs
if input_method == "Sliders":
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        fy_slider = st.slider("Steel Yield Strength, fy (MPa)", 
                             min_value=200.0, max_value=600.0, value=420.0, step=10.0)
    with col2:
        fy = st.number_input("fy", value=fy_slider, label_visibility="collapsed", key="fy_manual")
    
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        fcu_slider = st.slider("Concrete Strength, f'c (MPa)", 
                              min_value=15.0, max_value=50.0, value=25.0, step=2.5)
    with col2:
        fcu = st.number_input("fcu", value=fcu_slider, label_visibility="collapsed", key="fcu_manual")
else:
    fy = st.sidebar.number_input("Steel Yield Strength, fy (MPa)", value=420.0, min_value=200.0, max_value=600.0)
    fcu = st.sidebar.number_input("Concrete Strength, f'c (MPa)", value=25.0, min_value=15.0, max_value=50.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Loading")

if input_method == "Sliders":
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        Mu_slider = st.slider("Ultimate Moment, Mu (kN.m)", 
                             min_value=0.0, max_value=200.0, value=13.7, step=0.1)
    with col2:
        Mu = st.number_input("Mu", value=Mu_slider, label_visibility="collapsed", key="Mu_manual")
else:
    Mu = st.sidebar.number_input("Ultimate Moment, Mu (kN.m)", value=13.7, min_value=0.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Section Dimensions")

if input_method == "Sliders":
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        b_slider = st.slider("Width, b (mm)", 
                            min_value=100.0, max_value=2000.0, value=1000.0, step=50.0)
    with col2:
        b = st.number_input("b", value=b_slider, label_visibility="collapsed", key="b_manual")
    
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        h_slider = st.slider("Height, h (mm)", 
                            min_value=100.0, max_value=500.0, value=150.0, step=10.0)
    with col2:
        h = st.number_input("h", value=h_slider, label_visibility="collapsed", key="h_manual")
else:
    b = st.sidebar.number_input("Width, b (mm)", value=1000.0, min_value=100.0)
    h = st.sidebar.number_input("Height, h (mm)", value=150.0, min_value=100.0)

cover = st.sidebar.number_input("Cover (mm)", value=20.0, min_value=15.0, max_value=75.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Design Parameters")

phi = st.sidebar.number_input("Strength Reduction Factor, φ", value=0.9, min_value=0.65, max_value=0.9, step=0.05)
jd = st.sidebar.number_input("Moment Arm Factor, jd", value=0.95, min_value=0.85, max_value=0.95, step=0.01)
beta1 = st.sidebar.number_input("β₁ Factor", value=0.85, min_value=0.65, max_value=0.85, step=0.05)

# Perform calculations
d = h - cover
Mu_Nmm = Mu * 1e6
As_initial = Mu_Nmm / (phi * fy * jd * d)
a_initial = (As_initial * fy) / (0.85 * fcu * b)
As_calculated = Mu_Nmm / (phi * fy * (d - a_initial/2))
As_min = (1.4 * b * d) / fy
As_required = max(As_calculated, As_min)
a_final = (As_required * fy) / (0.85 * fcu * b)
c = a_final / beta1
es = ((d - c) / c) * 0.003
phi_Mn_Nmm = phi * As_required * fy * (d - a_final/2)
phi_Mn = phi_Mn_Nmm / 1e6

# Main content - Input Summary
st.markdown('<h2 class="section-header">📋 Input Summary</h2>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Mu", f"{Mu} kN.m")
    st.metric("b", f"{b} mm")
with col2:
    st.metric("h", f"{h} mm")
    st.metric("Cover", f"{cover} mm")
with col3:
    st.metric("fy", f"{fy} MPa")
    st.metric("f'c", f"{fcu} MPa")
with col4:
    st.metric("φ", f"{phi}")
    st.metric("jd", f"{jd}")

# Calculations Table
st.markdown('<h2 class="section-header">🔢 Design Calculations</h2>', unsafe_allow_html=True)

# Create calculation table
calc_data = []

# Row 1: Effective depth
calc_data.append({
    'step': 'd',
    'formula': r'$d = h - cover$',
    'substitution': f'd = {h} - {cover}',
    'result': f'{d:.1f} mm'
})

# Row 2: Initial As
calc_data.append({
    'step': 'As initial',
    'formula': r'$A_s = \frac{M_u}{\phi \cdot f_y \cdot jd \cdot d}$',
    'substitution': f'As = {Mu*1e6:.2e} / ({phi} × {fy} × {jd} × {d})',
    'result': f'{As_initial:.2f} mm²'
})

# Row 3: Calculate a
calc_data.append({
    'step': 'a',
    'formula': r"$a = \frac{A_s \cdot f_y}{0.85 \cdot f'_c \cdot b}$",
    'substitution': f'a = ({As_initial:.2f} × {fy}) / (0.85 × {fcu} × {b})',
    'result': f'{a_initial:.2f} mm'
})

# Row 4: Accurate As
calc_data.append({
    'step': 'As',
    'formula': r'$A_s = \frac{M_u}{\phi \cdot f_y \cdot (d - \frac{a}{2})}$',
    'substitution': f'As = {Mu*1e6:.2e} / ({phi} × {fy} × {d - a_initial/2:.2f})',
    'result': f'{As_calculated:.2f} mm²'
})

# Row 5: As min
calc_data.append({
    'step': 'As min',
    'formula': r'$A_{s,min} = \frac{1.4 \cdot b \cdot d}{f_y}$',
    'substitution': f'As,min = (1.4 × {b} × {d}) / {fy}',
    'result': f'{As_min:.2f} mm²'
})

# Row 6: Check As
governing = "As min" if As_required == As_min else "As calculated"
calc_data.append({
    'step': 'Check As',
    'formula': r'$A_{s,req} = max(A_s, A_{s,min})$',
    'substitution': f'As,req = max({As_calculated:.2f}, {As_min:.2f})',
    'result': f'{As_required:.2f} mm² ({governing})'
})

# Row 7: Final c value
calc_data.append({
    'step': 'c',
    'formula': r'$c = \frac{a}{\beta_1}$',
    'substitution': f'c = {a_final:.2f} / {beta1}',
    'result': f'{c:.2f} mm'
})

# Row 8: Steel strain
calc_data.append({
    'step': 'εs',
    'formula': r'$\varepsilon_s = \frac{d - c}{c} \times 0.003$',
    'substitution': f'εs = ({d} - {c:.2f}) / {c:.2f} × 0.003',
    'result': f'{es:.5f}'
})

# Row 9: Check strain
strain_check_result = "✓ OK" if es >= 0.002 else "✗ FAIL"
strain_status = "Tension-controlled" if es >= 0.005 else ("Transition" if es >= 0.002 else "Compression")
calc_data.append({
    'step': 'Check εs',
    'formula': r'$\varepsilon_s \geq 0.002$',
    'substitution': f'{es:.5f} ≥ 0.002',
    'result': f'{strain_check_result} ({strain_status})'
})

# Row 10: Design moment
calc_data.append({
    'step': 'φMn',
    'formula': r'$\phi M_n = \phi \cdot A_s \cdot f_y \cdot (d - \frac{a}{2})$',
    'substitution': f'φMn = {phi} × {As_required:.2f} × {fy} × {d - a_final/2:.2f}',
    'result': f'{phi_Mn:.2f} kN.m'
})

# Row 11: Final check
capacity_check_result = "✓ SAFE" if phi_Mn >= Mu else "✗ UNSAFE"
calc_data.append({
    'step': 'Check φMn',
    'formula': r'$\phi M_n \geq M_u$',
    'substitution': f'{phi_Mn:.2f} ≥ {Mu}',
    'result': f'{capacity_check_result}'
})

# Display table
table_html = """
<table class="calc-table">
    <thead>
        <tr>
            <th style="width: 15%;">Parameter</th>
            <th style="width: 35%;">Formula</th>
            <th style="width: 35%;">Substitution</th>
            <th style="width: 15%;">Result</th>
        </tr>
    </thead>
    <tbody>
"""

for row in calc_data:
    table_html += f"""
        <tr>
            <td><strong>{row['step']}</strong></td>
            <td class="formula-col">{row['formula']}</td>
            <td class="substitution-col">{row['substitution']}</td>
            <td class="result-col">{row['result']}</td>
        </tr>
    """

table_html += """
    </tbody>
</table>
"""

st.markdown(table_html, unsafe_allow_html=True)

# Final Summary
st.markdown('<h2 class="section-header">✅ Design Summary</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
    st.markdown("#### Required Reinforcement")
    st.metric("As required", f"{As_required:.2f} mm²")
    
    # Suggest rebar configuration
    st.markdown("#### Rebar Suggestions")
    rebar_sizes = [10, 12, 16, 20, 25]
    rebar_areas = [78.5, 113.1, 201.1, 314.2, 490.9]
    
    suggestions = []
    for size, area in zip(rebar_sizes, rebar_areas):
        num_bars = math.ceil(As_required / area)
        if num_bars <= 12:
            provided_area = num_bars * area
            suggestions.append(f"• {num_bars}Ø{size} → {provided_area:.0f} mm²")
    
    for suggestion in suggestions[:3]:  # Show top 3
        st.markdown(suggestion)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
    st.markdown("#### Safety Checks")
    
    # Determine overall safety
    strain_safe = es >= 0.002
    capacity_safe = phi_Mn >= Mu
    overall_safe = strain_safe and capacity_safe
    
    if overall_safe:
        st.markdown('<p class="safe">✅ DESIGN IS SAFE</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="unsafe">❌ DESIGN IS NOT SAFE</p>', unsafe_allow_html=True)
    
    st.markdown("**Details:**")
    st.markdown(f"• Strain Check: {'✓ Pass' if strain_safe else '✗ Fail'} (εs = {es:.5f})")
    st.markdown(f"• Capacity Check: {'✓ Pass' if capacity_safe else '✗ Fail'} (φMn/Mu = {phi_Mn/Mu:.3f})")
    st.markdown(f"• Section Type: {strain_status}")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">ACI 318 Code | For Educational Purposes</p>', unsafe_allow_html=True)
