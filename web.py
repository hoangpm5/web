import streamlit as st
from sklearn.linear_model import LinearRegression
import feedparser

st.sidebar.title("🎶 Danh sách nghệ sĩ")
selected_artist = st.sidebar.radio("Chọn nghệ sĩ:", ["Đen Vâu", "Hà Anh Tuấn", "Sơn Tùng M-TP", "Những bản nhạc giúp tâm trạng vui vẻ hơn"])

videos = {
    "Đen Vâu": [
        ("Bữa ăn cho em", "https://www.youtube.com/watch?v=ukHK1GVyr0I"),
        ("Mang tiền về cho mẹ", "https://www.youtube.com/watch?v=UVbv-PJXm14"),
        ("Trời hôm nay nhiều mây cực!", "https://www.youtube.com/watch?v=MBaF0l-PcRY"),
        ("Hai triệu năm", "https://www.youtube.com/watch?v=LSMDNL4n0kM")
    ],
    "Hà Anh Tuấn": [
        ("Tuyết rơi mùa hè", "https://www.youtube.com/watch?v=pTh3KCD7Euc"),
        ("Nước ngoài", "https://www.youtube.com/watch?v=pU3O9Lnp-Z0"),
        ("Tháng tư là lời nói dối của em", "https://www.youtube.com/watch?v=UCXao7aTDQM"),
        ("Xuân thì", "https://www.youtube.com/watch?v=3s1r_g_jXNs")
    ],
    "Sơn Tùng M-TP": [
        ("Lạc trôi", "https://www.youtube.com/watch?v=Llw9Q6akRo4"),
        ("Chúng ta không thuộc về nhau", "https://www.youtube.com/watch?v=qGRU3sRbaYw"),
        ("Muộn rồi mà sao còn", "https://www.youtube.com/watch?v=xypzmu5mMPY"),
        ("Hãy trao cho anh", "https://www.youtube.com/watch?v=knW7-x7Y7RE")
    ],
    "Những bản nhạc giúp tâm trạng vui vẻ hơn":[
        ("Những bản nhạc giúp tâm trạng vui vẻ hơn", "https://www.youtube.com/watch?v=SlsH6PbDJZk&t=898s"),
        ("Lỡ Duyên", "https://www.youtube.com/watch?v=fq_H4A3HgD4&list=RDfq_H4A3HgD4&start_radio=1&rv=fq_H4A3HgD4"),
        ("Bài hat về tình yêu quê hương đất nước", "https://www.youtube.com/watch?v=GOMGeUetqlI&list=RDSlsH6PbDJZk&index=3"),
        ("Đi giữa trời rực rỡ", "https://www.youtube.com/watch?v=D1Uf9vREh6Q&list=RDSlsH6PbDJZk&index=3"),
        ("STAY HOME, STAY HAPPY, STAY HÀANHTUẤN", "https://www.youtube.com/watch?v=MMgPOQ9gJhM&list=RDEMrx5Xy48sg-WCr9qiaw1hhg&index=2"),
    ]
}

st.title("🎧 Ứng dụng giải trí và sức khỏe")

tab1, tab2, tab3, tab4 = st.tabs(["🎤 MV yêu thích", "💤 Dự đoán giờ ngủ", "📰 Đọc báo", "💰 Giá vàng" ])

with tab1:
    st.header(f"Các bài hát của {selected_artist} 🎵")
    for title, url in videos[selected_artist]:
        st.subheader(title)
        st.video(url)

with tab2:
    st.header("🔮 Dự đoán giờ ngủ mỗi đêm")

    x = [
        [10, 1, 8],
        [20, 5, 6],
        [25, 8, 3],
        [30, 6, 5],
        [35, 2, 9],
        [40, 4, 3]
    ]
    y = [10, 8, 6, 7, 9.5, 9]

    model = LinearRegression()
    model.fit(x, y)

    st.write("Nhập thông tin cá nhân:")
    age = st.number_input("Tuổi của bạn", min_value=5, max_value=100, value=25)
    activity = st.slider("Mức độ hoạt động thể chất (1 = ít, 10 = rất nhiều)", 1, 10, 5)
    screen_time = st.number_input("Thời gian dùng màn hình mỗi ngày (giờ)", min_value=0, max_value=24, value=6)

    if st.button("💤 Dự đoán ngay"):
        input_data = [[age, activity, screen_time]]
        result = model.predict(input_data)[0]
        st.success(f"Bạn nên ngủ khoảng {result:.1f} giờ mỗi đêm")

        if result < 6.5:
            st.warning("😴 Có thể bạn cần nghỉ ngơi nhiều hơn để cải thiện sức khỏe.")
        elif result > 9:
            st.info("😅 Có thể bạn đang vận động nhiều – ngủ bù hợp lý nhé.")
        else:
            st.success("✅ Lượng ngủ lý tưởng! Hãy giữ thói quen tốt nhé.")
with tab3:
    st.header("📰 Tin tức mới nhất từ VnExpress")
    feed = feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
    for entry in feed.entries[:5]:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(entry.link)
# Tab 4: Giá vàng
with tab4:
    st.header("💰 Cập nhật giá vàng trong nước và thế giới")

    # Lấy bản tin từ Vietnamnet
    feed = feedparser.parse("https://vietnamnet.vn/rss/kinh-doanh.rss")
    gold_news = [entry for entry in feed.entries if "vàng" in entry.title.lower() or "giá vàng" in entry.summary.lower()]

    displayed = False
    gia_vang_trong_nuoc = None

    for entry in gold_news:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(f"[Đọc chi tiết]({entry.link})")
        
        # Tìm giá vàng trong nội dung
        match = re.search(r"(\d{2,3}[.,]?\d{3})\s?(triệu|nghìn)?", entry.title + entry.summary)
        if match and not gia_vang_trong_nuoc:
            raw = match.group(1).replace(".", "").replace(",", "")
            try:
                value = int(raw)
                if value > 30_000_000:  # Có thể là giá vàng
                    gia_vang_trong_nuoc = value
            except:
                pass
        displayed = True

        if displayed:
            break  # Hiện 1 bản tin đầu tiên

    # Hiển thị giá thế giới và tính chênh lệch
    gia_vang_the_gioi_usd = 2350  # Ví dụ: 2.350 USD/ounce (cập nhật thủ công hoặc qua API nếu có)
    ty_gia = 24000
    gia_vang_the_gioi_vnd = gia_vang_the_gioi_usd * ty_gia * 0.829  # 1 ounce ≈ 0.829 lượng vàng

    st.markdown("---")
    st.subheader("📊 So sánh giá vàng:")

    if gia_vang_trong_nuoc:
        st.success(f"🏠 Giá vàng trong nước: **{gia_vang_trong_nuoc:,.0f} VNĐ/lượng**")
    else:
        st.warning("Không lấy được giá vàng trong nước từ tin tức.")

    st.info(f"🌍 Giá vàng thế giới quy đổi: **{gia_vang_the_gioi_vnd:,.0f} VNĐ/lượng**")

    if gia_vang_trong_nuoc:
        chenh_lech = gia_vang_trong_nuoc - gia_vang_the_gioi_vnd
        st.write(f"📈 Mức chênh lệch: **{chenh_lech:,.0f} VNĐ/lượng**")
        if chenh_lech > 0:
            st.warning("💰 Giá trong nước cao hơn thế giới.")
        else:
            st.success("✅ Giá trong nước thấp hơn hoặc ngang với thế giới.")
