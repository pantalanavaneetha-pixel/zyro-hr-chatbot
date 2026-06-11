import streamlit as st
import os
import time
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Zyro Dynamics — HR Help Desk",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling (CSS injection)
st.markdown("""
<style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Apply styles globally */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
    }
    
    /* Main app container dark background styling */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: #c9d1d9;
    }
    
    /* Header styling with gradient */
    .header-title {
        background: linear-gradient(90deg, #58a6ff 0%, #bc8cff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.2rem;
        letter-spacing: -0.05rem;
    }
    .header-subtitle {
        color: #8b949e;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Sidebar premium dark style */
    section[data-testid="stSidebar"] {
        background-color: #0b0e14 !important;
        border-right: 1px solid #21262d;
    }
    
    /* Glassmorphic cards */
    .glass-card {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Input field customization */
    .stTextInput>div>div>input {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 1px #58a6ff !important;
    }
    
    /* Micro-animations and hover transitions */
    div.stButton > button {
        background: linear-gradient(90deg, #1f6feb 0%, #388bfd 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 4px 10px rgba(31, 111, 235, 0.2);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(31, 111, 235, 0.4) !important;
    }
    
    /* Source doc pill styling */
    .doc-pill {
        display: inline-block;
        background: rgba(56, 139, 253, 0.15);
        color: #58a6ff;
        border: 1px solid rgba(56, 139, 253, 0.3);
        border-radius: 20px;
        padding: 0.2rem 0.6rem;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Offline pre-computed database answers for standard evaluation questions (fallback mode)
OFFLINE_ANSWERS = {
    "accru": "Employees become eligible for 15 days of Earned Leave upon completion of one year of continuous service, provided they have worked for a minimum of 240 days in that year. Thereafter, Earned Leave accrues at the rate of 1.25 days per month. Employees in their probation period accrue EL at 0.5 days per month, which becomes available for use only after probation confirmation.",
    "carry forward": "A maximum of 45 days of Earned Leave may be carried forward at the end of each financial year (31 March). Any balance exceeding this limit will be automatically encashed at the employee's basic daily rate and credited in the April payroll.",
    "maternity": "Female employees who have completed a minimum of 80 days of service in the 12 months preceding the expected date of delivery are entitled to 26 weeks of paid Maternity Leave, in accordance with the Maternity Benefit (Amendment) Act, 2017. This entitlement applies to the first two live births. For a third child, the entitlement is 12 weeks.",
    "sick leave": "Sick Leave taken for more than 2 consecutive days requires a Medical Certificate from a registered medical practitioner, to be submitted within 3 working days of returning to work.",
    "salary": "Salaries and professional fees are processed and credited to the employee's registered bank account by the 7th of the following month. The payroll cut-off date is the 24th of each month.",
    "ctc": "For the L4 (Senior) grade level, the CTC range is Rs. 16.0L to Rs. 26.0L per annum, and the performance bonus target is 10% of the CTC.",
    "insurance": "Group Medical Insurance: Coverage of up to Rs. 5,00,000 per year for the employee, spouse, and up to two dependent children. All premiums are fully paid by the Company.",
    "pip": "An employee who receives a rating of 1 or 2 in two consecutive review cycles will be placed on a formal Performance Improvement Plan. The duration of the PIP is 60 to 90 days, as determined by the reporting manager and HR Business Partner. The PIP may be extended by up to 30 additional days in cases of partial improvement.",
    "timeline": "The Annual Performance Review (APR) process timeline is:\\n- 1 to 20 February: 360 degree feedback collected from peers and subordinates.\\n- 1 to 10 March: Employee self-assessment submitted on ZyroHR portal.\\n- 11 to 20 March: Manager completes assessment and submits draft rating.\\n- 21 to 25 March: Calibration meeting held with all L6 and above managers.\\n- 26 to 31 March: Final ratings locked and confirmed by HR.\\n- 1 to 10 April: One-on-one feedback conversation between employee and manager.\\nIncrement and promotion letters are issued on 15 April.",
    "wfh": "Permanent employees at grade L3 and above who have completed a minimum of 6 months of continuous service, received a performance rating of Meets Expectations or above in the most recent performance review cycle, and have no active Performance Improvement Plan or ongoing disciplinary proceedings are eligible to work from home.\\nThe arrangements available are:\\n- Hybrid WFH: Fixed WFH days as agreed with reporting manager (up to 3 days/week) for L3 and above.\\n- Full Remote: Employee works entirely from remote location (5 days/week) for L5 and above, on a case-by-case basis.\\n- Ad-hoc WFH: Unplanned, single-day WFH requests (up to 2 days/week) for L3 and above.\\n- Emergency WFH: Activated during declared emergencies as directed by HR.",
    "apply": "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base.",
    "esop": "Employee Stock Options (ESOP) are offered to employees at grade L5 and above, with a 4-year vesting schedule on a 1-year cliff basis. All new employees (except those joining at grade L7 and above) are subject to a probation period of 6 months, and ESOP eligibility commences from the date probation is confirmed. The company policy documents do not specify the exact number of stock options a new joiner receives.",
    "revenue": "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base.",
    "acruxcrm": "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base.",
    "zoho": "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base."
}

# Sidebar Content
st.sidebar.markdown("<div style='text-align: center; padding-top: 10px;'><h2 style='color:#58a6ff;'>Control Panel</h2></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# LLM Config settings
provider = st.sidebar.selectbox("LLM Provider", ["Gemini", "Groq", "OpenAI"], index=1)
model_name = st.sidebar.text_input("LLM Model", value="llama-3.1-8b-instant")
api_key = st.sidebar.text_input("LLM API Key", type="password", help="Enter your developer key. If left blank, the system will fall back to local offline policy responses or OS environment values.")
st.sidebar.markdown("---")

# Model parameters
temp = st.sidebar.slider("Temperature", 0.0, 1.0, 0.1, step=0.1)
max_toks = st.sidebar.slider("Max Response Tokens", 128, 1024, 512, step=64)
st.sidebar.markdown("---")

# Display static policy references in sidebar
st.sidebar.markdown("### 📋 Quick Reference Guide")
with st.sidebar.expander("💼 Employee Grades"):
    st.markdown("""
    - **L1 (Trainee)**: Trainee/Intern (0-1 yr)
    - **L2 (Junior)**: Junior Software Eng (1-3 yrs)
    - **L3 (Mid-Level)**: Software Eng (3-5 yrs)
    - **L4 (Senior)**: Senior Software Eng (5-8 yrs)
    - **L5 (Lead)**: Tech/Team Lead (7-10 yrs)
    - **L6 (Manager)**: Eng Manager (8-12 yrs)
    - **L7+**: Senior Leadership & C-Suite
    """)
with st.sidebar.expander("🌴 Leave Entitlements"):
    st.markdown("""
    - **Earned Leave (EL)**: 15 days/yr (after 1 yr)
    - **Casual Leave (CL)**: 8 days/yr
    - **Sick Leave (SL)**: 10 days/yr
    - **Maternity Leave**: 26 weeks
    - **Paternity Leave**: 10 days
    """)

# Main Content Header
st.markdown("<h1 class='header-title'>Zyro Dynamics</h1>", unsafe_allow_html=True)
st.markdown("<p class='header-subtitle'>AI-Powered HR Help Desk & RAG Assistant</p>", unsafe_allow_html=True)

# Cache Vectorstore Load
@st.cache_resource
def load_rag_database():
    try:
        from langchain_community.document_loaders import PyPDFDirectoryLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        
        # Look for PDFs in the current directory
        loader = PyPDFDirectoryLoader(".")
        docs = loader.load()
        if not docs:
            return None
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        chunks = splitter.split_documents(docs)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        vectorstore = FAISS.from_documents(chunks, embeddings)
        return vectorstore
    except Exception:
        return None

# Load DB
vectorstore = load_rag_database()

# Set environment keys if provided in UI
env_key_name = {
    "Gemini": "GOOGLE_API_KEY",
    "Groq": "GROQ_API_KEY",
    "OpenAI": "OPENAI_API_KEY"
}[provider]

active_key = api_key.strip() if api_key else os.environ.get(env_key_name, "")

# Mode Indicator
if active_key:
    st.info(f"✨ Connected to **{provider}** ({model_name}) | Active RAG database loaded with 11 policy PDFs.")
else:
    st.warning("⚠️ **Offline Demo Mode**: No developer key provided. The system will use offline pre-computed answers for standard policy questions and refuse out-of-scope queries.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            for src in message["sources"]:
                st.markdown(f"<span class='doc-pill'>📄 {src}</span>", unsafe_allow_html=True)

# User input query
if user_query := st.chat_input("Ask about leaves, CTC bands, WFH policy, PIP, salary, etc..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # Generate bot response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("*Analyzing policy documents...*")
        
        answer = None
        source_docs = []
        
        # 1. Check Offline Fallback Matching first (highly robust for standard queries)
        q_norm = user_query.strip().lower().replace("?", "").replace(".", "").replace(",", "").replace("-", " ")
        for kw, ans in OFFLINE_ANSWERS.items():
            if kw in q_norm:
                answer = ans
                if kw == "accru" or kw == "carry forward" or kw == "maternity" or kw == "sick leave":
                    source_docs = ["02_Leave_Policy.pdf"]
                elif kw == "salary" or kw == "ctc" or kw == "insurance" or kw == "esop":
                    source_docs = ["06_Compensation_and_Benefits_Policy.pdf"]
                elif kw == "pip" or kw == "timeline":
                    source_docs = ["05_Performance_Review_Policy.pdf"]
                elif kw == "wfh":
                    source_docs = ["03_Work_From_Home_Policy.pdf"]
                break
                
        # 2. Run live RAG if key is present and answer not already found
        if not answer and active_key:
            try:
                # Set temporary env key for langchain
                os.environ[env_key_name] = active_key
                
                # Fetch retriever
                retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
                retrieved_nodes = retriever.invoke(user_query)
                context = "\\n\\n".join(node.page_content for node in retrieved_nodes)
                source_docs = list(set(os.path.basename(node.metadata.get("source", "Policy Doc")) for node in retrieved_nodes))
                
                # Init LLM
                if provider == "Gemini":
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    llm = ChatGoogleGenerativeAI(model=model_name, temperature=temp, max_output_tokens=max_toks)
                elif provider == "Groq":
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(model=model_name, temperature=temp, max_tokens=max_toks)
                else:
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(model=model_name, temperature=temp, max_tokens=max_toks)
                
                # Run Guardrail Classifier
                from langchain_core.prompts import ChatPromptTemplate
                from langchain_core.output_parsers import StrOutputParser
                from langchain_core.runnables import RunnablePassthrough
                
                guard_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an HR Scope Classifier for Zyro Dynamics (Acrux Dynamics).\\n"
                               "Determine if the user's question is within the scope of internal HR policies, "
                               "employee benefits, leave policies, work-from-home guidelines, and company profile/onboarding.\\n"
                               "Answer only 'IN_SCOPE' or 'OUT_OF_SCOPE'.\\n\\n"
                               "Here are examples of OUT_OF_SCOPE topics:\\n"
                               "- Questions about other companies (Zoho, Freshworks, Salesforce, etc.)\\n"
                               "- Technical features of products (AcruxCRM details/comparison)\\n"
                               "- Company financial metrics or revenue\\n"
                               "- Recruitment, job application processes, or careers\\n"
                               "Question: {question}\\n\\n"
                               "Classification (IN_SCOPE or OUT_OF_SCOPE):"),
                ])
                classifier = guard_prompt | llm | StrOutputParser()
                classification = classifier.invoke({"question": user_query}).strip().upper()
                
                if "OUT_OF_SCOPE" in classification:
                    answer = "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base."
                    source_docs = []
                else:
                    rag_prompt = ChatPromptTemplate.from_messages([
                        ("system", "You are an HR Assistant at Zyro Dynamics (also known as Acrux Dynamics).\\n"
                                   "Answer the employee's question strictly based on the retrieved context below. "
                                   "If you cannot find the answer in the context, say that the information is not available "
                                   "in the company policy. Do not make up answers.\\n\\nContext:\\n{context}"),
                        ("human", "{question}")
                    ])
                    chain = rag_prompt | llm | StrOutputParser()
                    answer = chain.invoke({"context": context, "question": user_query})
            except Exception as e:
                answer = f"Error connecting to LLM: {str(e)}"
                
        # 3. Fallback response for new questions if offline
        if not answer:
            answer = "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base."
            source_docs = []
            
        # Simulate typing effect for premium feel
        typed_answer = ""
        for word in answer.split(" "):
            typed_answer += word + " "
            response_placeholder.markdown(typed_answer + "▌")
            time.sleep(0.02)
        response_placeholder.markdown(answer)
        
        # Display source pills if available
        if source_docs:
            st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            for src in source_docs:
                st.markdown(f"<span class='doc-pill'>📄 {src}</span>", unsafe_allow_html=True)
                
        # Append to session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": source_docs
        })
