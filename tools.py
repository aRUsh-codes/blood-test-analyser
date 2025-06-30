## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tools
from crewai_tools import SerperDevTool
from langchain.tools import Tool
from langchain.document_loaders import PyPDFLoader as PDFLoader
from crewai.tools import BaseTool
from typing import Optional, Any
## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class BloodTestReportTool(BaseTool):
    name: str = "ReadBloodReportPDF"
    description: str = "Reads and returns the text from a blood report PDF file"

    def _run(self, path: str = 'data/sample.pdf', run_manager: Optional[Any] = None) -> str:
        docs = PDFLoader(file_path=path).load()
        full_report = ""
        for data in docs:
            content = data.page_content.replace("\n\n", "\n")
            full_report += content + "\n"
        return full_report

    def _arun(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Async not implemented for this tool")
    
    @staticmethod
    async def read_data_tool(path='data/sample.pdf'):
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Blood Test report file
        """
        
        docs = PDFLoader(file_path=path).load()

        full_report = ""
        for data in docs:
            # Clean and format the report data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += content + "\n"
            
        return full_report

## Creating Nutrition Analysis Tool
class NutritionTool:
    async def analyze_nutrition_tool(blood_report_data):
        # Process and analyze the blood report data
        processed_data = blood_report_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement nutrition analysis logic here
        nutrition_insights = []

        if "Hemoglobin" in processed_data:
            if "low" in processed_data.lower() or "decreased" in processed_data.lower():
                nutrition_insights.append("- Hemoglobin is low. Recommend increasing iron intake (e.g., spinach, red meat, lentils).")
        
        if "Vitamin B12" in processed_data:
            if "low" in processed_data.lower():
                nutrition_insights.append("- Vitamin B12 deficiency detected. Recommend dairy, eggs, or B12 supplements (especially for vegetarians).")

        if "Glucose" in processed_data:
            if "high" in processed_data.lower():
                nutrition_insights.append("- Elevated glucose levels. Recommend reducing sugar, processed carbs, and increasing fiber-rich foods.")

        if "Cholesterol" in processed_data:
            if "high" in processed_data.lower():
                nutrition_insights.append("- High cholesterol. Suggest heart-healthy fats (like olive oil, nuts), more vegetables, and cutting trans fats.")

        if "Calcium" in processed_data:
            if "low" in processed_data.lower():
                nutrition_insights.append("- Low calcium levels. Recommend dairy, tofu, sesame seeds, or calcium-fortified foods.")

        if "Vitamin D" in processed_data:
            if "low" in processed_data.lower():
                nutrition_insights.append("- Vitamin D deficiency. Recommend sun exposure, fortified foods, or supplements.")

        if not nutrition_insights:
            nutrition_insights.append("No major nutritional deficiencies detected in the report. Maintain a balanced diet.")

        return "\n".join(nutrition_insights)

## Creating Exercise Planning Tool
class ExerciseTool:
    async def create_exercise_plan_tool(blood_report_data):        
        # TODO: Implement exercise planning logic here
        plan = []

        report = blood_report_data.lower()

        # Hemoglobin check (anemia-related)
        if "hemoglobin" in report and "low" in report:
            plan.append("- Low hemoglobin detected: Start with light to moderate aerobic exercises like walking or yoga. Avoid intense cardio until levels normalize.")

        # Glucose (diabetes/insulin sensitivity)
        if "glucose" in report and "high" in report:
            plan.append("- Elevated glucose levels: Recommend 30 minutes of brisk walking, cycling, or moderate cardio 5x/week. Helps improve insulin sensitivity.")

        # Thyroid (hypothyroidism or hyperthyroidism)
        if "thyroid" in report:
            if "low" in report or "hypo" in report:
                plan.append("- Hypothyroid profile: Focus on low-impact strength training, yoga, and stretching to boost metabolism.")
            elif "high" in report or "hyper" in report:
                plan.append("- Hyperthyroid profile: Incorporate calming exercises like tai chi, pilates, and walking to avoid overstimulation.")

        # Cholesterol
        if "cholesterol" in report and "high" in report:
            plan.append("- High cholesterol: Recommend aerobic exercises like jogging, swimming, or dancing 4–5x/week.")

        # No specific indicators
        if not plan:
            plan.append("- No critical findings: Recommend a balanced mix of strength training (2–3x/week) and cardio (3–4x/week). Include flexibility routines.")

        return "\n".join(plan)