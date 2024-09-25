from dotenv import load_dotenv
load_dotenv()
import os
import PyPDF2 as pdf
import streamlit as st
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 

# step 1 - get gemini response 
# step 2 -read pdf using PyPDF2 and extract text from pdf
# step 3 - input prompt that takes job description and resume as input 
# step 4 - take input from user and pass it to the input prompt using streamlit

# step 1 - get gemini response
def gemini_api_response(input):
    model = genai.GenerativeModel("gemini-1.5-pro")                      #  CODE                  
    response = model.generate_content(input)
    return response.text

# step 2 -read pdf using PyPDF2 and extract text from pdf
def text_extractor_from_pdf(pdf_file):
    reader = pdf.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text 

# step 3 - input prompt that takes job description and resume as input 
prompt_template = '''
    Analyze the following job description and candidate resume.

    {job_description}

    Resume text : {text}

    Task:

        Assess Keyword Match: Compare the keywords and skills listed in the job description with those present in the candidate's resume.
        Calculate ATS Score: Based on the keyword match and other relevant factors, calculate an ATS (Applicant Tracking System) score as a percentage.
        Identify Skill Gaps: Determine any skills or keywords mentioned in the job description that are missing from the candidate's resume.
        Provide Improvement Suggestions: Offer specific recommendations to the candidate on how they can improve their resume to better align with the job requirements.

    Output Format:

        ATS Score: [Percentage]
        Missing Skills: [List of missing skills or keywords] highlight them in BOLD font.
        Improvement Suggestions: [Detailed recommendations]

    Evaluation Criteria:

        Accuracy of keyword matching and ATS score calculation.
        Relevance and specificity of skill gap identification and improvement suggestions.
        Clarity and conciseness of the output.

Additional Considerations:

    Contextual Understanding: Ensure the AI model can understand the context of the job description and resume, including industry-specific terms and jargon.
    Weighting Factors: Consider implementing weighting factors for different types of keywords (e.g., hard skills, soft skills, industry-specific terms) to accurately assess the candidate's fit.
    Resume Structure: Take into account the structure of the resume (e.g., sections like summary, skills, experience) to identify relevant information.
    Customization: Allow for customization of the evaluation criteria and output format based on specific industry or company requirements.

'''

# step 4 - take input from user and pass it to the input prompt using streamlit

# Streamlit App
st.title("Resume VS Job Description Analyzer")

job_description = st.text_area("Job Description") # input to the prompt

st.subheader("Get your resume ready")

uploaded_file = st.file_uploader("Upload Your Resume in pdf format here : ", type="pdf", help="Please upload the PDF")

submit = st.button("Submit to Analyze") 

if submit:
    if uploaded_file is not None:
        text = text_extractor_from_pdf(uploaded_file) 
        prompt = prompt_template.format(job_description=job_description, text=text)
        answer = gemini_api_response(prompt)
        st.subheader(answer)