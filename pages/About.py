import streamlit as st

st.set_page_config(
    page_icon="assets/logo.png",
    page_title="About Me"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("assets/nazzal.jpg", width=150)
st.markdown("""
## **👨‍💻 About Me – Nazzal**  
### **AI Developer | Machine Learning Engineer**  

Welcome! I’m **Nazzal**, the creator of **TalkToDocs** – an intelligent AI-powered assistant designed to help users interact with their documents..  

---

### **💡 Who Am I?**  
I am an **AI Developer and Machine Learning Engineer** with a passion for building **cutting-edge AI applications**. My expertise lies in **Retrieval-Augmented Generation (RAG), NLP, deep learning, and Machine Learning**.  

### **🚀 My Journey**  
My journey in AI started with a deep curiosity about how machines can **understand, process, and generate human-like responses**. Over time, I have explored various AI technologies, constantly refining my skills to develop practical and impactful AI applications.  


### **🎯 Why I Built TalkToDocs?**  
The idea behind **TalkToDocs** emerged from a common problem: **people struggle to extract meaningful insights from lengthy documents**. Whether it’s research papers, contracts, or legal documents, reading through everything can be time-consuming. With **TalkToDocs**, I wanted to create an **AI-powered assistant that allows users to query and chat with their documents effortlessly.**  

### **📌 Connect with Me**  
I’m always excited to discuss AI, work on innovative projects, and collaborate with fellow developers. If you’d like to see my work or get in touch, check out my portfolio:  
👉 **GitHub**: [nazzal5448](https://github.com/nazzal5448) 


Thank you for visiting! I hope **TalkToDocs** makes your document interactions smoother and more productive. 🚀  

---

This version keeps it concise, focuses on your skills and tools, and highlights **TalkToDocs** as your main project. Let me know if you want any tweaks!
""")