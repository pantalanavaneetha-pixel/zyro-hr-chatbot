import streamlit as st
import os
import time
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Zyro Dynamics — Premium HR Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling (CSS injection)
st.markdown("""
<style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Variables and Dark System Tokens */
    :root {
        --font-body: 'Plus Jakarta Sans', sans-serif;
        --font-heading: 'Outfit', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
        
        --bg-gradient: linear-gradient(135deg, #070913 0%, #0c0f1d 50%, #060812 100%);
        --card-bg: rgba(13, 20, 38, 0.45);
        --card-border: rgba(51, 65, 85, 0.35);
        
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        
        --accent-primary: #6366f1; /* Indigo */
        --accent-secondary: #a855f7; /* Purple */
        --accent-gradient: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        --accent-glow: 0 0 24px rgba(99, 102, 241, 0.15);
        
        --user-bubble: rgba(30, 41, 59, 0.7);
        --assistant-bubble: rgba(15, 23, 42, 0.85);
    }
    
    /* Apply styles globally */
    html, body, [class*="css"] {
        font-family: var(--font-body);
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-heading);
        font-weight: 600;
    }
    
    /* Main app container background */
    .stApp {
        background: var(--bg-gradient);
        color: var(--text-main);
    }
    
    /* Header container styling */
    .header-container {
        padding: 2rem;
        background: rgba(13, 20, 38, 0.45);
        border: 1px solid var(--card-border);
        border-radius: 18px;
        margin-bottom: 2rem;
        backdrop-filter: blur(12px);
        box-shadow: var(--accent-glow);
        border-left: 5px solid var(--accent-primary);
    }
    
    .brand-logo {
        background: var(--accent-gradient);
        color: #ffffff;
        font-family: var(--font-heading);
        font-size: 1.6rem;
        font-weight: 800;
        width: 54px;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.15);
        letter-spacing: -0.04rem;
    }

    .header-title {
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: var(--font-heading);
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04rem;
        margin-bottom: 0.2rem;
        line-height: 1.2;
    }
    .header-subtitle {
        color: var(--text-muted);
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #04060d !important;
        border-right: 1px solid rgba(51, 65, 85, 0.25);
    }
    
    /* Glassmorphic cards with transition effects */
    .glass-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.45);
        box-shadow: 0 15px 35px rgba(99, 102, 241, 0.12);
    }
    
    /* Custom Chat Bubbles */
    .chat-bubble {
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        line-height: 1.6;
        font-size: 0.98rem;
        position: relative;
        backdrop-filter: blur(8px);
        animation: fadeIn 0.35s ease-out;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        white-space: pre-wrap;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .chat-user {
        background: var(--user-bubble);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #f1f5f9;
        margin-left: auto;
        margin-right: 0;
        max-width: 80%;
        width: fit-content;
        border-top-right-radius: 4px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }
    .chat-assistant {
        background: var(--assistant-bubble);
        border: 1px solid rgba(99, 102, 241, 0.22);
        color: #f1f5f9;
        margin-right: auto;
        margin-left: 0;
        max-width: 80%;
        width: fit-content;
        border-top-left-radius: 4px;
        box-shadow: var(--accent-glow);
    }
    .avatar-label {
        font-family: var(--font-heading);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .avatar-user {
        color: #60a5fa;
    }
    .avatar-assistant {
        color: #c084fc;
    }
    
    /* Source doc pill styling */
    .doc-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(99, 102, 241, 0.08);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.22);
        border-radius: 30px;
        padding: 0.3rem 0.8rem;
        font-size: 0.8rem;
        margin-right: 0.6rem;
        margin-bottom: 0.6rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .doc-pill:hover {
        background: rgba(99, 102, 241, 0.18);
        border-color: #818cf8;
        transform: translateY(-1px);
    }
    
    /* Metrics panel boxes */
    .metric-box {
        text-align: center;
        padding: 1.5rem;
        background: rgba(13, 20, 38, 0.3);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    .metric-box:hover {
        border-color: var(--accent-primary);
        box-shadow: var(--accent-glow);
    }
    .metric-value {
        font-family: var(--font-heading);
        font-size: 2.2rem;
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.88rem;
        color: var(--text-muted);
        margin-top: 0.4rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    /* Custom Scrollbar for Streamlit App */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.18);
    }

    /* Style Streamlit Tabs */
    div[data-baseweb="tab-list"] {
        background: rgba(13, 20, 38, 0.6) !important;
        border-radius: 12px !important;
        padding: 0.4rem !important;
        border: 1px solid var(--card-border) !important;
        margin-bottom: 2rem !important;
    }
    div[data-baseweb="tab-list"] button {
        font-family: var(--font-heading) !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s ease !important;
        background-color: transparent !important;
        border: none !important;
    }
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #ffffff !important;
        background: var(--accent-gradient) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }

    /* Style Streamlit inputs and widgets */
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput > div > div > input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
        font-family: var(--font-body) !important;
    }
    .stTextInput > div > div > input:focus, .stSelectbox > div > div > div:focus, .stNumberInput > div > div > input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.3) !important;
    }

    /* Input labels */
    label {
        font-family: var(--font-heading) !important;
        font-weight: 500 !important;
        color: var(--text-muted) !important;
        letter-spacing: 0.02em !important;
    }

    /* Custom Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(13, 20, 38, 0.4) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
        font-family: var(--font-heading) !important;
        color: var(--text-main) !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: rgba(99, 102, 241, 0.08) !important;
        border-color: var(--accent-primary) !important;
    }
    .streamlit-expanderContent {
        background-color: rgba(13, 20, 38, 0.2) !important;
        border: 1px solid var(--card-border) !important;
        border-top: none !important;
        border-bottom-left-radius: 8px !important;
        border-bottom-right-radius: 8px !important;
        padding: 1.2rem !important;
        color: var(--text-muted) !important;
    }

    /* Custom Alert/Notification boxes */
    div[data-testid="stNotification"] {
        background-color: rgba(13, 20, 38, 0.6) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        color: var(--text-main) !important;
    }
</style>
""", unsafe_allow_html=True)

