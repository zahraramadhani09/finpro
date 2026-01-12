import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

def prediction_app():

    #1. Load Model & Metadata
    model = joblib.load("kmeans_model.pkl")
    scaler = joblib.load("scaler.pkl")
    numeric_cols = joblib.load("numeric_columns.pkl")
    
    # Add CSS to center input labels and increase font size
    st.markdown(
        """
        <style>
        .stNumberInput > label {
            text-align: left;
            width: 100%;
            display: block;
            font-size: 30px;
            font-weight: 800;
        }
        /* center the numeric value inside Streamlit number_input fields */
        .stNumberInput input[type="number"],
        .stNumberInput input {
            text-align: left;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    #2. Form Input Pengguna
    st.markdown('<h3 style="text-align:center; font-size : 35px;">Input Data Country</h3>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-size:16px; color:#FFFFFF; margin-top:4px;">Input information about a country to predict its category based on socio-economic indicators</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        gdpp = st.number_input("GDP per capita :", 0.0, 100000.0, 1000.0)
        if gdpp < 1000:
            gdp_category = "Low"
        elif gdpp < 12000:
            gdp_category = "Middle"
        else:
            gdp_category = "High"
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:10px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:13px;">GDP Category</div>
                <div style="font-size:16px;font-weight:bold;">{gdp_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        income = st.number_input("Income :", 0.0, 100000.0, 5000.0)
        if income < 1000:
            income_category = "Low"
        elif income < 12000:
            income_category = "Middle"
        else:
            income_category = "High"
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:10px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:13px;">Income Category</div>
                <div style="font-size:16px;font-weight:bold;">{income_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        exports = st.number_input("Exports :", 0.0, 100000.0, 2000.0)
        if exports < 500:
            exports_category = "Low"
        elif exports < 5000:
            exports_category = "Medium"
        else:
            exports_category = "High"
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:10px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:13px;">Exports Category</div>
                <div style="font-size:16px;font-weight:bold;">{exports_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("   ")
        child_mort = st.number_input("Child Mortality :", 0.0, 100.0, 10.0)
        if child_mort < 20:
            child_mort_category = "Low"
        elif child_mort < 50:
            child_mort_category = "Medium"
        else:
            child_mort_category = "High"
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:10px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:13px;">Child Mortality Category</div>
                <div style="font-size:16px;font-weight:bold;">{child_mort_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.write("   ")
        inflation = st.number_input("Inflation :", 0.0, 100.0, 5.0)
        if inflation < 3:
            inflation_category = "Low"
        elif inflation < 10:
            inflation_category = "Medium"
        else:
            inflation_category = "High"
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:10px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:13px;">Inflation Category</div>
                <div style="font-size:16px;font-weight:bold;">{inflation_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.write("   ")
        imports = st.number_input("Imports :", 0.0, 100000.0, 1500.0)
        if imports < 500:
            imports_category = "Low"
        elif imports < 5000:
            imports_category = "Medium"
        else:
            imports_category = "High"
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:10px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:13px;">Imports Category</div>
                <div style="font-size:16px;font-weight:bold;">{imports_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("   ")
        total_fer = st.number_input("Total Fertility Rate :", 0.0, 10.0, 2.5)
        if total_fer < 2:
            fertility_category = "Low"
        elif total_fer < 4:
            fertility_category = "Medium"
        else:
            fertility_category = "High"
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:10px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:13px;">Fertility Rate Category</div>
                <div style="font-size:16px;font-weight:bold;">{fertility_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.write("")

    with col2:
        st.write("   ")
        life_expec = st.number_input("Life Expectancy :", 0.0, 100.0, 70.0)
        if life_expec < 60:
            life_category = "Low"
        elif life_expec < 75:
            life_category = "Medium"
        else:
            life_category = "High"
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:10px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:13px;">Life Expectancy Category</div>
                <div style="font-size:16px;font-weight:bold;">{life_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.write("")

    with col3:
        st.write("   ")
        health = st.number_input("Health :", 0.0, 100.0, 50.0)
        if health < 30:
            health_category = "Low"
        elif health < 70:
            health_category = "Medium"
        else:
            health_category = "High"
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:10px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:13px;">Health Category</div>
                <div style="font-size:16px;font-weight:bold;">{health_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.write("")

    # 4. Prediction Button
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        predict_button = st.button("🔎  Make Prediction", use_container_width=True)

    if predict_button:
        #3. Masukkan menjadi DataFrame
        user_df = pd.DataFrame({
            "gdpp": [gdpp],
            "income": [income],
            "exports": [exports],
            "child_mort": [child_mort],
            "inflation": [inflation],
            "imports": [imports],
            "total_fer": [total_fer],
            "life_expec": [life_expec],
            "health": [health],
            "gdp_category": [gdp_category],
            "income_category": [income_category],
            "exports_category": [exports_category],
            "inflation_category": [inflation_category],
            "imports_category": [imports_category],
            "life_category": [life_category],
            "child_mort_category": [child_mort_category],
            "health_category": [health_category]
        })

        #5. mapping cluster menjadi kategori negara
        cluster_mapping = {
            0: "Developed Country",
            1: "Developing Country"
        }
        country_category = cluster_mapping.get(model.predict(scaler.transform(user_df[numeric_cols]))[0], "Unknown")

        #prediksi cluster dari input user
        cluster_pred = model.predict(scaler.transform(user_df[numeric_cols]))[0]
        country_category = cluster_mapping.get(cluster_pred, "Unknown")

        #Tampilkan hasil prediksi dengan KPI Card
        st.write("#### Based on the socio-economic indicators provided, this country is classified as :")
        st.markdown(
            f"""
            <div style="background:#91c6bc; padding:20px; border-radius:10px; text-align:center; color:#213448;">
                <div style="font-size:30px;font-weight:bold;">{country_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    #9 . Footer
    st.markdown(
        """
        <hr>
        <p style="text-align:center; color:#FFFFFF;">&copy; 2026 Country Data Dashboard. All rights reserved.</p>
        """,
        unsafe_allow_html=True
    )
    

if __name__ == "__main__":
    prediction_app()
