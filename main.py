import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import docx
from PIL import Image
import time

# --- Configuration and Setup ---

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Nyay Sahayak",
    page_icon="⚖️",
    layout="wide"
)

# Configure the Generative AI model
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    st.error(f"API Configuration Error: Please ensure your GOOGLE_API_KEY is set in .env. Details: {e}")

# --- UI Internationalization (i18n) Dictionary (Unchanged) ---
translations = {
    "en": {
        "page_title": "Nyay Sahayak: Kanooni Madad, Aapke Sath",
        "sidebar_header": "Settings",
        "language_select": "Select Output Language",
        "disclaimer": "This is a prototype created for the Gen AI Exchange Hackathon. It is not a substitute for professional legal advice.",
        "uploader_label": "Upload your legal document (PDF, DOCX, PNG, JPG)",
        "button_text": "Begin Multi-Agent Analysis",
        "analysis_complete_header": "Analysis Complete",
        "tab_overview": "📊 At-a-Glance Dashboard",
        "tab_breakdown": "📖 Detailed Breakdown",
        "tab_strategic": "💡 Strategic Insights",
        "tab_cases": "🏛️ Related Cases",
        "overview_summary": "Quick Summary",
        "overview_doc_type": "Document Type",
        "overview_strength": "Case Strength (Lower is Better)",
        "overview_assessment": "Case Strength Assessment",
        "overview_reasoning": "Reasoning",
        "overview_parties": "Parties Involved",
        "overview_takeaways": "Key Takeaways for You",
        "breakdown_header": "Detailed Document Understanding",
        "breakdown_comp_summary_header": "Comprehensive Summary",
        "strategic_header_points": "Key Points for Hearing/Negotiation",
        "strategic_header_sections": "Legal Sections & Acts Mentioned",
        "cases_header": "Related Case Law & Precedents",
        "cases_disclaimer": "🚨 DISCLAIMER: This is AI-generated information for educational purposes ONLY and is not legal advice. Consult a qualified lawyer.",
        "qna_header": "💬 Ask Follow-up Questions",
        "qna_input_placeholder": "Ask a specific question about the document...",
        "lang_change_popup_text": "You have changed the language. To view the analysis in the new language, please re-run the process.",
        "rerun_button": "Translate Results",
        "point_label": "Point",
        "importance_label": "Importance",
        "case_label": "Case",
        "precedent_label": "Precedent",
        "progress_text": "Analyzing your document... Please wait."
    },
    "hi": {
        "page_title": "न्याय सहायक: कानूनी मदद, आपके साथ",
        "sidebar_header": "सेटिंग्स",
        "language_select": "आउटपुट भाषा चुनें",
        "disclaimer": "यह जेन एआई एक्सचेंज हैकथॉन के लिए बनाया गया एक प्रोटोटाइप है। यह पेशेवर कानूनी सलाह का विकल्प नहीं है।",
        "uploader_label": "अपना कानूनी दस्तावेज़ अपलोड करें (PDF, DOCX, PNG, JPG)",
        "button_text": "मल्टी-एजेंट विश्लेषण शुरू करें",
        "analysis_complete_header": "विश्लेषण पूरा हुआ",
        "tab_overview": "📊 एक नज़र में डैशबोर्ड",
        "tab_breakdown": "📖 विस्तृत विश्लेषण",
        "tab_strategic": "💡 रणनीतिक अंतर्दृष्टि",
        "tab_cases": "🏛️ संबंधित मामले",
        "overview_summary": "संक्षिप्त सारांश",
        "overview_doc_type": "दस्तावेज़ का प्रकार",
        "overview_strength": "केस की ताकत (कम बेहतर है)",
        "overview_assessment": "केस की ताकत का आकलन",
        "overview_reasoning": "तर्क",
        "overview_parties": "शामिल पक्ष",
        "overview_takeaways": "आपके लिए मुख्य बातें",
        "breakdown_header": "दस्तावेज़ की विस्तृत समझ",
        "breakdown_comp_summary_header": "विस्तृत सारांश",
        "strategic_header_points": "सुनवाई/बातचीत के लिए मुख्य बिंदु",
        "strategic_header_sections": "उल्लिखित कानूनी धाराएं और अधिनियम",
        "cases_header": "संबंधित मामले और मिसालें",
        "cases_disclaimer": "🚨 अस्वीकरण: यह केवल शैक्षिक उद्देश्यों के लिए एआई-जनित जानकारी है और कानूनी सलाह नहीं है। एक योग्य वकील से परामर्श करें।",
        "qna_header": "💬 अनुवर्ती प्रश्न पूछें",
        "qna_input_placeholder": "दस्तावेज़ के बारे में एक विशिष्ट प्रश्न पूछें...",
        "lang_change_popup_text": "आपने भाषा बदल दी है। नए भाषा में परिणाम देखने के लिए, कृपया प्रक्रिया फिर से चलाएं।",
        "rerun_button": "परिणामों का अनुवाद करें",
        "point_label": "बिंदु",
        "importance_label": "महत्व",
        "case_label": "मामला",
        "precedent_label": "मिसाल",
        "progress_text": "आपके दस्तावेज़ का विश्लेषण किया जा रहा है... कृपया प्रतीक्षा करें।"
    }
}

