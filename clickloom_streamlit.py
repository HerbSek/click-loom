import streamlit as st
import json
import time
import plotly.graph_objects as go
from clickloom_llm import llm 
import requests

st.set_page_config(page_title="Clickloom.io - Website Dashboard", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # st.image("logo.png", width=200)  # Add a logo image file
    st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>Clickloom.io</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: grey;'>Website Risk Intelligent Agent</h4>", unsafe_allow_html=True)
    st.markdown("---")

    user_input = st.text_input("Enter Website URL:", placeholder="https://example.com")
    analyze_button = st.button("🚨 Analyze Website", type="primary", disabled=not user_input.startswith(("http://", "https://")))

# Button to load JSON
if analyze_button:
    # Define URL and payload from user input
    url = "https://selenium-scraper-sayw.onrender.com/scrape"  # Replace with your actual API endpoint
    payload = {"link": user_input}
    
    progress_bar = st.progress(0)
    with st.spinner("Running analysis..."):
        try:
            progress_bar.progress(25)
            response = requests.get(url, params=payload)
            response.raise_for_status()  # Check for HTTP errors
            data1 = response.json()
            progress_bar.progress(50)
            
            with st.status("Processing website data...") as status:
                st.write("Analyzing website content...")
                results = llm(data1)
                progress_bar.progress(100)
                status.update(label="Analysis complete!", state="complete")
            
            data = results
            
            # Check if required keys exist
            required_keys = ["verdict", "risk_score", "page_text_findings", "script_analysis", "link_analysis"]
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                st.error(f"Missing data in analysis results: {', '.join(missing_keys)}")
                st.stop()
                
            # Top Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Verdict", data["verdict"])
            col2.metric("Risk Score", f"{data['risk_score']}/10")
            col3.metric("Suspicious Phrases", len(data["page_text_findings"]["suspicious_phrases"]))

            # Pie Chart - Risk Visualization
        
            risk_score = data['risk_score']
            safe_score = 10 - risk_score
            left, right = st.columns(2)

            with left:
                st.write(" ")
                st.write(" ")
                st.subheader("🔍 Summary")
                st.info(data["summary"])

                st.subheader("⚠️ Recommendations")
                st.warning(data["recommendations"])

                st.subheader("🕵️ Suspicious Phrases")
                for phrase in data["page_text_findings"]["suspicious_phrases"]:
                    st.markdown(f"- 🔸 {phrase}")
                if data["page_text_findings"]["phishing_indicators"]:
                    st.error("Phishing Indicators: **Detected**")
                else:
                    st.info("Phishing Indicators: **None Detected**")

            # Main Layout - Findings and Technical Details
       

            # right Column - Summary + Findings
            with right:
               st.write(" ")
               st.write(" ")
               st.markdown("### Risk Score Breakdown")
               fig = go.Figure(data=[go.Pie(
                    labels=['Risk', 'Safe'],
                    values=[risk_score, safe_score],
                    hole=0.5,
                    marker=dict(colors=["#EF553B", "#00CC96"])
                )])
               fig.update_layout(width=600, height=600, showlegend=True)

               st.plotly_chart(fig, use_container_width=True)


        
            tab1, tab2, tab3 = st.tabs(["Summary", "Script Analysis", "Link Analysis"])

            with tab1:
                st.subheader("📊 Summary")
                # Summary content here

            with tab2:
                st.subheader("📜 Script Analysis")
                st.markdown(f"- **Total Scripts:** {data['script_analysis']['total_scripts']}")
                st.markdown(f"- **External Scripts:** {data['script_analysis']['external_scripts']}")
                st.markdown(f"- **Suspicious Domains:**")
                for d in data['script_analysis']['suspicious_domains']:
                    st.markdown(f"  - ❗ {d}")
                if data["script_analysis"]["minified_or_encoded"]:
                    st.warning("Minified or Encoded Scripts: Detected")

            with tab3:
                st.subheader("🔗 Link Analysis")
                st.markdown(f"- **Total Links:** {data['link_analysis']['total_links']}")
                st.markdown(f"- **External Links:** {data['link_analysis']['external_links']}")

                st.markdown(f"- **Redirect Services Used:**")
                if data['link_analysis']['redirect_services_used']:
                    for r in data['link_analysis']['redirect_services_used']:
                        st.markdown(f"  - {r}")
                else:
                    st.markdown("*None*")

                st.markdown(f"- **Phishing-like Links:**")
                if data['link_analysis']['phishing_like_links']:
                    for p in data['link_analysis']['phishing_like_links']:
                        st.markdown(f"  - {p}")
                else:
                    st.markdown("*None*")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to scraper service: {e}")
            st.stop()
        except json.JSONDecodeError:
            st.error("Invalid response from scraper service")
            st.stop()
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.stop()

    # Footer
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: grey;'>© 2025 Clickloom.io — Making the web safer, one link at a time.</p>", unsafe_allow_html=True)
else:
    st.info("Click the button above to load and analyze the website report.")


