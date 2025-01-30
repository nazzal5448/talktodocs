import streamlit as st
st.set_page_config(page_title="TalkToDocs",
                   page_icon="assets/logo.png",
                   initial_sidebar_state="collapsed"
                   )
logo_path = "assets/logo.png"  # Update this to your logo's path

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo_path, width=250)


st.markdown("""
# Welcome to **TalkToDocs**! 📄🗣️  

## **Your Intelligent Document Assistant**  
---

### **📌 Key Features** 🚀  

✅ **Upload Documents**  
   - Supports **PDF, TXT, and DOCX** formats  
   - Handles **text, images, and tables**  

✅ **Ask Questions**  
   - Get **accurate answers** based on the document's content  
   - Extract meaningful insights quickly  

✅ **Voice & Text Interaction**  
   - **Type or speak** your questions  
   - Receive responses in **text and voice** formats  

✅ **Multi-Modal Support**  
   - Works with **text, images, and tables**  
   - Extracts and processes relevant information intelligently  

---

### **⚙️ How It Works**  

1. **Upload**: Choose a document to upload  
2. **Process**: The app analyzes the document for interaction  
3. **Interact**: Summarize, ask questions, or chat with your document  
4. **Get Results**: Receive **instant and context-aware responses**  

---

### **🌟 Why Use TalkToDocs?**  

🚀 **Save Time** – Quickly extract key information without reading entire documents  
👌 **User-Friendly** – Simple and intuitive interface  
🤖 **Powerful AI** – Uses cutting-edge models for accurate and reliable results  

---

### **🎯 Get Started Now!**  

Upload your document below and start interacting with **TalkToDocs** today!  

---

### **⚠️ Supported File Formats**  
📂 **PDF, TXT, DOCX** – For the best experience, ensure your documents are well-structured.  
""")

if st.button("Go To Chat ->"):
    st.switch_page("pages/Talk.py")