# --- Multi-Format Input Handling (Unchanged) ---
def get_document_content(uploaded_files):
    text = ""
    for uploaded_file in uploaded_files:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension == ".pdf":
            try:
                pdf_reader = PdfReader(uploaded_file);
                for page in pdf_reader.pages: text += page.extract_text()
            except Exception as e: st.error(f"Error reading PDF file: {e}"); return None
        elif file_extension == ".docx":
            try:
                doc = docx.Document(uploaded_file);
                for para in doc.paragraphs: text += para.text + "\n"
            except Exception as e: st.error(f"Error reading DOCX file: {e}"); return None
        elif file_extension in [".png", ".jpg", ".jpeg"]:
            try:
                image = Image.open(uploaded_file);
                vision_model = genai.GenerativeModel("gemini-1.5-flash");
                response = vision_model.generate_content(["Extract all text from this image of a legal document.", image]);
                text += response.text + "\n"
            except Exception as e: st.error(f"Error processing image file: {e}"); return None
    return text

# --- Core AI Functions (Unchanged) ---
def get_gemini_response(prompt, model_name="gemini-1.5-flash"):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        if not hasattr(response, 'text'):
            st.error(f"The model returned an empty response. This may be due to safety settings or an internal error.")
            return None
        clean_json_str = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_json_str)
    except json.JSONDecodeError:
        st.error("The AI's response was not in the expected JSON format. Please try again.")
        st.text_area("Raw AI Response for debugging:", response.text if 'response' in locals() else "No response received.")
        return None
    except Exception as e:
        st.error(f"An API error occurred with model {model_name}: {e}")
        return None

# --- THE MULTI-AGENT SYSTEM (with FINAL prompts for simple language and depth) ---

# This helper string will be used in all agents to ensure simple Hindi
HINDI_INSTRUCTION = """
**If the target language is Hindi, you MUST follow this critical instruction:**
Your user is an average person, not a legal expert. Do NOT use difficult or pure 'shuddh' Hindi words.
Use simple, conversational, everyday Hindi (often called Hinglish).
For example:
- Instead of 'न्यायालय', use 'कोर्ट'.
- Instead of 'अधिवक्ता', use 'वकील'.
- Instead of 'याचिकाकर्ता', use 'अर्जी देने वाला' or 'याचिकाकर्ता'.
- Instead of 'प्रतिवादी', use 'जिसके खिलाफ केस है' or 'प्रतिवादी'.
The goal is MAXIMUM simplicity and readability for a common person.
"""

def run_triage_agent(document_text, language="English"):
    json_structure_string = f"""{{ "document_type": "...", "parties_involved": [{{ "role": "Translate this role (e.g., 'Applicant', 'Respondent') to {language}.", "name": "..."}}], "legal_sections_mentioned": ["..."] }}"""
    prompt = f"""You are a Triage Agent. Your task is to perform a quick scan of the legal document below and extract key metadata.
    {HINDI_INSTRUCTION if language == "Hindi" else ""}
    Translate all string values in the final JSON to {language}. Output a single, valid JSON object.
    Document Text: --- {document_text[:4000]} ---
    JSON Structure: {json_structure_string}
    """
    return get_gemini_response(prompt)

