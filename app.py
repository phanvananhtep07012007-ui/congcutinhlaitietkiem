import streamlit as st
import pandas as pd
st.image("logo.jpg.jpg")

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="🏦",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("CÔNG CỤ TÍNH LÃI TIẾT KIỆM_PHAN VÂN ANH")
st.write(
    "Nhập thông tin khoản tiền gửi để tính tiền lãi và "
    "tổng số tiền nhận được."
)

st.divider()

# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📝 Thông tin tiền gửi")

so_tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=500_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn gửi (tháng)",
    min_value=1,
    value=3,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=12.0,
    step=0.1
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


# =========================
# NÚT TÍNH
# =========================
if st.button("💰 TÍNH TIỀN LÃI", use_container_width=True):

    # Kiểm tra dữ liệu
    if so_tien_gui <= 0:
        st.error("Số tiền gửi phải lớn hơn 0.")

    elif lai_suat <= 0:
        st.error("Lãi suất phải lớn hơn 0.")

    else:
        # Chuyển lãi suất từ % sang số thập phân
        lai_suat_nam = lai_suat / 100

        # Lãi suất theo tháng
        lai_suat_thang = lai_suat_nam / 12

        # Tổng tiền lãi của toàn bộ kỳ hạn
        tong_tien_lai = (
            so_tien_gui
            * lai_suat_nam
            * ky_han
            / 12
        )

        # Tổng tiền gốc + lãi
        tong_tien_nhan = so_tien_gui + tong_tien_lai

        # =========================
        # TÍNH THEO HÌNH THỨC NHẬN LÃI
        # =========================
        lich_nhan_lai = []

        # -------- CUỐI KỲ --------
        if hinh_thuc == "Cuối kỳ":

            tien_lai_dinh_ky = tong_tien_lai

            lich_nhan_lai.append({
                "Kỳ nhận lãi": f"Cuối tháng {ky_han}",
                "Tiền lãi": tien_lai_dinh_ky
            })

        # -------- HÀNG THÁNG --------
        elif hinh_thuc == "Hàng tháng":

            tien_lai_dinh_ky = (
                so_tien_gui
                * lai_suat_thang
            )

            for thang in range(1, ky_han + 1):
                lich_nhan_lai.append({
                    "Kỳ nhận lãi": f"Tháng {thang}",
                    "Tiền lãi": tien_lai_dinh_ky
                })

        # -------- HÀNG QUÝ --------
        elif hinh_thuc == "Hàng quý":

            tien_lai_mot_thang = (
                so_tien_gui
                * lai_suat_thang
            )

            tien_lai_dinh_ky = tien_lai_mot_thang * 3

            so_quy_day_du = ky_han // 3
            so_thang_le = ky_han % 3

            # Các quý đầy đủ
            for quy in range(1, so_quy_day_du + 1):
                lich_nhan_lai.append({
                    "Kỳ nhận lãi": f"Quý {quy}",
                    "Tiền lãi": tien_lai_dinh_ky
                })

            # Nếu kỳ hạn không chia hết cho 3
            if so_thang_le > 0:
                lai_ky_cuoi = (
                    tien_lai_mot_thang
                    * so_thang_le
                )

                lich_nhan_lai.append({
                    "Kỳ nhận lãi":
                        f"{so_thang_le} tháng còn lại",
                    "Tiền lãi": lai_ky_cuoi
                })

        # =========================
        # HIỂN THỊ KẾT QUẢ
        # =========================
        st.divider()
        st.subheader("📊 Kết quả")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💵 Tiền gửi ban đầu",
                dinh_dang_tien(so_tien_gui)
            )

            st.metric(
                "📅 Kỳ hạn",
                f"{ky_han} tháng"
            )

        with col2:
            st.metric(
                "📈 Lãi suất",
                f"{lai_suat:.2f}%/năm"
            )

            st.metric(
                "🔄 Hình thức nhận lãi",
                hinh_thuc
            )

        st.divider()

        # Tiền lãi định kỳ
        if hinh_thuc == "Cuối kỳ":
            st.info(
                "💰 Tiền lãi nhận cuối kỳ: "
                + dinh_dang_tien(tien_lai_dinh_ky)
            )

        elif hinh_thuc == "Hàng tháng":
            st.info(
                "💰 Tiền lãi nhận mỗi tháng: "
                + dinh_dang_tien(tien_lai_dinh_ky)
            )

        elif hinh_thuc == "Hàng quý":
            st.info(
                "💰 Tiền lãi mỗi quý đầy đủ: "
                + dinh_dang_tien(tien_lai_dinh_ky)
            )

        # =========================
        # CÁC CHỈ SỐ CHÍNH
        # =========================
        col3, col4 = st.columns(2)

        with col3:
            st.metric(
                "💸 Tổng tiền lãi",
                dinh_dang_tien(tong_tien_lai)
            )

        with col4:
            st.metric(
                "💰 Tổng gốc + lãi",
                dinh_dang_tien(tong_tien_nhan)
            )

        # =========================
        # BẢNG LỊCH NHẬN LÃI
        # =========================
        st.divider()
        st.subheader("📆 Lịch nhận lãi")

        df = pd.DataFrame(lich_nhan_lai)

        df["Tiền lãi"] = df["Tiền lãi"].apply(
            dinh_dang_tien
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # =========================
        # GIẢI THÍCH CÔNG THỨC
        # =========================
        with st.expander("📘 Xem công thức tính"):

            st.write("### Công thức")

            st.latex(
                r"""
                \text{Tiền lãi}
                =
                P \times r
                \times
                \frac{n}{12}
                """
            )

            st.write("""
            Trong đó:

            - **P**: Số tiền gửi ban đầu
            - **r**: Lãi suất năm
            - **n**: Số tháng gửi
            """)

            st.write("### Số liệu hiện tại")

            st.write(
                f"Số tiền gửi: "
                f"**{dinh_dang_tien(so_tien_gui)}**"
            )

            st.write(
                f"Lãi suất: **{lai_suat}%/năm**"
            )

            st.write(
                f"Kỳ hạn: **{ky_han} tháng**"
            )

            st.write(
                f"Tổng tiền lãi: "
                f"**{dinh_dang_tien(tong_tien_lai)}**"
            )

# =========================
# GHI CHÚ
# =========================
st.divider()

st.caption(
    "Lưu ý: Ứng dụng giả định lãi suất nhập vào là lãi suất %/năm "
    "và tiền lãi được tính trên số tiền gốc ban đầu. "
    "Kết quả mang tính tham khảo."
)
