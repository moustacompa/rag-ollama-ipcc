import streamlit as st
import requests

st.set_page_config(page_title="RAG IPCC", page_icon="🌍")
st.title("🌍 RAG Demo — IPCC AR6")
st.caption("Powered by Ollama + LangChain")

q = st.text_input("Ask a question about IPCC reports")

if st.button("Ask") and q:
    with st.spinner("Research in progress..."):
        try:
            resp = requests.post(
                "http://localhost:8000/ask",
                json={"question": q},
                timeout=180
            )
            if resp.ok:
                data = resp.json()
                st.subheader("Answer")
                st.write(data["answer"])
                if data.get("sources"):
                    st.subheader("Sources")
                    for src in data["sources"]:
                        st.json(src)
            else:
                st.error(f"Erreur API : {resp.status_code}")
        except requests.exceptions.ReadTimeout:
            st.error("The backend took too long to respond. Try a shorter question, or use a lighter Ollama template..")
        except requests.exceptions.ConnectionError:
            st.error("Unable to contact the backend. Make sure uvicorn is running on port 8000..")