def run_demystifier_agent(document_text, language="English"):
    prompt = f"""
    You are a Demystifier Agent. Your task is to provide a very detailed, simple-language breakdown of the legal document.
    {HINDI_INSTRUCTION if language == "Hindi" else ""}
    Translate all string values in the final JSON to {language}. Output a single, valid JSON object.

    Document Text: --- {document_text} ---
    JSON Structure: {{
        "quick_summary": "Provide a clear, simple, 4-5 line summary of what this paper is about and what it wants to achieve.",
        "comprehensive_summary": "Provide a very detailed, multi-paragraph summary covering all key aspects of the document. This should be exhaustive (at least 300 words). Structure it logically: 1. Start with the background of the case. 2. Detail the main arguments presented by the applicant. 3. List the key evidence or points mentioned to support the arguments. 4. State the final request or 'prayer' made to the court. Ensure all points from the original document are covered in this detailed summary.",
        "key_takeaways_for_user": ["List 3-4 of the most important, action-oriented points for the user. Make each point a detailed, multi-sentence explanation of what the user needs to know or do."],
        "detailed_understanding": [{{ "heading": "Provide a clear heading for a major section in simple language.", "explanation": "Explain this section in extremely simple, practical, and very detailed terms, using at least two paragraphs. Use analogies if helpful."}}]
    }}
    """
    return get_gemini_response(prompt)

def run_strategic_advisor_agent(document_text, language="English"):
    prompt = f"""
    You are a Strategic Advisor Agent. Based on the document, provide a detailed strategic assessment and actionable points in simple language.
    {HINDI_INSTRUCTION if language == "Hindi" else ""}
    Translate all string values in the final JSON to {language}. Output a single, valid JSON object.
    Document Text: --- {document_text} ---
    JSON Structure: {{
        "case_strength_assessment": {{ "score": "On a scale of 1-10 (1=very strong, 10=very weak), assess the strength of the case for the primary applicant.", "reasoning": "Provide a detailed, multi-sentence reasoning for your score, elaborating on the strengths and weaknesses." }},
        "key_points_for_hearing": [ {{ "point": "Identify a critical point or argument.", "importance": "Explain in detail (at least two sentences) why this point is so important and how it can be argued effectively." }} ]
    }}
    """
    return get_gemini_response(prompt)

def run_legal_scholar_agent(triage_data, language="English"):
    sections = ", ".join(triage_data.get("legal_sections_mentioned", []))
    doc_type = triage_data.get("document_type", "legal document")
    if not sections: return {"related_cases": [{"case_name": "No specific legal sections found to research.", "precedent_summary": "Please ensure the document clearly states the laws or sections it is based on."}]}
    prompt = f"""
    You are a Legal Scholar Agent. Based on an {doc_type} involving sections {sections}, find relevant landmark case laws from India.
    {HINDI_INSTRUCTION if language == "Hindi" else ""}
    Translate all string values in the final JSON to {language}. Output a single, valid JSON object.
    JSON Structure: {{ "related_cases": [{{ "case_name": "Full case name", "precedent_summary": "Explain the case's main outcome, its context, and its importance in simple, detailed, multi-sentence terms." }}] }}
    """
    return get_gemini_response(prompt)

# --- THE ORCHESTRATOR (Unchanged) ---
def run_orchestrator(document_text, language, lang_code, progress_placeholder, progress_text_key):
    st.session_state.analysis_data = {}
    progress_bar = progress_placeholder.progress(0, text=translations.get(lang_code, translations['en'])[progress_text_key])
    agents = [
        {"func": run_triage_agent, "name": "triage"},
        {"func": run_demystifier_agent, "name": "demystifier"},
        {"func": run_strategic_advisor_agent, "name": "advisor"}
    ]
    total_agents = len(agents) + 1
    for i, agent in enumerate(agents):
        results = agent["func"](document_text, language)
        progress = int(((i + 1) / total_agents) * 100)
        progress_bar.progress(progress, text=translations.get(lang_code, translations['en'])[progress_text_key])
        if not results:
            st.error(f"{agent['name'].capitalize()} Agent failed. Analysis stopped.")
            progress_placeholder.empty()
            return
        st.session_state.analysis_data[agent['name']] = results
    scholar_results = run_legal_scholar_agent(st.session_state.analysis_data['triage'], language)
    progress_bar.progress(100, text=translations.get(lang_code, translations['en'])[progress_text_key])
    if not scholar_results:
        st.error("Legal Scholar Agent failed.")
        progress_placeholder.empty()
        return
    st.session_state.analysis_data['scholar'] = scholar_results
    time.sleep(1)
    progress_placeholder.empty()
    st.session_state.analysis_done = True
    st.session_state.document_context = document_text
    st.session_state.analysis_language = lang_code

# --- STREAMLIT UI (Unchanged) ---
if "analysis_done" not in st.session_state: st.session_state.analysis_done = False
if "analysis_language" not in st.session_state: st.session_state.analysis_language = "en"
if "document_context" not in st.session_state: st.session_state.document_context = ""

