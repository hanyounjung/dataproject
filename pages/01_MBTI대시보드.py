import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -----------------------------
# UI 구성
# -----------------------------
st.set_page_config(page_title="🌍 세계 MBTI 비율 대시보드", layout="wide")

st.title("🌍 세계 각국의 MBTI 분포 시각화")
st.markdown("국가를 선택하면 해당 국가의 **16가지 MBTI 비율**을 인터랙티브 막대그래프로 보여줍니다.")

# -----------------------------
# 국가 선택
# -----------------------------
country_list = df["Country"].sort_values().unique()
selected_country = st.selectbox("국가를 선택하세요:", country_list, index=0)

# -----------------------------
# 선택된 국가 데이터 필터링
# -----------------------------
row = df[df["Country"] == selected_country].iloc[0]
mbti_data = row.drop("Country").sort_values(ascending=False).reset_index()
mbti_data.columns = ["MBTI", "Percentage"]

# -----------------------------
# 색상 설정 (1등은 빨간색, 나머지는 그라데이션)
# -----------------------------
colors = ["#ff4d4d"] + px.colors.sequential.Blues[len(mbti_data) - 1:]

# -----------------------------
# 그래프 생성
# -----------------------------
fig = px.bar(
    mbti_data,
    x="MBTI",
    y="Percentage",
    title=f"🇺🇳 {selected_country}의 MBTI 유형 분포",
    text=mbti_data["Percentage"].apply(lambda x: f"{x*100:.1f}%"),
    color=mbti_data["MBTI"],
    color_discrete_sequence=colors,
)

# 디자인 개선
fig.update_traces(textposition="outside")
fig.update_layout(
    showlegend=False,
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis_tickformat=".0%",
    plot_bgcolor="white",
    font=dict(size=14),
)

# -----------------------------
# 그래프 출력
# -----------------------------
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 데이터 표 표시
# -----------------------------
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(df.style.format("{:.2%}", subset=df.columns[1:]))