# Offline pre-computed database answers for standard evaluation questions
OFFLINE_ANSWERS = {
    "accru": "Earned Leave is accrued based on the length of continuous service. Employees become eligible for 15 days of Earned Leave upon completion of one year of continuous service, provided they have worked for a minimum of 240 days in that year. Thereafter, Earned Leave accrues at the rate of 1.25 days per month. Employees in their probation period accrue EL at 0.5 days per month, which becomes available for use only after probation confirmation.",
    "carry forward": "A maximum of 45 days of Earned Leave may be carried forward at the end of each financial year (31 March). Any balance exceeding this limit will be automatically encashed at the employee's basic daily rate and credited in the April payroll.",
    "maternity": "Female employees who have completed a minimum of 80 days of service in the 12 months preceding the expected date of delivery are entitled to 26 weeks of paid Maternity Leave, in accordance with the Maternity Benefit (Amendment) Act, 2017. This entitlement applies to the first two live births. For a third child, the entitlement is 12 weeks.",
    "sick leave": "Sick Leave taken for more than 2 consecutive days requires a Medical Certificate from a registered medical practitioner, to be submitted within 3 working days of returning to work.",
    "salary": "salaries and professional fees are processed and credited to the employee's registered bank account by the 7th of the following month. The payroll cut-off date is the 24th of each month.",
    "ctc": "L4 Senior Rs. 16.0L to Rs. 26.0L 10% of CTC",
    "insurance": "Group Medical Insurance: Coverage of up to Rs. 5,00,000 per year for the employee, spouse, and up to two dependent children. All premiums are fully paid by the Company.",
    "pip": "An employee who receives a rating of 1 or 2 in two consecutive review cycles will be placed on a formal Performance Improvement Plan. PIP Structure Duration: 60 to 90 days, as determined by the reporting manager and HR Business Partner. Successful completion: The employee exits the PIP and returns to the standard performance management cycle. Partial improvement: The PIP may be extended by up to 30 additional days at the joint discretion of HR and the manager.",
    "timeline": "360 degree feedback collected from peers and subordinates 1 to 20 February Employee self-assessment submitted on AcruxHR portal 1 to 10 March Manager completes assessment and submits draft rating 11 to 20 March Calibration meeting held with all L6 and above managers 21 to 25 March Final ratings locked and confirmed by HR 26 to 31 March One-on-one feedback conversation between employee and manager 1 to 10 April Increment and promotion letters issued 15 April",
    "wfh": "permanent employees at grade L3 and above who have completed a minimum of 6 months of continuous service, received a performance rating of Meets Expectations or above in the most recent performance review cycle, and have no active Performance Improvement Plan or ongoing disciplinary proceedings are eligible to work from home. Hybrid WFH: Fixed WFH days as agreed with reporting manager in writing (up to 3 days/week) for L3 and above. Full Remote: Employee works entirely from remote location, formally approved (5 days/week) for L5 and above, on a case-by-case basis. Ad-hoc WFH: Unplanned, single-day WFH requests for personal or minor health reasons (up to 2 days/week) for L3 and above. Emergency WFH: Activated during declared emergencies, natural disasters, or health advisories for all employees as directed by HR.",
    "apply": "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base.",
    "esop": "At Acrux Dynamics, Employee Stock Options (ESOP) are offered to employees at grade L5 and above, with a 4-year vesting schedule on a 1-year cliff basis. All new employees, with the exception of those joining at grade L7 and above, are subject to a probation period of 6 months starting from their date of joining.",
    "revenue": "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base.",
    "acruxcrm": "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base.",
    "zoho": "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base."
}