lang_map = {"English": "en", "हिंदी (Hindi)": "hi"}
selected_lang_name = st.sidebar.selectbox("Select Language / भाषा चुनें", list(lang_map.keys()), key="language_selector")
lang_code = lang_map[selected_lang_name]
T = translations.get(lang_code, translations['en'])

st.title(T["page_title"])
with st.sidebar:
    st.image("https://tse4.mm.bing.net/th/id/OIP.pKYxAsdzwLdveNPRvfdFQwHaEK?rs=1&pid=ImgDetMain&o=7&rm=3",width=250)
    st.header(T["sidebar_header"])
    st.info(T["disclaimer"])

if st.session_state.analysis_done and st.session_state.analysis_language != lang_code:
    with st.container(border=True):
        st.info(T["lang_change_popup_text"])
        if st.button(T["rerun_button"], key="rerun_translation"):
            progress_placeholder = st.empty()
            run_orchestrator(st.session_state.document_context, selected_lang_name.split(" ")[0], lang_code, progress_placeholder, "progress_text")
            st.rerun()

uploaded_files = st.file_uploader(T["uploader_label"], type=["pdf", "docx", "png", "jpg", "jpeg"], accept_multiple_files=True, key="file_uploader")
progress_placeholder = st.empty()

if st.button(T["button_text"], disabled=not uploaded_files):
    st.session_state.analysis_done = False
    content = get_document_content(uploaded_files)
    if content:
        run_orchestrator(content, selected_lang_name.split(" ")[0], lang_code, progress_placeholder, "progress_text")
        st.rerun()

if st.session_state.analysis_done:
    data = st.session_state.analysis_data
    triage, demystifier, advisor, scholar = data.get('triage', {}), data.get('demystifier', {}), data.get('advisor', {}), data.get('scholar', {})
    st.header(T["analysis_complete_header"], divider='rainbow')
    tab1, tab2, tab3, tab4 = st.tabs([T["tab_overview"], T["tab_breakdown"], T["tab_strategic"], T["tab_cases"]])
    with tab1:
        st.subheader(T["overview_summary"]); st.write(demystifier.get('quick_summary'))
        st.subheader(T["overview_takeaways"]); 
        for takeaway in demystifier.get('key_takeaways_for_user', []): st.success(f"👉 {takeaway}")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(T["overview_doc_type"]); st.info(triage.get('document_type'))
            st.subheader(T["overview_parties"]); 
            for party in triage.get('parties_involved', []): st.markdown(f"- **{party.get('role')}:** {party.get('name')}")
        with col2:
            st.subheader(T["overview_assessment"])
            assessment = advisor.get('case_strength_assessment', {})
            st.metric(T["overview_strength"], f"{assessment.get('score')}/10")
            st.warning(f"**{T['overview_reasoning']}:** {assessment.get('reasoning')}")
    with tab2:
        st.subheader(T["breakdown_comp_summary_header"]); st.write(demystifier.get('comprehensive_summary'))
        st.divider()
        st.subheader(T["breakdown_header"]); 
        for item in demystifier.get('detailed_understanding', []):
            with st.expander(f"**{item.get('heading')}**"): st.write(item.get('explanation'))
    with tab3:
        st.subheader(T["strategic_header_points"])
        for item in advisor.get('key_points_for_hearing', []):
            if isinstance(item, dict):
                container = st.container(border=True)
                container.markdown(f"**{T['point_label']}:** {item.get('point')}")
                container.info(f"**{T['importance_label']}:** {item.get('importance')}")
        st.subheader(T["strategic_header_sections"]); st.code(", ".join(triage.get('legal_sections_mentioned', ['None'])))
    with tab4:
        st.subheader(T["cases_header"]); st.error(T["cases_disclaimer"])
        for case in scholar.get('related_cases', []):
            container = st.container(border=True)
            container.markdown(f"**{T['case_label']}:** {case.get('case_name')}")
            container.info(f"**{T['precedent_label']}:** {case.get('precedent_summary')}")
    st.header(T["qna_header"], divider='rainbow')
    if "messages" not in st.session_state: st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])
    if prompt := st.chat_input(T["qna_input_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                qna_prompt = f"Context:\n{st.session_state.document_context}\n\nQuestion: {prompt}\n\nAnswer the question based ONLY on the context. {HINDI_INSTRUCTION if language == 'Hindi' else 'Use extremely simple language.'}"
                model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(qna_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})