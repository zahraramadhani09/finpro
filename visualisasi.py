import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def chart():
    st.markdown('<h1 style="text-align:center; margin:0;"> Country Development Dashboard</h1>', unsafe_allow_html=True)
    
    # Tambahkan timestamp update
    st.markdown(f'<p style="text-align:center; color:#75b9bf; font-size:14px;">Last Updated: {datetime.now().strftime("%d %B %Y, %H:%M:%S")}</p>', unsafe_allow_html=True)
    
    df = pd.read_excel('1. Country Data.xlsx')
    
    #SIDEBAR FILTER
    st.sidebar.markdown("### 🔍 Filter Data")
    
    # Initialize session state
    if 'countries_selected' not in st.session_state:
        st.session_state.countries_selected = df["country"].unique()[:10].tolist()
    
    all_countries = df["country"].unique().tolist()
    
    # Buttons with better styling
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("✅ Select All", use_container_width=True):
            st.session_state.countries_selected = all_countries
            st.rerun()
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.countries_selected = []
            st.rerun()
    
    # Multiselect
    selected_country = st.sidebar.multiselect(
        "Pilih Negara:",
        options=all_countries,
        default=st.session_state.countries_selected,
        key='country_multiselect'
    )
    
    st.session_state.countries_selected = selected_country
    
    # FITUR BARU 1: Advanced Filters dengan Expander
    with st.sidebar.expander("🎯 Advanced Filters", expanded=False):
        # Filter by Development Level
        dev_levels = st.multiselect(
            "Development Level:",
            options=df['development_level'].unique(),
            default=df['development_level'].unique()
        )
        
        # Filter by Income Level
        income_levels = st.multiselect(
            "Income Level:",
            options=df['income_level'].unique(),
            default=df['income_level'].unique()
        )
        
        # Filter by GDP Range
        gdp_range = st.slider(
            "GDP per Capita Range:",
            min_value=int(df['gdpp'].min()),
            max_value=int(df['gdpp'].max()),
            value=(int(df['gdpp'].min()), int(df['gdpp'].max()))
        )
    
    # Apply all filters
    if len(selected_country) > 0:
        df_filtered = df[
            (df["country"].isin(selected_country)) &
            (df['development_level'].isin(dev_levels)) &
            (df['income_level'].isin(income_levels)) &
            (df['gdpp'] >= gdp_range[0]) &
            (df['gdpp'] <= gdp_range[1])
        ]
    else:
        df_filtered = df
        st.sidebar.warning("⚠️ Tidak ada negara dipilih")
    
    # FITUR BARU 2: Info Card dengan Animasi
    st.sidebar.markdown("---")
    st.sidebar.metric(
        label="📊 Countries Selected",
        value=len(selected_country),
        delta=f"{len(selected_country) - len(all_countries)} from total"
    )
    st.sidebar.metric(
        label="📋 Data Rows",
        value=len(df_filtered),
        delta=f"{len(df_filtered) - len(df)} filtered"
    )
    
    # FITUR BARU 3: Download Button
    st.sidebar.markdown("---")
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name=f'country_data_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        use_container_width=True
    )
    
    # Styling
    st.markdown("""
        <style>
        .stApp {background-color: #181818;}
        </style>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #282828 !important;
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] * {color: #FFFFFF !important;}
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] .stMultiSelect,
        [data-testid="stSidebar"] .stSelectbox {
            background-color: #1e1e1e !important;
            color: #FFFFFF !important;
            border-color: #75b9bf !important;
            border-width: 2px;
        }
        [data-testid="stSidebar"] [role="listbox"] {
            background-color: #75b9bf !important;
            color: #FFFFFF !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # FITUR BARU 4: KPI Metrics dengan Progress Bar dan Delta
    st.markdown("### 📈 Key Performance Indicators")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    avg_income = df_filtered['income'].mean()
    avg_gdpp = df_filtered['gdpp'].mean()
    avg_life = df_filtered['life_expec'].mean()
    avg_mort = df_filtered['child_mort'].mean()
    
    with kpi_col1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #91c6bc 0%, #75b9bf 100%); 
                        padding:15px; border-radius:15px; text-align:center; 
                        color:#213448; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <div style="font-size:16px; font-weight:600;">💰 Avg Income</div>
                <div style="font-size:24px; font-weight:bold; margin:10px 0;">{avg_income:,.0f}</div>
                <div style="font-size:12px; opacity:0.8;">Per Year</div>
            </div>
            """, unsafe_allow_html=True)
        st.progress(min(avg_income / df['income'].max(), 1.0))
    
    with kpi_col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #91c6bc 0%, #75b9bf 100%); 
                        padding:15px; border-radius:15px; text-align:center; 
                        color:#213448; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <div style="font-size:16px; font-weight:600;">📈 Avg GDP/Capita</div>
                <div style="font-size:24px; font-weight:bold; margin:10px 0;">{avg_gdpp:,.0f}</div>
                <div style="font-size:12px; opacity:0.8;">Per Person</div>
            </div>
            """, unsafe_allow_html=True)
        st.progress(min(avg_gdpp / df['gdpp'].max(), 1.0))
    
    with kpi_col3:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #91c6bc 0%, #75b9bf 100%); 
                        padding:15px; border-radius:15px; text-align:center; 
                        color:#213448; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <div style="font-size:16px; font-weight:600;">❤️ Avg Life Expectancy</div>
                <div style="font-size:24px; font-weight:bold; margin:10px 0;">{avg_life:.1f}</div>
                <div style="font-size:12px; opacity:0.8;">Years</div>
            </div>
            """, unsafe_allow_html=True)
        st.progress(min(avg_life / df['life_expec'].max(), 1.0))
    
    with kpi_col4:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #91c6bc 0%, #75b9bf 100%); 
                        padding:15px; border-radius:15px; text-align:center; 
                        color:#213448; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <div style="font-size:16px; font-weight:600;">⚠️ Avg Child Mortality</div>
                <div style="font-size:24px; font-weight:bold; margin:10px 0;">{avg_mort:.1f}</div>
                <div style="font-size:12px; opacity:0.8;">Per 1000</div>
            </div>
            """, unsafe_allow_html=True)
        st.progress(max(1 - (avg_mort / df['child_mort'].max()), 0))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # FITUR BARU 5: Tabs untuk organize content
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Overview", "📈 Economic Analysis", "🏥 Health Metrics", "🌍 Geographic Distribution"])
    
    with tab1:
        # Dataset Preview with search
        st.subheader("📋 Dataset Preview")

        # Controls row
        col_search, col_sort, col_order, col_rows = st.columns([3, 2, 1, 1])
        
        with col_search:
            search_term = st.text_input(
                "🔍 Search in dataset:",
                placeholder="Type country name...",
                key="search_dataset"
            )
        
        with col_sort:
            sort_by = st.selectbox(
                "📊 Sort by:",
                options=['country', 'gdpp', 'income', 'life_expec', 'child_mort', 'exports', 'imports'],
                index=0,
                key="sort_dataset"
            )
        
        with col_order:
            sort_order = st.selectbox(
                "⬆️⬇️",
                options=['Asc', 'Desc'],
                index=0,
                key="order_dataset"
            )
        
        with col_rows:
            show_rows = st.selectbox(
                "Rows:",
                options=[10, 25, 50, 100, 'All'],
                index=1,
                key="rows_dataset"
            )
        
        # Apply search filter
        if search_term:
            df_display = df_filtered[df_filtered['country'].str.contains(search_term, case=False, na=False)]
        else:
            df_display = df_filtered.copy()
        
        # Apply sorting
        ascending = True if sort_order == 'Asc' else False
        df_display = df_display.sort_values(by=sort_by, ascending=ascending)
        
        # Reset index untuk urutan yang rapi
        df_display = df_display.reset_index(drop=True)
        
        # Apply row limit
        if show_rows != 'All':
            df_display = df_display.head(show_rows)
        
        # Display info
        st.info(f"📊 Showing {len(df_display)} of {len(df_filtered)} countries (Total in database: {len(df)})")
        
        # Display dataframe dengan styling
        st.dataframe(
            df_display,
            use_container_width=True,
            height=500,
            hide_index=False,
            column_config={
                "country": st.column_config.TextColumn("Country", width="medium"),
                "gdpp": st.column_config.NumberColumn("GDP/Capita", format="%d"),
                "income": st.column_config.NumberColumn("Income", format="%d"),
                "life_expec": st.column_config.NumberColumn("Life Exp", format="%.1f"),
                "child_mort": st.column_config.NumberColumn("Child Mort", format="%.2f"),
                "exports": st.column_config.NumberColumn("Exports ", format="%.1f"),
                "imports": st.column_config.NumberColumn("Imports ", format="%.1f"),
                "inflation": st.column_config.NumberColumn("Inflation ", format="%.2f"),
                "fertility": st.column_config.NumberColumn("Fertility", format="%.2f"),
            }
        )
        
        # Summary Statistics
        st.subheader("📊 Summary Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_filtered.describe().round(2), use_container_width=True)
        with col2:
            # Top 5 Countries by GDP
            st.markdown("**🏆 Top 5 by GDP per Capita**")
            top5 = df_filtered.nlargest(5, 'gdpp')[['country', 'gdpp', 'income']]
            st.dataframe(top5, use_container_width=True, hide_index=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar Chart GDP
            st.markdown("### 📊 GDP per Capita by Country")
            fig_gdpp = px.bar(
                df_filtered.nlargest(20, 'gdpp'),
                x='country',
                y='gdpp',
                labels={'gdpp': 'GDP per Capita', 'country': 'Country'},
                color='gdpp',
                color_continuous_scale='Teal'
            )
            fig_gdpp.update_layout(
                plot_bgcolor='#181818',
                paper_bgcolor='#181818',
                font_color='#FFFFFF',
                showlegend=False
            )
            st.plotly_chart(fig_gdpp, use_container_width=True)
        
        with col2:
            # Trade Balance
            st.markdown("### 💹 Export vs Import")
            df_filtered['trade_balance'] = df_filtered['exports'] - df_filtered['imports']
            fig_trade = px.bar(
                df_filtered.nlargest(20, 'trade_balance'),
                x='country',
                y='trade_balance',
                labels={'trade_balance': 'Trade Balance', 'country': 'Country'},
                color='trade_balance',
                color_continuous_scale=['#ff6b6b', '#4ecdc4']
            )
            fig_trade.update_layout(
                plot_bgcolor='#181818',
                paper_bgcolor='#181818',
                font_color='#FFFFFF'
            )
            st.plotly_chart(fig_trade, use_container_width=True)
        
    
    with tab3:
       
            # Life Expectancy Distribution
            st.markdown("### 📊 Life Expectancy Distribution")
            fig_hist = px.histogram(
                df_filtered,
                x='life_expec',
                nbins=30,
                labels={'life_expec': 'Life Expectancy (years)'},
                color_discrete_sequence=['#75b9bf']
            )
            fig_hist.update_layout(
                plot_bgcolor='#181818',
                paper_bgcolor='#181818',
                font_color='#FFFFFF'
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        
    
    with tab4:
        # Risk Distribution Donuts
        st.markdown("### 🎯 Risk & Development Distribution")
        col1, col2, col3, col4 = st.columns(4)
        
        donut_data = [
            (col1, 'inflation_risk', 'Inflation Risk', '💹'),
            (col2, 'mortality_risk', 'Mortality Risk', '🏥'),
            (col3, 'income_level', 'Income Level', '💰'),
            (col4, 'development_level', 'Development Level', '🌍')
        ]
        
        for col, field, title, emoji in donut_data:
            with col:
                counts = df_filtered[field].value_counts().reset_index()
                counts.columns = [field, 'count']
                fig = px.pie(
                    counts,
                    names=field,
                    values='count',
                    title=f'{emoji} {title}',
                    hole=0.5,
                    color_discrete_sequence=['#75b9bf', '#91c6bc', '#dceae9', '#6d8387']
                )
                fig.update_layout(
                    plot_bgcolor='#181818',
                    paper_bgcolor='#181818',
                    font_color='#FFFFFF',
                    showlegend=True,
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # World comparison
        st.markdown("### 🌏 Global Comparison")
        comparison_metric = st.selectbox(
            "Select metric to compare:",
            ['gdpp', 'income', 'life_expec', 'child_mort', 'exports', 'imports']
        )
        
        fig_comparison = px.bar(
            df_filtered.nlargest(30, comparison_metric),
            x='country',
            y=comparison_metric,
            color=comparison_metric,
            color_continuous_scale='Teal',
            labels={comparison_metric: comparison_metric.upper()}
        )
        fig_comparison.update_layout(
            plot_bgcolor='#181818',
            paper_bgcolor='#181818',
            font_color='#FFFFFF'
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align:center; padding:20px; background: linear-gradient(135deg, #1e1e1e 0%, #282828 100%); 
                    border-radius:10px; margin-top:30px;">
            <p style="color:#FFFFFF; margin:0;">© 2026 Country Data Dashboard. All rights reserved.</p>
            <p style="color:#75b9bf; margin:5px 0; font-size:12px;">Built with Streamlit & Plotly</p>
        </div>
        """, unsafe_allow_html=True)