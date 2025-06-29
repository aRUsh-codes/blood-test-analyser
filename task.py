## Importing libraries and files
from crewai import Task

from agents import doctor, verifier
from tools import search_tool, BloodTestReportTool

## Creating a task to help solve user's query
help_patients = Task(
    description="""You are a highly experienced medical doctor reviewing a patient's blood test report.
        Your goal is to carefully analyze the report, identify any significant findings, and summarize the results clearly. 
        Use accessible medical terminology when needed, and explain abnormal values or critical ranges.
        If any health conditions may be indicated, list them with a brief explanation.
        Ensure your summary is concise, evidence-based, and useful for general understanding.""",

    expected_output="""A clear, factual summary of the blood test report in under 100 words.
        Include only relevant medical findings and explain their implications in layman's terms.
        Avoid speculative diagnoses. Structure the output as bullet points or short paragraphs.
        Do not fabricate data or URLs. Focus on clarity, accuracy, and medical relevance.""",

    agent=doctor,
    tools=[BloodTestReportTool()],
    async_execution=False,
)

## Creating a nutrition analysis task
nutrition_analysis = Task(
    description="""You are a certified clinical nutritionist with deep knowledge of interpreting blood test reports.
        Your task is to analyze the blood report data and provide personalized dietary recommendations.
        Explain which nutrients the patient may be deficient in or consuming in excess, based on specific markers in the report. 
        Recommend relevant foods to include or avoid, and provide evidence-based nutritional guidance aligned with the user's query: {query}.
        Use accessible language while maintaining scientific accuracy.""",

    expected_output="""A list of personalized, evidence-based nutrition recommendations in bullet points.
        Each point should reference a relevant blood marker (e.g., iron, B12, glucose) and explain the suggested dietary adjustment.
        Include 1–2 optional supplements only if justified by the data. Avoid pseudoscience or exaggerated claims.
        Keep the advice clear, realistic, and medically responsible.""",

    agent=doctor,
    tools=[BloodTestReportTool()],
    async_execution=False,
)

## Creating an exercise planning task
exercise_planning = Task(
    description="""You are a certified fitness and exercise specialist. Your goal is to create a safe, personalized workout plan for the user
        based on their blood test results and query: {query}. Consider markers like glucose levels, hemoglobin, vitamin D, thyroid function,
        and any other indicators that may influence fitness, stamina, or recovery.
        If any contraindications exist (e.g., low hemoglobin, thyroid imbalance), adapt the exercise plan accordingly.
        Include clear reasoning behind each recommendation, and ensure it is suitable for a general adult audience unless otherwise specified.""",

    expected_output="""A personalized, safe, and effective workout plan in bullet points.
        Include 3–5 recommended activities (e.g., strength training, cardio, yoga) with brief explanations.
        Tailor intensity, frequency, and duration based on blood report data.
        Mention any health considerations or limitations. Avoid dangerous or exaggerated claims, and do not invent exercises or terminology.""",

    agent=doctor,
    tools=[BloodTestReportTool()],
    async_execution=False,
)

    
verification = Task(
    description="""You are a document analysis specialist. Your goal is to determine whether the uploaded PDF document is a valid blood test report.
        Review the document contents to identify key medical terminology, test names (e.g., CBC, Hemoglobin, Glucose, TSH), lab values, and reference ranges.
        If such elements are present, classify the document as a valid blood test report.
        If the document lacks clear indicators of a lab report (e.g., it contains unrelated content like invoices, recipes, or letters), classify it as invalid.
        Be objective and provide reasoning for your decision.""",

    expected_output="""Return a short classification summary (valid/invalid) followed by a brief explanation.
        If valid, optionally mention key terms or sections that support your judgment.
        If invalid, explain what is missing. Avoid hallucinations, speculation, or invented content.
        Be concise and factual, ideally under 50 words.""",

    agent=doctor,
    tools=[BloodTestReportTool()],
    async_execution=False
)