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
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .calculation-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .safe {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .unsafe {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .warning {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🏗️ Reinforced Concrete Section Design</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #7f8c8d;">Based on ACI 318 Code</p>', unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("📊 Input Parameters")

# Input method selection
input_method = st.sidebar.radio("Input Method", ["Sliders with Manual Override", "Manual Input Only"])

st.sidebar.markdown("---")
st.sidebar.subheader("Material Properties")

# Material properties inputs
if input_method == "Sliders with Manual Override":
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        fy_slider = st.slider("Steel Yield Strength, fy (MPa)", 
                             min_value=200.0, max_value=600.0, value=420.0, step=10.0)
    with col2:
        fy = st.number_input("fy", value=fy_slider, label_visibility="collapsed", key="fy_manual")
    
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        fcu_slider = st.slider("Concrete Compressive Strength, f'c (MPa)", 
                              min_value=15.0, max_value=50.0, value=25.0, step=2.5)
    with col2:
        fcu = st.number_input("fcu", value=fcu_slider, label_visibility="collapsed", key="fcu_manual")
else:
    fy = st.sidebar.number_input("Steel Yield Strength, fy (MPa)", value=420.0, min_value=200.0, max_value=600.0)
    fcu = st.sidebar.number_input("Concrete Compressive Strength, f'c (MPa)", value=25.0, min_value=15.0, max_value=50.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Loading")

# Moment input
if input_method == "Sliders with Manual Override":
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

# Section dimensions
if input_method == "Sliders with Manual Override":
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        b_slider = st.slider("Section Width, b (mm)", 
                            min_value=100.0, max_value=2000.0, value=1000.0, step=50.0)
    with col2:
        b = st.number_input("b", value=b_slider, label_visibility="collapsed", key="b_manual")
    
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        h_slider = st.slider("Section Height, h (mm)", 
                            min_value=100.0, max_value=500.0, value=150.0, step=10.0)
    with col2:
        h = st.number_input("h", value=h_slider, label_visibility="collapsed", key="h_manual")
else:
    b = st.sidebar.number_input("Section Width, b (mm)", value=1000.0, min_value=100.0)
    h = st.sidebar.number_input("Section Height, h (mm)", value=150.0, min_value=100.0)

cover = st.sidebar.number_input("Concrete Cover (mm)", value=20.0, min_value=15.0, max_value=75.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Design Parameters")

# Design parameters
phi = st.sidebar.number_input("Strength Reduction Factor, φ", value=0.9, min_value=0.65, max_value=0.9, step=0.05)
jd = st.sidebar.number_input("Moment Arm Factor, jd", value=0.95, min_value=0.85, max_value=0.95, step=0.01,
                             help="Typically 0.95 for slabs, 0.9 for beams")
beta1 = st.sidebar.number_input("β₁ Factor", value=0.85, min_value=0.65, max_value=0.85, step=0.05,
                                help="β₁ = 0.85 for f'c ≤ 28 MPa, reduces for higher strengths")

# Main content
st.markdown('<h2 class="section-header">📋 Design Summary</h2>', unsafe_allow_html=True)

# Display input summary
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ultimate Moment, Mu", f"{Mu} kN.m")
    st.metric("Section Width, b", f"{b} mm")
with col2:
    st.metric("Section Height, h", f"{h} mm")
    st.metric("Concrete Cover", f"{cover} mm")
with col3:
    st.metric("Steel Strength, fy", f"{fy} MPa")
    st.metric("Concrete Strength, f'c", f"{fcu} MPa")

# Calculations
st.markdown('<h2 class="section-header">🔢 Detailed Calculations</h2>', unsafe_allow_html=True)

# Step 1: Effective depth
st.markdown("### Step 1: Calculate Effective Depth")
d = h - cover
st.markdown(f"""
<div class="calculation-box">
<b>Formula:</b> d = h - cover<br>
<b>Calculation:</b> d = {h} - {cover} = <b>{d} mm</b>
</div>
""", unsafe_allow_html=True)

# Step 2: Initial steel area
st.markdown("### Step 2: Calculate Initial Steel Area")
Mu_Nmm = Mu * 1e6  # Convert kN.m to N.mm
As_initial = Mu_Nmm / (phi * fy * jd * d)
st.markdown(f"""
<div class="calculation-box">
<b>Formula:</b> As<sub>initial</sub> = Mu / (φ × fy × jd × d)<br>
<b>Calculation:</b> As<sub>initial</sub> = {Mu * 1e6:.2e} / ({phi} × {fy} × {jd} × {d})<br>
<b>Result:</b> As<sub>initial</sub> = <b>{As_initial:.2f} mm²</b>
</div>
""", unsafe_allow_html=True)

# Step 3: Iterative calculation for As
st.markdown("### Step 3: Calculate Accurate Steel Area")

# Calculate 'a' using initial As
a = (As_initial * fy) / (0.85 * fcu * b)
st.markdown(f"""
<div class="calculation-box">
<b>Formula:</b> a = (As × fy) / (0.85 × f'c × b)<br>
<b>Calculation:</b> a = ({As_initial:.2f} × {fy}) / (0.85 × {fcu} × {b})<br>
<b>Result:</b> a = <b>{a:.2f} mm</b>
</div>
""", unsafe_allow_html=True)

# Calculate accurate As
As_calculated = Mu_Nmm / (phi * fy * (d - a/2))
st.markdown(f"""
<div class="calculation-box">
<b>Formula:</b> As = Mu / (φ × fy × (d - a/2))<br>
<b>Calculation:</b> As = {Mu * 1e6:.2e} / ({phi} × {fy} × ({d} - {a:.2f}/2))<br>
<b>Calculation:</b> As = {Mu * 1e6:.2e} / ({phi} × {fy} × {d - a/2:.2f})<br>
<b>Result:</b> As<sub>calculated</sub> = <b>{As_calculated:.2f} mm²</b>
</div>
""", unsafe_allow_html=True)

# Step 4: Minimum reinforcement
st.markdown("### Step 4: Calculate Minimum Steel Area")
As_min = (1.4 * b * d) / fy
st.markdown(f"""
<div class="calculation-box">
<b>Formula:</b> As<sub>min</sub> = (1.4 × b × d) / fy<br>
<b>Calculation:</b> As<sub>min</sub> = (1.4 × {b} × {d}) / {fy}<br>
<b>Result:</b> As<sub>min</sub> = <b>{As_min:.2f} mm²</b>
</div>
""", unsafe_allow_html=True)

# Step 5: Required As
st.markdown("### Step 5: Determine Required Steel Area")
As_required = max(As_calculated, As_min)
if As_required == As_min:
    st.warning("⚠️ Minimum reinforcement governs!")
    governing = "As_min"
else:
    st.info("✓ Calculated reinforcement governs")
    governing = "As_calculated"

st.markdown(f"""
<div class="calculation-box">
<b>Formula:</b> As<sub>required</sub> = max(As<sub>calculated</sub>, As<sub>min</sub>)<br>
<b>Calculation:</b> As<sub>required</sub> = max({As_calculated:.2f}, {As_min:.2f})<br>
<b>Result:</b> As<sub>required</sub> = <b>{As_required:.2f} mm²</b> ({governing} governs)
</div>
""", unsafe_allow_html=True)

# Step 6: Check reinforcement ratio
st.markdown("### Step 6: Verify Design - Check Strain Conditions")

# Recalculate 'a' with required As
a_final = (As_required * fy) / (0.85 * fcu * b)
c = a_final / beta1
es = ((d - c) / c) * 0.003

st.markdown(f"""
<div class="calculation-box">
<b>Calculate depth of neutral axis:</b><br>
a = (As<sub>required</sub> × fy) / (0.85 × f'c × b) = ({As_required:.2f} × {fy}) / (0.85 × {fcu} × {b}) = <b>{a_final:.2f} mm</b><br><br>
<b>Calculate distance to neutral axis:</b><br>
c = a / β₁ = {a_final:.2f} / {beta1} = <b>{c:.2f} mm</b><br><br>
<b>Calculate steel strain:</b><br>
εs = ((d - c) / c) × 0.003 = (({d} - {c:.2f}) / {c:.2f}) × 0.003 = <b>{es:.5f}</b>
</div>
""", unsafe_allow_html=True)

# Check if tension-controlled
min_strain = 0.002  # ACI code requirement for tension-controlled
if es >= 0.005:
    strain_status = "✓ Tension-controlled section (εs ≥ 0.005)"
    strain_check = True
    strain_class = "safe"
elif es >= min_strain:
    strain_status = "✓ Tension-controlled section (εs ≥ 0.002)"
    strain_check = True
    strain_class = "safe"
else:
    strain_status = "✗ Compression-controlled or transition zone (εs < 0.002) - Reduce φ factor!"
    strain_check = False
    strain_class = "unsafe"

st.markdown(f'<p class="{strain_class}">{strain_status}</p>', unsafe_allow_html=True)

# Step 7: Calculate design moment capacity
st.markdown("### Step 7: Calculate Design Moment Capacity")
phi_Mn_Nmm = phi * As_required * fy * (d - a_final/2)
phi_Mn = phi_Mn_Nmm / 1e6  # Convert to kN.m

st.markdown(f"""
<div class="calculation-box">
<b>Formula:</b> φMn = φ × As × fy × (d - a/2)<br>
<b>Calculation:</b> φMn = {phi} × {As_required:.2f} × {fy} × ({d} - {a_final:.2f}/2)<br>
<b>Calculation:</b> φMn = {phi} × {As_required:.2f} × {fy} × {d - a_final/2:.2f}<br>
<b>Result:</b> φMn = <b>{phi_Mn:.2f} kN.m</b>
</div>
""", unsafe_allow_html=True)

# Step 8: Final capacity check
st.markdown("### Step 8: Capacity Check")
capacity_ratio = phi_Mn / Mu
if phi_Mn >= Mu:
    capacity_status = f"✓ SAFE: φMn ({phi_Mn:.2f} kN.m) ≥ Mu ({Mu} kN.m)"
    capacity_check = True
    capacity_class = "safe"
else:
    capacity_status = f"✗ UNSAFE: φMn ({phi_Mn:.2f} kN.m) < Mu ({Mu} kN.m)"
    capacity_check = False
    capacity_class = "unsafe"

st.markdown(f"""
<div class="calculation-box">
<b>Check:</b> φMn ≥ Mu<br>
<b>Calculation:</b> {phi_Mn:.2f} kN.m vs {Mu} kN.m<br>
<b>Capacity Ratio:</b> φMn / Mu = {capacity_ratio:.3f}<br>
<p class="{capacity_class}">{capacity_status}</p>
</div>
""", unsafe_allow_html=True)

# Final Design Summary
st.markdown('<h2 class="section-header">✅ Final Design Summary</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Required Reinforcement")
    st.metric("As required", f"{As_required:.2f} mm²")
    st.metric("Minimum As", f"{As_min:.2f} mm²")
    st.metric("Calculated As", f"{As_calculated:.2f} mm²")
    
    # Suggest rebar configuration
    st.markdown("#### Suggested Rebar Configuration")
    rebar_sizes = [10, 12, 16, 20, 25, 32]
    rebar_areas = [78.5, 113.1, 201.1, 314.2, 490.9, 804.2]  # mm²
    
    st.markdown("**Common rebar configurations:**")
    for size, area in zip(rebar_sizes, rebar_areas):
        num_bars = math.ceil(As_required / area)
        provided_area = num_bars * area
        if num_bars <= 15:  # Reasonable number of bars
            percentage_over = ((provided_area - As_required) / As_required) * 100
            st.markdown(f"- {num_bars}Ø{size} mm → {provided_area:.1f} mm² (+{percentage_over:.1f}%)")

with col2:
    st.markdown("#### Design Checks")
    
    # Overall status
    if capacity_check and strain_check:
        overall_status = "✅ DESIGN IS SAFE"
        overall_class = "safe"
    else:
        overall_status = "❌ DESIGN IS NOT SAFE"
        overall_class = "unsafe"
    
    st.markdown(f'<h3 class="{overall_class}">{overall_status}</h3>', unsafe_allow_html=True)
    
    st.markdown("**Check Details:**")
    st.markdown(f"- Strain Check: {'✓ Pass' if strain_check else '✗ Fail'}")
    st.markdown(f"  - Steel strain εs = {es:.5f}")
    st.markdown(f"  - Required: εs ≥ {min_strain}")
    st.markdown(f"- Capacity Check: {'✓ Pass' if capacity_check else '✗ Fail'}")
    st.markdown(f"  - φMn = {phi_Mn:.2f} kN.m")
    st.markdown(f"  - Mu = {Mu} kN.m")
    st.markdown(f"  - Ratio = {capacity_ratio:.3f}")

# Additional notes
st.markdown('<h2 class="section-header">📝 Design Notes</h2>', unsafe_allow_html=True)
st.info("""
**Important Considerations:**
- This design is based on ACI 318 Code for reinforced concrete
- The analysis assumes singly reinforced rectangular section
- For tension-controlled sections: εs ≥ 0.005, use φ = 0.9
- For transition sections: 0.002 ≤ εs < 0.005, φ varies between 0.65 and 0.9
- Always check local building codes and standards
- Consider serviceability requirements (deflection, crack width)
- Verify development length and detailing requirements
- This is a preliminary design - final design should be reviewed by a licensed engineer
""")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #7f8c8d;">Developed for Civil Engineering Applications | ACI 318 Code</p>',
    unsafe_allow_html=True
)
