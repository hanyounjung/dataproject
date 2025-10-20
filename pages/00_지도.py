
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Seoul Top 10 for Visitors", page_icon="🗺️", layout="wide")

st.title("🗺️ 서울 외국인 인기 관광지 Top 10 (Folium)")
st.write("**Streamlit + Folium**으로 외국인들이 많이 찾는 서울의 주요 명소 10곳을 지도에 표시했습니다. "
         "왼쪽에서 표시할 장소를 선택하고, 마커 클러스터/경로 보기 옵션을 조정해보세요.")

# ---- 데이터 정의 ----
# 좌표는 공개 자료(구글/오픈맵 기준)와 일반적 안내값을 바탕으로 한 근사치입니다.
PLACES = [
    {
        "name": "경복궁 (Gyeongbokgung Palace)",
        "lat": 37.579617,
        "lon": 126.977041,
        "district": "종로구",
        "station": "경복궁역",
        "desc": "조선의 정궁. 근정전, 경회루가 특히 유명.",
        "tips": "한복 대여 후 입장 시 무료. 11:00 수문장 교대식(변동 가능)."
    },
    {
        "name": "북촌한옥마을 (Bukchon Hanok Village)",
        "lat": 37.582604,
        "lon": 126.983998,
        "district": "종로구",
        "station": "안국역",
        "desc": "전통 한옥 골목 풍경으로 유명한 포토 스팟.",
        "tips": "주거지역이므로 정숙 필수. 오전 방문 추천."
    },
    {
        "name": "인사동 (Insadong)",
        "lat": 37.574034,
        "lon": 126.985495,
        "district": "종로구",
        "station": "안국역/종각역",
        "desc": "전통 공예품, 찻집, 갤러리가 모여 있는 거리.",
        "tips": "전통 다도 체험과 골목 카페 탐방."
    },
    {
        "name": "명동 (Myeong-dong)",
        "lat": 37.563757,
        "lon": 126.985302,
        "district": "중구",
        "station": "명동역",
        "desc": "쇼핑, 길거리 음식, 환전소 밀집 지역.",
        "tips": "저녁 시간 방문 시 네온사인 야경이 매력적."
    },
    {
        "name": "남산 N서울타워 (N Seoul Tower)",
        "lat": 37.551169,
        "lon": 126.988227,
        "district": "용산구",
        "station": "명동역/충무로역",
        "desc": "서울 전망 명소. 케이블카/버스로 접근 가능.",
        "tips": "해 질 녘~야간 방문 추천."
    },
    {
        "name": "동대문디자인플라자 DDP (Dongdaemun Design Plaza)",
        "lat": 37.566477,
        "lon": 127.009041,
        "district": "중구",
        "station": "동대문역사문화공원역",
        "desc": "미래지향적 건축과 전시·야시장으로 유명.",
        "tips": "야간 LED 장미정원 시즌 운영 여부 확인."
    },
    {
        "name": "홍대 거리 (Hongdae Street)",
        "lat": 37.556334,
        "lon": 126.922651,
        "district": "마포구",
        "station": "홍대입구역",
        "desc": "버스킹, 핫플 카페, 클럽/바 문화의 중심.",
        "tips": "주말 저녁 버스킹과 프리마켓 구경."
    },
    {
        "name": "코엑스·스타필드 라이브러리 (COEX & Starfield Library)",
        "lat": 37.512558,
        "lon": 127.059200,
        "district": "강남구",
        "station": "삼성역",
        "desc": "초대형 실내 서가와 쇼핑, 봉은사와 인접.",
        "tips": "코엑스 아쿠아리움 연계 방문."
    },
    {
        "name": "롯데월드타워·석촌호수 (Lotte World Tower & Seokchon Lake)",
        "lat": 37.512501,
        "lon": 127.102778,
        "district": "송파구",
        "station": "잠실역",
        "desc": "123층 전망대와 호수 산책로, 롯데월드 인접.",
        "tips": "벚꽃철 석촌호수 산책 강력 추천."
    },
    {
        "name": "광장시장 (Gwangjang Market)",
        "lat": 37.570159,
        "lon": 127.001795,
        "district": "종로구",
        "station": "종로5가역/을지로4가역",
        "desc": "빈대떡, 마약김밥 등 길거리 음식 천국.",
        "tips": "현금/간편결제 준비. 점심 전 살짝 일찍 방문."
    }
]

# ---- 사이드바 ----
with st.sidebar:
    st.header("🧭 표시 옵션")
    place_names = [p["name"] for p in PLACES]
    selected = st.multiselect("표시할 장소 선택 (기본: 전체)", place_names, default=place_names)
    use_cluster = st.checkbox("마커 클러스터 사용", value=True)
    show_path = st.checkbox("선택한 순서대로 경로(폴리라인) 표시", value=False)
    zoom = st.slider("초기 줌 레벨", min_value=10, max_value=14, value=12)
    st.caption("Tip: 경로 옵션을 켜고 목록 순서를 바꾸려면, 멀티셀렉트에서 선택 순서를 변경해 보세요.")

# ---- 지도 생성 ----
center_lat, center_lon = 37.5665, 126.9780  # 서울시청 근처
m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, control_scale=True, tiles="OpenStreetMap")

# (선택) 마커 클러스터
cluster = MarkerCluster(name="Attractions") if use_cluster else None

# 선택한 장소들만 추출
selected_places = [p for p in PLACES if p["name"] in selected]

# 마커 추가
for p in selected_places:
    popup_html = f"""
    <b>{p['name']}</b><br>
    📍 {p['district']} · 🚇 {p['station']}<br>
    {p['desc']}<br>
    <i>{p['tips']}</i>
    """
    marker = folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=p["name"],
        icon=folium.Icon(icon="info-sign")
    )
    if cluster:
        cluster.add_child(marker)
    else:
        marker.add_to(m)

if cluster:
    m.add_child(cluster)

# 경로(폴리라인) 옵션
if show_path and len(selected_places) >= 2:
    coords = [(p["lat"], p["lon"]) for p in selected_places]
    folium.PolyLine(coords, weight=4, opacity=0.8).add_to(m)

folium.LayerControl().add_to(m)

# ---- 렌더링 ----
st_data = st_folium(m, width="100%", height=650)

# ---- 하단 정보 ----
with st.expander("데이터(Top 10) 보기 / CSV로 저장"):
    import pandas as pd
    df = pd.DataFrame(PLACES)
    st.dataframe(df[["name", "district", "station", "lat", "lon", "desc", "tips"]])
    st.download_button(
        label="CSV 다운로드",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="seoul_top10_attractions.csv",
        mime="text/csv",
    )

st.caption("© Demo for education • Folium tiles: OpenStreetMap contributors")
