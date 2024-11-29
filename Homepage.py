import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Cancer Detection Feature Selection", 
    page_icon="🧬", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    .reportview-container { 
        background-color: #072947;
    }
    .stTitle {
        color: #0066cc;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,102,204,0.2);
        text-align: center;
    }
    .stMarkdown {
        color: #FFFFFF;
    }
    .stInfo {
        background-color: #e6f3ff;
        border-left: 6px solid #00a2ff;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,162,255,0.1);
        padding: 15px;
        color: #FFFFFF
    }
    .creator-card {
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 12px;
        text-align: center;
        color: navy;
        font-size: 0.9em;
    }
    .creator-card h3 {
        font-size: 1.1em;
        margin-bottom: 8px;
    }
    .creator-card p {
        margin: 5px 0;
        font-size: 0.85em;
    }
    </style>
""", unsafe_allow_html=True)

# Main Content Sections
def main():
    # Bright Title
    st.title("🧬 Optimized Feature Selection for Cancer Detection")

    # Workflow Section
    st.markdown("### 🌟 Advanced Genomic Exploration Platform")

    # Create two columns for data requirements and info
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        #### **Data Requirements:**
        1. **Gene Expression Data:**
           - *Source*: RNA-seq datasets (STAR-Counts)
           - *Format*: Tabular data 
           - *Columns*: Genes as rows, samples as columns
           - *Content*: Normalized gene expression levels

        2. **Phenotype Data:**
           - *Source*: Clinical datasets (GDC TCGA)
           - *Format*: Sample metadata
        """)

    with col2:
        st.info("""
        🚀 **Research Insight**
        - TCGA-Compliant Processing
        - Advanced Genomic Insights
        - Machine Learning Integration
        """)

    # Future Work Section
    st.markdown("### 🔮 Future Directions")
    st.markdown("""
    - Expand machine learning models
    - Integrate more diverse datasets
    - Develop personalized cancer prediction algorithms
    """)

    # Creator Section
    st.markdown("### 👥 Developer Team")
    
    # Create columns for creator profiles
    creator_cols = st.columns(3)
    
    creators = [
        {
            "name": "Jheno Syechlo",
            "role": "Data Scientist",
            "expertise": "Machine Learning",
            "image": "🧬"
        },
        {
            "name": "Adithama Mulia",
            "role": "Lead Developer",
            "expertise": "Machine Learning",
            "image": "🤖"
        },
        {
            "name": "Vincent Kurniawan",
            "role": "Data Scientist",
            "expertise": "Machine Learning",
            "image": "🔬"
        }
    ]
        
    for i, creator in enumerate(creators):
        with creator_cols[i]:
            st.markdown(f"""
            <div class="creator-card" style="
                background-color: #0d1117; 
                color: #57b1ff; 
                border-radius: 10px; 
                padding: 15px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                border: 1px solid #444;
            ">
                <h3 style="color: #f0f0f0; margin-bottom: 10px;">{creator['image']} {creator['name']}</h3>
                <p style="margin: 5px 0;"><strong style="color: #a0a0a0;">Role:</strong> {creator['role']}</p>
                <p style="margin: 5px 0;"><strong style="color: #a0a0a0;">Expertise:</strong> {creator['expertise']}</p>
            </div>
            """, unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()