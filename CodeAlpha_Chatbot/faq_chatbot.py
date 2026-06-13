import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. SETUP THE FAQ DATASET ---
# You can customize these questions and answers to fit any topic!
# --- 1. SETUP THE FAQ DATASET ---
faq_data = [
    {
        "question": "What is CodeAlpha?",
        "answer": "CodeAlpha is a software development platform that provides remote internship opportunities to students, helping them gain hands-on experience in areas like AI, Web Development, and Cyber Security."
    },
    {
        "question": "What perks do interns receive?",
        "answer": "Interns receive an Internship Offer Letter, a QR-verified Completion Certificate, a Unique ID Certificate, a performance-based Letter of Recommendation, job opportunities/placement support, and resume building support."
    },
    {
        "question": "How long is the internship program?",
        "answer": "The standard duration for CodeAlpha internship modules is typically 1 month, during which you complete industry-relevant tasks."
    },
    {
        "question": "How do I submit my completed tasks?",
        "answer": "You should host your project code on GitHub and record a short video demonstration. Submit the GitHub repository link and video link through the submission form provided by CodeAlpha before the deadline."
    },
    {
        "question": "Can I get a completion certificate if I only finish one task?",
        "answer": "To successfully clear the internship and receive a certificate, you are generally required to complete and submit all the assigned mandatory tasks within the given deadline."
    },
    # 👇 ADD THESE NEW FAQ PAIRS HERE 👇
    {
        "question": "What is cosine similarity?",
        "answer": "Cosine similarity is a metric used to measure how similar two text documents are, irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. The closer the score is to 1, the more similar the texts are."
    },
    {
        "question": "How does this chatbot work?",
        "answer": "This chatbot uses TF-IDF Vectorization to convert your text input into mathematical vectors, and then applies Cosine Similarity to find which question in its database matches your question the closest!"
    }
]

# Extract lists of just questions and just answers for processing
faq_questions = [item["question"] for item in faq_data]
faq_answers = [item["answer"] for item in faq_data]

# --- 2. NLP SIMILARITY MATCHING FUNCTION ---
def get_chatbot_response(user_query):
    # Standardize input
    user_query = user_query.strip().lower()
    
    # Preprocess questions using TF-IDF Vectorizer
    # ngram_range=(1,2) helps capture word pairs for better context matching
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    
    # Combine the dataset questions with the user's new question
    all_texts = faq_questions + [user_query]
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Calculate similarity between the user's query (last item) and dataset queries (all items before last)
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
    
    # Find the index of the highest similarity score
    best_match_idx = similarity_scores.argmax()
    highest_score = similarity_scores[best_match_idx]
    
    # Set a confidence threshold. If similarity score is too low, use a fallback response.
    THRESHOLD = 0.25
    if highest_score >= THRESHOLD:
        return faq_answers[best_match_idx]
    else:
        return "I'm sorry, I couldn't find a matching question in my database. Could you please rephrase or ask something else?"


# --- 3. STREAMLIT USER INTERFACE (UI) ---
st.set_page_config(page_title="CodeAlpha FAQ Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 AI Chatbot for FAQs")
st.write("Ask me anything about the CodeAlpha internship overview, tasks, or perks!")
st.divider()

# Initialize session state for chat history so it doesn't clear on every refresh
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your CodeAlpha support assistant. How can I help you today?"}
    ]

# Display all previous messages in the chat UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Capture user input using Streamlit's native chat input box
if user_input := st.chat_input("Type your question here..."):
    
    # 1. Display user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Generate and display chatbot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            bot_response = get_chatbot_response(user_input)
            st.write(bot_response)
            
    st.session_state.messages.append({"role": "assistant", "content": bot_response})