import streamlit as st
import pandas as pd
import plotly.express as px
import math
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from imblearn.over_sampling import SMOTE 
from sklearn.metrics import ConfusionMatrixDisplay

def ml_model():
    st.markdown('<h1 style="text-align:center; margin:0;"> Machine Learning</h1>', unsafe_allow_html=True)
    df = pd.read_excel('1. Country Data.xlsx')

    #1. Membagi kolom numerik dan kategorik
    numbers = df.select_dtypes(include=['number']).columns
    categories = df.select_dtypes(exclude=['number']).columns


    #2. Membaca Dataset
    df_select = df[numbers]
    st.write('### Dataset yang digunakan')
    st.dataframe(df_select.head())

    
    #3. Correlation Heatmap untuk melihat korelasi linear antara kolom-kolom numerik
    st.write('### Korelasi Linear antar Kolom Numerik')
    col1, col2 = st.columns([6,4])
    with col1:
    #3.a Correlation Heatmap
        corr = df_select[numbers].corr().round(2)

        # Use custom Heatsage palette provided by user
        heatsage_palette = ["#dfd8d2", "#cbdbcd", "#759c8a", "#00544d", "#5f555a"]

        # Create heatmap with symmetric color range for correlations (-1 to 1)
        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            color_continuous_scale=heatsage_palette,
            zmin=-1,
            zmax=1
        )
        # set heatmap background and font colors
        table_colorbg = '#181818'
        table_colorfg = '#FFFFFF'
        fig.update_layout(
            plot_bgcolor=table_colorbg,
            paper_bgcolor=table_colorbg,
            font_color=table_colorfg
        )
        fig.update_traces(textfont=dict(color=table_colorfg))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
    #3.b Deskripsi Correlation Heatmap
        st.write('**Deskripsi Correlation Heatmap**')
        st.write("""
        - Korelasi **bernilai >0.80**, Korelasi positif yang sangat tinggi.
            Variabel yang memiliki nilai tersebut tidak perlu dihapus,
            karena dengan menghapus variabel dengan korelasi tinggi justru dapat mengurangi kualitas pemisahan cluster.
        - Korelasi **bernilai <0.8**, Korelasi positif yang sedang hingga lemah. 
            Variabel yang memiliki nilai korelasi di bawah 0.8 masih saling berhubungan, 
            tetapi hubungannya tidak terlalu kuat, sehingga setiap variabel tetap memberikan informasi yang berbeda
            dan penting untuk membantu membedakan karakteristik antar negara dalam proses clustering.
        - Korelasi yang **memiliki nilai negatif**, tidak menunjukkan korelasi kuat. 
            Variabel yang memiliki nilai korelasi bertanda negatif menunjukkan hubungan yang berlawanan arah, 
            artinya ketika satu variabel meningkat, variabel lainnya cenderung menurun, 
            namun hubungan ini tidak cukup kuat sehingga tetap berguna untuk menggambarkan 
            perbedaan kondisi antar negara dalam proses clustering.
       """)

    

    #5. Standarisasi kolom numerik dengan Standard Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_select)

    #6. menentukan PCA
    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)   # Mengambil 2 komponen utama
    pca.fit(X_scaled)
    X_pca = pca.transform(X_scaled)
    df_pca = pd.DataFrame(data = X_pca, columns = ['PC 1', 'PC 2'])

    #7. visualisasi scree plot
    pca_full = PCA()
    pca_full.fit(X_scaled)
    expl_var = pca_full.explained_variance_ratio_
    st.write('### Scree Plot')
    fig = px.line(x=range(1, len(expl_var)+1), y=expl_var, markers=True,
                  labels={'x':'Principal Component', 'y':'Explained Variance Ratio'})
    # set line color and marker color
    fig.update_traces(line=dict(color='#75b9bf'), marker=dict(color='#75b9bf'))

    # set plot background and font colors
    table_colorbg = '#181818'
    table_colorfg = '#FFFFFF'
    fig.update_layout(xaxis=dict(dtick=1), plot_bgcolor=table_colorbg, paper_bgcolor=table_colorbg, font_color=table_colorfg)
    st.plotly_chart(fig, use_container_width=True)

    #8. Pemodelan
    df_scaled = pd.DataFrame(X_scaled, columns=df_select.columns)
    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=2, random_state=0).fit(df_scaled)
    clusters = kmeans.labels_
    df['clusters'] = clusters

    #Tabel distribusi cluster
    st.write('### Dataset dengan distribusi cluster')
    st.dataframe(df)

    #9. visualisasi clustering PCA
    st.write('### Visualisasi Clustering dengan PCA')
    # map cluster integers to descriptive labels
    cluster_names = {0: 'Developed Country', 1: 'Developing Country'}
    df_pca['cluster_label'] = df['clusters'].map(cluster_names)

    # define colors for each cluster label
    cluster_colors = {
        'Developed Country': '#75b9bf',
        'Developing Country': '#a7c1a8'
    }

    fig = px.scatter(
        df_pca,
        x='PC 1',
        y='PC 2',
        color='cluster_label',
        color_discrete_map=cluster_colors,
        labels={'cluster_label :': 'Cluster'}
    )

    # style markers (size and outline)
    fig.update_traces(marker=dict(size=8, line=dict(width=1, color='rgba(0,0,0,0.15)')))

    # set plot background and font colors for PCA scatter
    table_colorbg = '#181818'
    table_colorfg = '#FFFFFF'
    fig.update_layout(plot_bgcolor=table_colorbg, paper_bgcolor=table_colorbg, font_color=table_colorfg)

    st.plotly_chart(fig, use_container_width=True)

    #10. evaluasi clustering
    st.write('### Evaluasi Clustering')
    
    # Statistik per cluster
    df2 = df.drop(["country"], axis=1)
    cluster_means = df2.groupby('clusters').mean(numeric_only=True).round(2)
    st.write('**Rata-rata Fitur per Cluster:**')
    st.dataframe(cluster_means)

    col1, col2 = st.columns(2)

    with col1 :
        # Rounded summary card for Cluster 0
        st.markdown(
            f"""
            <div style="background:#3f9aae; padding:12px; border-radius:10px; text-align:center; color:#213448; max-width:320px; margin:8px auto;">
                <div style="font-size:14px; font-weight:600;">Cluster 0</div>
                <div style="font-size:18px; font-weight:700;">🌍 Negara Maju</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background:#75b9bf; padding:14px; border-radius:12px; color:#213448;">
                <div style="white-space:pre-wrap; text-align:left;">
        Negara maju memiliki nilai-nilai yang lebih unggul dibandingkan dengan negara berkembang dari segi ekspor, impor, health, income, life expectancy dan GDPP. Hal tersebut menunjukkan bahwa negara maju memiliki ekonomi kuat, kesehatan baik, dan kualitas hidup yang tinggi.
        
        <strong> - Child Mortality (8.69)</strong>
            Angka kematian anak rendah, menandakan kualitas layanan kesehatan dan gizi yang baik.
        <strong> - Exports (53.25) </strong>
            Tingkat ekspor tinggi, menunjukkan perekonomian yang aktif dan daya saing global yang kuat.
        <strong> - Health (7.93) </strong>
            Pengeluaran untuk kesehatan relatif tinggi, mencerminkan perhatian besar terhadap kualitas hidup masyarakat.
        <strong> - Imports (52.22) </strong>
            Impor tinggi, menandakan aktivitas perdagangan internasional yang stabil dan kebutuhan industri yang besar.
        <strong> - Income (31,006.76) </strong>
            Pendapatan per kapita sangat tinggi, menunjukkan tingkat kesejahteraan masyarakat yang baik.
        <strong> - Inflation (3.93) </strong>
            Inflasi rendah dan stabil, mencerminkan kondisi ekonomi yang terkendali.
        <strong> - Life Expectancy (77.65) </strong>
            Harapan hidup tinggi, menunjukkan kualitas hidup dan layanan kesehatan yang baik.
        <strong> - Total Fertility Rate (1.79) </strong>
            Tingkat kelahiran rendah, umumnya terjadi di negara dengan pendidikan dan urbanisasi tinggi.
        <strong> - GDPP (25,559.19) </strong>
            Produk domestik bruto per kapita tinggi, menandakan ekonomi yang kuat dan maju.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with col2 :
        # Rounded summary card for Cluster 1
        st.markdown(
            f"""
            <div style="background:#3f9aae; padding:12px; border-radius:10px; text-align:center; color:#213448; max-width:320px; margin:8px auto;">
                <div style="font-size:14px; font-weight:600;">Cluster 1</div>
                <div style="font-size:18px; font-weight:700;">🌱 Negara Berkembang</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background:#75b9bf; padding:14px; border-radius:12px; color:#213448;">
                <div style="white-space:pre-wrap; text-align:left;">
        Negara berkembang memiliki ciri dengan nilai child mortality, inflasi, dan total fertility rate yang tinggi dibandingkan dengan negara maju. Hal tersebut menggambarkan negara berkembang masih menghadapi tantangan pada aspek ekonomi, kesehatan, dan stabilitas sosial.

        <strong> - Child Mortality (61.81) </strong>
            Angka kematian anak tinggi, menunjukkan masih adanya tantangan dalam akses dan kualitas layanan kesehatan.
        <strong> - Exports (31.45) </strong>
            Tingkat ekspor lebih rendah, menandakan daya saing ekonomi yang masih terbatas.
        <strong> - Health (5.93) </strong>
            Pengeluaran kesehatan lebih rendah dibanding negara maju, berdampak pada kualitas kesehatan masyarakat.
        <strong> - Imports (42.65) </strong>
            Impor cukup tinggi, namun belum diimbangi dengan ekspor yang kuat.
        <strong> - Income (6,114.66) </strong>
            Pendapatan per kapita rendah, mencerminkan tingkat kesejahteraan masyarakat yang masih terbatas.
        <strong> - Inflation (10.85) </strong>
            Inflasi relatif tinggi, menunjukkan kondisi ekonomi yang kurang stabil.
        <strong> - Life Expectancy (64.91) </strong>
            Harapan hidup lebih rendah, sejalan dengan keterbatasan layanan kesehatan dan kualitas hidup.
        <strong> - Total Fertility Rate (3.87) </strong>
            Tingkat kelahiran tinggi, umumnya terjadi di negara dengan akses pendidikan dan kesehatan yang masih terbatas.
        <strong> - GDPP (2,942.3) </strong>
            GDPP rendah, menandakan kapasitas ekonomi yang masih berkembang.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    

    # Distribusi anggota cluster
    st.write(" ")
    cluster_counts = df['clusters'].value_counts().to_frame().reset_index().rename(columns={"index": "clusters", "clusters": "total_members"})
    st.write('**Distribusi Anggota per Cluster:**')
    st.dataframe(cluster_counts)
    
    # Silhouette Score
    from sklearn.metrics import silhouette_score
    sil_score = silhouette_score(X_scaled, clusters)
    # Display Silhouette Score in a centered rounded card
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:18px; border-radius:12px; text-align:center; color:#213448; max-width:360px; margin:0 auto;">
                <div style="font-size:20px;">Silhouette Score</div>
                <div style="font-size:26px; font-weight:700;">{sil_score:.4f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Simpan model clustering
    import joblib
    joblib.dump(kmeans, "kmeans_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(numbers, "numeric_columns.pkl") 

    #9 . Footer
    st.markdown(
        """
        <hr>
        <p style="text-align:center; color:#FFFFFF;">&copy; 2026 Country Data Dashboard. All rights reserved.</p>
        """,
        unsafe_allow_html=True
    ) 