
import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objs as go
import yfinance as yf

# إعداد الصفحة
st.set_page_config(page_title="GoldSmart - التحليل الموسمي للذهب", layout="wide")
st.markdown("""<h1 style='text-align: center; color: gold;'>🌟 GoldSmart Dashboard 🌟</h1>""", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #888;'>تحليل موسمي وتاريخي احترافي لأسعار الذهب</h4>", unsafe_allow_html=True)
st.markdown("---")

# تحميل بيانات الذهب
end = datetime.date.today()
start = end - datetime.timedelta(days=365 * 5)
data = yf.download("GC=F", start=start, end=end)
data = data[['Close']].dropna().reset_index()
data.columns = ['Date', 'Price']
data['Month'] = data['Date'].dt.month

# التأثيرات الموسمية حسب تحليلك
seasonal_effects = {
    1: 1.008576, 2: 0.996684, 3: 1.016732, 4: 1.019485,
    5: 1.016862, 6: 1.006577, 7: 1.026193, 8: 1.011332,
    9: 0.977220, 10: 0.991212, 11: 0.968613, 12: 0.994965
}

# جدول لكل الشهور
months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
          "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

table_data = []
for i in range(1, 13):
    effect = seasonal_effects.get(i, 1)
    signal = '📈 Bullish' if effect > 1 else '📉 Bearish'
    table_data.append({
        "📅 الشهر": months[i-1],
        "📊 التأثير الموسمي": round(effect, 6),
        "📌 الاتجاه المتوقع": signal
    })

df_season = pd.DataFrame(table_data)

# عرض جدول التحليل الموسمي بشكل أنيق
st.markdown("### 🔎 التحليل الموسمي لجميع أشهر السنة")
st.dataframe(df_season.style.set_properties(**{
    'background-color': '#111',
    'color': 'gold',
    'border-color': 'white'
}))

# عرض السعر الحالي للذهب
st.markdown("### 💰 السعر الحالي للذهب")
col1, col2 = st.columns(2)
col1.metric("سعر الأونصة (USD)", f"{data['Price'].iloc[-1]:,.2f}")
col2.write(f"📆 التاريخ اليوم: **{end.strftime('%d / %B / %Y')}**")

# رسم بياني جميل لتطور الذهب
st.markdown("### 📉 تطور سعر الذهب خلال آخر 5 سنوات")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['Date'], y=data['Price'], name='Gold Price',
                         line=dict(color='gold', width=2)))
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    title='🔔 Gold Price Over Time',
    xaxis_title='📆 التاريخ',
    yaxis_title='💲 السعر بالدولار'
)
st.plotly_chart(fig, use_container_width=True)

# رسالة ختامية
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>تم التطوير بواسطة الذكاء الاصطناعي 🤖</div>", unsafe_allow_html=True)
