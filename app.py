import streamlit as st
import pandas as pd
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Slab Design Pro", page_icon="🏗️", layout="wide")

# --- العنوان ---
st.title("🏗️ تصميم بلاطة خرسانية مصمتة (Solid Slab Design)")
st.markdown("---")

# --- القائمة الجانبية للمدخلات ---
with st.sidebar:
    st.header("1. خصائص المواد (Materials)")
    fcu = st.number_input("مقاومة الخرسانة (fcu) [MPa]", value=25.0, step=5.0)
    fy = st.number_input("إجهاد خضوع الحديد (fy) [MPa]", value=420.0, step=10.0)
    
    st.header("2. الأبعاد والأحمال (Geometry & Loads)")
    Mu = st.number_input("العزم الأقصى (Mu) [kN.m]", value=13.7, step=0.1)
    h = st.number_input("سماكة البلاطة (h) [mm]", value=150.0, step=10.0)
    b = st.number_input("عرض الشريحة (b) [mm]", value=1000.0, disabled=True, help="يتم التصميم دائماً لشريحة عرضها 1 متر")
    cover = st.number_input("الغطاء الخرساني (Cover) [mm]", value=20.0, step=5.0)
    
    st.header("3. تفاصيل التسليح (Reinforcement)")
    bar_dia = st.selectbox("قطر السيخ المستخدم (Φ) [mm]", [8, 10, 12, 14, 16], index=2)

# --- الحسابات الهندسية ---

# 1. حساب العمق الفعال d
d = h - cover - (bar_dia / 2)

# 2. حساب مساحة الحديد المطلوبة (As Required)
# القانون: As = Mu / (phi * fy * j * d) .. سنستخدم معادلة دقيقة
# a = (As * fy) / (0.85 * fcu * b)
# سنبدأ بفرضية j=0.9 ثم نحسب بدقة
phi = 0.9
As_initial = (Mu * 1e6) / (phi * fy * 0.9 * d)
a = (As_initial * fy) / (0.85 * fcu * b)
As_req = (Mu * 1e6) / (phi * fy * (d - a/2))

# 3. حساب الحد الأدنى للتسليح (As Minimum)
# حسب الكود (مثال: ACI 318 أو الكود المصري، سنستخدم المعادلة العامة الشائعة)
As_min_1 = 0.0018 * b * h  # للحديد عالي المقاومة (Shrinkage & Temp)
As_min_2 = (1.4 * b * d) / fy # للكمرات والبلاطات العاملة في اتجاه واحد
As_min = max(As_min_1, As_min_2)

# 4. اختيار القيمة التصميمية النهائية
As_final = max(As_req, As_min)

# 5. حساب عدد الأسياخ والمسافات
bar_area = (math.pi * (bar_dia/2)**2)
num_bars = As_final / bar_area
spacing = 1000 / num_bars

# تقريب المسافة لأقرب 10 مم (للتنفيذ)
spacing_provided = math.floor(spacing / 10) * 10 
if spacing_provided > 250: spacing_provided = 250 # أقصى مسافة شائعة
if spacing_provided < 100: spacing_provided = 100 # أقل مسافة شائعة

As_provided = (1000 / spacing_provided) * bar_area

# --- عرض النتائج في الصفحة الرئيسية ---

# عمودين لعرض النتائج الرئيسية
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 النتائج الحسابية")
    st.info(f"العمق الفعال (d) = **{d} mm**")
    st.info(f"الحديد المطلوب حسابياً (As_req) = **{As_req:.1f} mm²**")
    st.info(f"الحد الأدنى للكود (As_min) = **{As_min:.1f} mm²**")

with col2:
    st.subheader("✅ القرار التصميمي")
    if As_req > As_min:
        st.success(f"التحكم: العزم هو الحاكم (As_req > As_min)")
    else:
        st.warning(f"التحكم: الحد الأدنى هو الحاكم (As_min > As_req)")
    
    st.metric(label="مساحة الحديد التصميمية النهائية", value=f"{As_final:.1f} mm²")

st.markdown("---")

# --- قسم المعادلات (كما طلبت) ---
st.subheader("📐 المعادلات المستخدمة")
st.latex(r'''
d = h - cover - \frac{\phi_{bar}}{2}
''')
st.latex(r'''
A_s = \frac{M_u \times 10^6}{\phi f_y (d - a/2)}
''')
st.latex(r'''
A_{s,min} = \max(0.0018 b h, \frac{1.4 b d}{f_y})
''')

st.markdown("---")

# --- الجدول النهائي (الخلاصة) ---
st.subheader("📋 جدول ملخص التصميم")

# نستخدم مكتبة Pandas لعمل جدول أنيق
data = {
    "البند": ["العزم المؤثر (Mu)", "سماكة البلاطة (h)", "الحديد المطلوب (As)", "الحديد المختار (Provided)"],
    "القيمة": [f"{Mu} kN.m", f"{h} mm", f"{As_final:.1f} mm²", f"{As_provided:.1f} mm²"],
    "التفاصيل": ["-", "-", "-", f"استخدم {math.ceil(1000/spacing_provided)}Φ{bar_dia} /m (كل {spacing_provided} مم)"]
}
df = pd.DataFrame(data)
st.table(df)

# رسالة نجاح نهائية
if As_provided >= As_final:
    st.success(f"🎉 التصميم آمن! استخدم شبكة حديد: قطر {bar_dia} مم كل {spacing_provided} مم.")
else:
    st.error("⚠️ تنبيه: الحديد المختار أقل من المطلوب (يرجى تقليل المسافات).")