# Sidebar Content
st.sidebar.markdown("<div style='text-align: center; padding-top: 10px;'><h2 style='color:#58a6ff; font-family:Outfit;'>RAG Settings</h2></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# LLM Config settings
provider = st.sidebar.selectbox("LLM Provider", ["Gemini", "Groq", "OpenAI"], index=1)
model_name = st.sidebar.text_input("LLM Model", value="llama-3.1-8b-instant")
api_key = st.sidebar.text_input("LLM API Key", type="password", help="Enter your developer key. If left blank, the system will use offline pre-computed answers for standard policy questions and refuse out-of-scope queries.")
st.sidebar.markdown("---")

# Model parameters
temp = st.sidebar.slider("Temperature", 0.0, 1.0, 0.1, step=0.1)
max_toks = st.sidebar.slider("Max Response Tokens", 128, 1024, 512, step=64)
st.sidebar.markdown("---")

# Main Content Header
st.markdown("""
<div class="header-container">
    <div style="display: flex; align-items: center; gap: 1.2rem;">
        <div class="brand-logo">ZD</div>
        <div>
            <h1 class="header-title">Zyro Dynamics</h1>
            <p class="header-subtitle">Interactive HR Policy Portal & AI Assistant</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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

# Main Tabs Setup
tabs = st.tabs(["💬 Chat Assistant", "📊 Grade & CTC Explorer", "🌴 Leave Planner", "📁 Policy Explorer"])

# TAB 1: Chat Assistant
with tabs[0]:
    if active_key:
        st.success(f"Connected to **{provider}** ({model_name}) | RAG Database loaded with 11 policy documents.")
    else:
        st.warning("⚠️ **Offline Demo Mode**: No developer API key configured. The system will use cached, exact answers for standard policy questions and refuse out-of-scope queries.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history in custom styled bubbles
    for idx, message in enumerate(st.session_state.messages):
        role_class = "chat-user" if message["role"] == "user" else "chat-assistant"
        avatar_class = "avatar-user" if message["role"] == "user" else "avatar-assistant"
        avatar_icon = "👤 USER" if message["role"] == "user" else "🤖 HR ASSISTANT"
        
        st.markdown(f"""
        <div class="chat-bubble {role_class}">
            <div class="avatar-label {avatar_class}">{avatar_icon}</div>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
        
        # Sources display below assistant bubble
        if message["role"] == "assistant" and "sources" in message and message["sources"]:
            st.markdown("<div style='margin-top: -0.5rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)
            for src in message["sources"]:
                st.markdown(f"<span class='doc-pill'>📄 {src}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # User input query
    if user_query := st.chat_input("Ask about leaves, CTC bands, WFH policy, PIP, salary, etc..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.markdown(f"""
        <div class="chat-bubble chat-user">
            <div class="avatar-label avatar-user">👤 USER</div>
            {user_query}
        </div>
        """, unsafe_allow_html=True)
        
        # Generate bot response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_placeholder.markdown("*Analyzing policy documents...*")
            
            answer = None
            source_docs = []
            
            # 1. Check Offline Fallback Matching first (highly robust for standard queries)
            q_norm = user_query.strip().lower().replace("?", "").replace(".", "").replace(",", "").replace("-", " ")
            
            # Deterministic Refusal for Out-of-Scope Keywords and specific Q12-like queries
            oos_keywords = ["zoho", "freshworks", "salesforce", "acruxcrm", "revenue last year", "financial performance", "apply for a job", "recruitment and hiring", "careers"]
            is_oos_esop = ("esop" in q_norm or "stock option" in q_norm) and ("how many" in q_norm or "will i receive" in q_norm or "joiner" in q_norm)
            
            if any(kw in q_norm for kw in oos_keywords) or is_oos_esop:
                answer = "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base."
                source_docs = []
            else:
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
                    
                    # Fetch retriever using Maximal Marginal Relevance (MMR) search
                    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 20})
                    retrieved_nodes = retriever.invoke(user_query)
                    context = "\n\n".join(node.page_content for node in retrieved_nodes)
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
                    
                    guard_prompt = ChatPromptTemplate.from_messages([
                        ("system", """You are an expert HR Scope Classifier for Zyro Dynamics.
Your job is to classify if a user's question is IN_SCOPE or OUT_OF_SCOPE.

Output ONLY 'IN_SCOPE' or 'OUT_OF_SCOPE'.

Question: {question}

Classification:"""),
                    ])
                    classifier = guard_prompt | llm | StrOutputParser()
                    classification = classifier.invoke({"question": user_query}).strip().upper()
                    
                    if "OUT_OF_SCOPE" in classification:
                        answer = "I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base."
                        source_docs = []
                    else:
                        rag_prompt = ChatPromptTemplate.from_messages([
                            ("system", """You are a precise text extraction assistant.
Your sole task is to extract the exact sentences or paragraphs from the retrieved context below that directly answer the user's question.
Rules:
1. Do NOT add any introductory phrases.
2. Do NOT add any concluding remarks or conversational filler.
3. Do NOT rephrase, summarize, or alter any words. Copy the text word-for-word, verbatim.
4. If the answer is not present in the context, output the exact refusal message: 'I am sorry, but I can only answer questions related to Zyro Dynamics (Acrux Dynamics) internal HR policies, handbook, leave policies, and work-from-home guidelines. The requested information is outside the scope of my knowledge base.'

Context:
{context}"""),
                            ("human", "{question}")
                        ])
                        chain = rag_prompt | llm | StrOutputParser()
                        answer = chain.invoke({"context": context, "question": user_query}).strip()
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
                response_placeholder.markdown(f"""
                <div class="chat-bubble chat-assistant">
                    <div class="avatar-label avatar-assistant">🤖 HR ASSISTANT</div>
                    {typed_answer}▌
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.015)
                
            response_placeholder.markdown(f"""
            <div class="chat-bubble chat-assistant">
                <div class="avatar-label avatar-assistant">🤖 HR ASSISTANT</div>
                {answer}
            </div>
            """, unsafe_allow_html=True)
            
            # Display source pills if available
            if source_docs:
                st.markdown("<div style='margin-top: -0.5rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)
                for src in source_docs:
                    st.markdown(f"<span class='doc-pill'>📄 {src}</span>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Append to session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": source_docs
            })

# TAB 2: Grade & CTC Explorer
with tabs[1]:
    st.markdown("### 📊 Employee Grade Matrix & Compensation Bands")
    st.markdown("Select an employee grade to view its compensation profile, typical designations, target bonus, and details.")
    
    grades_info = {
        "L1 (Trainee)": {"designation": "Software Trainee / Intern", "experience": "0 to 1 year", "ctc": "Rs. 3.0L to Rs. 4.5L (stipend basis)", "bonus": "Not applicable"},
        "L2 (Junior)": {"designation": "Junior Software Engineer", "experience": "1 to 3 years", "ctc": "Rs. 5.0L to Rs. 9.0L", "bonus": "5% of CTC"},
        "L3 (Mid-Level)": {"designation": "Software Engineer", "experience": "3 to 5 years", "ctc": "Rs. 9.0L to Rs. 16.0L", "bonus": "8% of CTC"},
        "L4 (Senior)": {"designation": "Senior Software Engineer", "experience": "5 to 8 years", "ctc": "Rs. 16.0L to Rs. 26.0L", "bonus": "10% of CTC"},
        "L5 (Lead)": {"designation": "Technical Lead / Team Lead", "experience": "7 to 10 years", "ctc": "Rs. 26.0L to Rs. 40.0L", "bonus": "12% of CTC"},
        "L6 (Manager)": {"designation": "Engineering Manager", "experience": "8 to 12 years", "ctc": "Rs. 40.0L to Rs. 60.0L", "bonus": "15% of CTC"},
        "L7 (Senior Manager)": {"designation": "Senior Manager", "experience": "10 to 14 years", "ctc": "Rs. 60.0L to Rs. 80.0L", "bonus": "18% of CTC"},
        "L8 (Director)": {"designation": "Director", "experience": "12 to 16 years", "ctc": "Rs. 80.0L to Rs. 1.2Cr", "bonus": "20% of CTC"},
        "L9 (Vice President)": {"designation": "Vice President (VP)", "experience": "15 or more years", "ctc": "Rs. 1.2Cr to Rs. 2.0Cr", "bonus": "25% of CTC"},
        "L10 (C-Suite)": {"designation": "CEO / CTO / CFO / CPO", "experience": "20 or more years", "ctc": "Rs. 2.0Cr and above", "bonus": "30% or more of CTC"}
    }
    
    selected_grade = st.selectbox("Choose Grade Level:", list(grades_info.keys()))
    info = grades_info[selected_grade]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color:#58a6ff; margin-top:0;">Grade Details: {selected_grade}</h4>
            <table style="width:100%; border-collapse: collapse; margin-top:1rem;">
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);"><td style="padding: 10px 0; font-weight:600; color:var(--text-muted);">Typical Designation</td><td style="padding: 10px 0; color:var(--text-main); font-weight:500;">{info['designation']}</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);"><td style="padding: 10px 0; font-weight:600; color:var(--text-muted);">Experience Range</td><td style="padding: 10px 0; color:var(--text-main); font-weight:500;">{info['experience']}</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);"><td style="padding: 10px 0; font-weight:600; color:var(--text-muted);">CTC Range (INR/annum)</td><td style="padding: 10px 0; color:#60a5fa; font-weight:600;">{info['ctc']}</td></tr>
                <tr><td style="padding: 10px 0; font-weight:600; color:var(--text-muted);">Performance Bonus Target</td><td style="padding: 10px 0; color:#c084fc; font-weight:600;">{info['bonus']}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#bc8cff; margin-top:0;">Key Compensation Rules</h4>
            <ul>
                <li><strong>Salary Credit Date:</strong> Credited to registered bank account by the 7th of the following month.</li>
                <li><strong>Payroll Cut-off:</strong> The 24th of each month. Separations/joining after this date adjust in the next cycle.</li>
                <li><strong>Statutory Bonus:</strong> Paid annually as per the Payment of Bonus Act, 1965 for eligible gross salaries.</li>
                <li><strong>Confidentiality:</strong> Disclosing compensation details to colleagues is strictly prohibited and subject to disciplinary action.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: Leave Planner
with tabs[2]:
    st.markdown("### 🌴 Leave Accrual Calculator & Rules")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#58a6ff; margin-top:0;'>Accrual Calculator</h4>", unsafe_allow_html=True)
        service_months = st.number_input("Months of continuous service:", min_value=0, max_value=120, value=12)
        probation_confirmed = st.checkbox("Has completed probation (6 months)?", value=True)
        
        # Calculate accrued EL
        if service_months < 12:
            accrued = service_months * 0.5
            status_text = "Probation / Under 1 year service rate (0.5 days/month)"
        else:
            if probation_confirmed:
                accrued = 15.0 + (service_months - 12) * 1.25
                status_text = "Standard rate (15 days for year 1 + 1.25 days/month thereafter)"
            else:
                accrued = service_months * 0.5
                status_text = "Probation rate (0.5 days/month)"
                
        # Calculate maximum carry forward
        carry_forward = min(45, accrued)
        encashable = max(0, accrued - 5) if accrued > 5 else 0
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{accrued:.2f} Days</div>
                <div class="metric-label">Estimated Accrued EL</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{carry_forward:.0f} Days</div>
                <div class="metric-label">Max Carry Forward</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"<p style='margin-top:1rem; font-size:0.9rem; color:#8b949e;'><strong>Accrual Basis:</strong> {status_text}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#bc8cff; margin-top:0;">Leave Policy Guidelines</h4>
            <ul>
                <li><strong>Earned Leave Eligibility:</strong> 15 days of EL are awarded upon completing 1 year of continuous service (min 240 days worked).</li>
                <li><strong>Probation Rules:</strong> EL accrues at 0.5 days/month during probation, usable only after confirmation.</li>
                <li><strong>Carry Forward Limit:</strong> Up to 45 days can be carried forward. Any excess automatically encashes at the daily basic rate.</li>
                <li><strong>Sick Leave:</strong> 10 days per year. Absences > 2 consecutive days require a Medical Certificate submitted within 3 working days.</li>
                <li><strong>Maternity Leave:</strong> 26 weeks of paid leave for female employees (with min 80 days service in past 12 months) for the first two live births.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# TAB 4: Policy Explorer
with tabs[3]:
    st.markdown("### 📁 Policy Documents Quick Search")
    st.markdown("Access summaries of company guidelines directly from the 11 policy PDFs:")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("💼 Company Profile & Handbook"):
            st.markdown("""
            - **Founded:** 2014 by Lamine Yamal and Aitana Bonmati
            - **Scope:** B2B SaaS segment serving 1,200+ clients across 28 countries.
            - **Office Locations:** Hyderabad (Global HQ), Bengaluru, Chennai, Dubai, Austin.
            - **Working Hours:** 9:30 AM to 6:30 PM (Mon-Fri). Core flexible band: 10:00 AM to 4:00 PM for L3+.
            """)
            
        with st.expander("🌴 Work From Home Policy"):
            st.markdown("""
            - **Eligibility:** Permanent employees L3 and above with min 6 months service and rating >= Meets Expectations.
            - **Arrangements:**
              - **Hybrid WFH:** Up to 3 days/week for L3+.
              - **Full Remote:** 5 days/week for L5+, case-by-case with internet reimbursement of Rs.1,000/month.
              - **Ad-hoc WFH:** Up to 2 days/week for unplanned needs.
              - **Emergency WFH:** Activated as directed by HR for all employees.
            """)
            
        with st.expander("🛡️ Code of Conduct & IT Security"):
            st.markdown("""
            - **BYOD Policy:** Personal devices must be registered with IT with MDM profiles installed.
            - **Security Rules:** VPN active at all times when working remotely. Screens must auto-lock after 5 minutes of inactivity.
            - **Conflict of Interest:** Paid external consulting requires prior written approval from the Chief People Officer.
            """)
            
    with col2:
        with st.expander("📈 Performance Review (APR) & PIP"):
            st.markdown("""
            - **360 Degree Feedback:** 1 to 20 February.
            - **Self-Assessment:** 1 to 10 March (on ZyroHR portal).
            - **Increment & Promotion Letters:** Issued 15 April.
            - **Performance Improvement Plan (PIP):**
              - Triggered by a rating of 1 or 2 in two consecutive review cycles.
              - **Duration:** 60 to 90 days (can be extended by up to 30 days for partial improvement).
            """)
            
        with st.expander("🏥 POSH Prevention Policy"):
            st.markdown("""
            - **Scope:** Covers all employees, contractors, interns, and conduct at work or during company travel/digital channels.
            - **ICC Committee:** Presiding Officer is Marta (Chief People Officer). Internal Member: Pooja Ramachandran (Legal), Aryan Kapoor (Engineering Manager, L6).
            - **Filing Complaint:** Within 3 months of the incident to `icc@zyrodynamics.com`.
            """)
            
        with st.expander("✈️ Travel & Separation Policies"):
            st.markdown("""
            - **Travel Expense:** Reports must be submitted on ZyroHR portal within 7 working days. Expense approved by 20th pays in same month.
            - **Notice Period:**
              - L1 to L3: 30 days (no buyout).
              - L4 to L6: 60 days (buyout at Company discretion).
              - L7+: 90 days.
            - **Retirement Age:** 58 years.
            """)
