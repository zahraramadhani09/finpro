import streamlit as st

def about_dataset():
    st.markdown('<h1 style="text-align:center; margin-bottom:6px;">🌎 Country Data Analysis 🌎</h1>', unsafe_allow_html=True)
    font_size = 16
    font_weight = 'bold'
    st.markdown('<p style="text-align:center; font-size:16px; font-weight:600; margin:0;">Final Project Data Science - Dibimbing Batch 1 Offline</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; margin:0;">Jakarta, 12 Januari 2026</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; margin-bottom:8px;">Zahra Ramadhani Putri Pramesti</p>', unsafe_allow_html=True)
    
    st.write('---')
    col1, col2= st.columns([5,5])

    with col1:
        link = "https://storage.googleapis.com/kaggle-datasets-images/3020072/5193980/132ea64c2cd4412e47c7e68414f427d1/dataset-cover.jpeg?t=2023-03-19-11-14-57"
        st.image(link, caption="Country Dataset")

    with col2:
        st.write('Dataset ini berisi data sosio-ekonomi dan kesehatan dari 167 negara di dunia, ' \
        'dengan fokus pada indikator pembangunan manusia dan ekonomi. ' \
        'Data dapat digunakan untuk menganalisis hubungan antara faktor ekonomi ' \
        '(seperti pendapatan, perdagangan, inflasi) ' \
        'dan indikator kesehatan (seperti angka kematian anak, ekpetasi hidup, tingkat kesuburan). ')
    
    #9 . Footer
    st.markdown(
        """
        <hr>
        <p style="text-align:center; color:#FFFFFF;">&copy; 2026 Country Data Dashboard. All rights reserved.</p>
        """,
        unsafe_allow_html=True
    )
