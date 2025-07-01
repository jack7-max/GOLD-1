
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.graph_objs as go

# إعداد الصفحة
st.set_page_config(page_title="GoldSmart Dashboard", layout="wide")
st.title("📈 GoldSmart Dashboard - توقع سعر الذهب")

# جلب بيانات الذهب آخر 5 سنوات
end = datetime.date.today()
start = end - datetime.timedelta(days=365 * 5)
gold = yf.download("GC=F", start=start, end=end, interval='1d')
gold = gold[['Close']].dropna().reset_index()
gold.columns = ['Date', 'Price']

# تحليل موسمي سريع
month = end.month
seasonal_effects = {
    1: 1.008576, 2: 0.996684, 3: 1.016732, 4: 1.019485,
    5: 1.016862, 6: 1.006577, 7: 1.026193, 8: 1.011332,
    9: 0.977220, 10: 0.991212, 11: 0.968613, 12: 0.994965
}
effect = seasonal_effects.get(month, 1)
signal = '📈 Bullish' if effect > 1 else '📉 Bearish'

# عرض السعر الحالي والإشارة
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 السعر الحالي للذهب:")
    st.metric("سعر الأونصة (USD)", f"{gold['Price'].iloc[-1]:,.2f}")
with col2:
    st.subheader("📆 التحليل الموسمي:")
    st.write(f"📅 الشهر الحالي: **{end:%B}**")
    st.write(f"📉 التأثير الموسمي: **{effect:.4f}**")
    st.success(f"🔍 الاتجاه المتوقع: {signal}")

# رسم سعر الذهب
fig = go.Figure()
fig.add_trace(go.Scatter(x=gold['Date'], y=gold['Price'], name="سعر الذهب", line=dict(color='gold')))
fig.update_layout(title="📈 تطور سعر الذهب", xaxis_title="التاريخ", yaxis_title="السعر (USD)")
st.plotly_chart(fig, use_container_width=True)
