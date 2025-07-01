
import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objs as go
import yfinance as yf

# إعداد الصفحة
st.set_page_config(page_title="GoldSmart - التحليل الموسمي للذهب", layout="wide")
st.title("📊 GoldSmart Dashboard - تحليل موسمي كامل للذهب")

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

# إنشاء جدول بجميع الشهور
months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]

table_data = []
for i in range(1, 13):
    effect = seasonal_effects.get(i, 1)
    signal = '📈 Bullish' if effect > 1 else '📉 Bearish'
    table_data.append({
        "Month": months[i-1],
        "Seasonal Effect": round(effect, 6),
        "Signal": signal
    })

df_season = pd.DataFrame(table_data)

# عرض جدول التحليل الموسمي
st.subheader("📅 التحليل الموسمي حسب كل شهر:")
st.table(df_season)

# عرض السعر الحالي للذهب
st.subheader("📈 السعر الحالي للذهب:")
st.metric("سعر الأونصة", f"{data['Price'].iloc[-1]:,.2f} USD")

# رسم بياني لتطور السعر
st.subheader("🔻 تطور سعر الذهب خلال آخر 5 سنوات")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['Date'], y=data['Price'], name='Gold Price', line=dict(color='gold')))
fig.update_layout(title="Gold Price Over Time", xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig, use_container_width=True)
