## Project Setup and Execution Guide
- ### Install Required Libraries
  ```sh
  pip install -r requirement.txt
  ```

- ### Make sure all the version dependencies are compatible with each other.

- ### Create a .env file and add your OPEN_API_KEY 

## Getting Started
 - Run the app by the command ```uvicorn main:app --reload```
 - Test the app if its working correctly
     - For root path : the message ```{Blood Test Report Analyser API is running}``` will be displayed
     - For /analyze path : Since it is a POST method so follow the given steps to test:
         - go to ```http://127.0.0.1:8000/docs```
         - In the POST method click on ```Try it out```
         - Choose file(sample or blood_test_report.pdf) and Execute.
         - Response will be in json format.

## Debugging and Changes made
### 1. `llm` was undefined
- **Issue**: `llm = llm` was present in `agents.py` without initialization.
- **Fix**: Replaced with OpenAI's `ChatOpenAI` instance using `langchain`.
- **Reason**: LangChain agents require an LLM instance; `llm` must be defined and passed in.

---

### 2. Incorrect use of `tool=` instead of `tools=`
- **Issue**: Used `tool=[...]` in `Agent(...)`, but LangChain expects `tools=[...]`.
- **Fix**: Renamed to `tools=[...]`.
- **Reason**: The parameter name `tool` caused validation errors as only `tools` is recognized.

---

### 3. `read_data_tool` used as a plain function
- **Issue**: Passed `BloodTestReportTool.read_data_tool` (a function) into `tools=`.
- **Fix**: Wrapped inside a LangChain `BaseTool` subclass with a `_run()` method.
- **Reason**: CrewAI expects tools to be valid `BaseTool` instances, not raw functions.

---

### 4. `BloodTestReportTool` lacked required method `_run()`
- **Issue**: Attempted to instantiate a `BaseTool` subclass without `_run()`.
- **Fix**: Implemented `_run()` to read and return cleaned PDF content.
- **Reason**: `BaseTool` is abstract and requires `_run()` for functionality.

---

### 5. `name` and `description` attributes not annotated
- **Issue**: `name = "..."` in tool class raised PydanticUserError.
- **Fix**: Annotated as `name: str = "..."` and `description: str = "..."`.
- **Reason**: Pydantic v2+ requires explicit type annotations on fields.

---

### 6. `run_crew()` used an async tool in a sync function
- **Issue**: `read_data_tool` was async, but `kickoff()` expected sync behavior.
- **Fix**: Refactored `read_data_tool` to be a synchronous method.
- **Reason**: Avoided async complications and ensured compatibility with `Crew.kickoff()`.

---

## ✍️ Prompt Engineering & Role Improvements (Changed prompts and descriptions to make it more sensible and produce accurate information.)

### ✅ Task: `help_patients`
- Refactored into a focused, professional diagnostic summary generator.
- Eliminated hallucinations, fake URLs, and contradictions.
  
### ✅ Task: `nutrition_analysis`
- Refocused on interpreting real nutritional markers from blood data.
- Discouraged pseudoscience, expensive unneeded supplements, or contradictions.

### ✅ Task: `exercise_planning`
- Turned extreme, unsafe suggestions into a safe, personalized F.I.T.T.-based plan.
- Included adaptation based on health data (e.g., anemia, thyroid).

### ✅ Task: `verification`
- Changed from "always say yes" to structured PDF validation based on actual test patterns.
- Enforced decision logic (valid/invalid) with short explanations.

---

## 🧠 Agent Role Refinement

### ✅ Agent: `doctor`
- Changed from arrogant, TV-character style into a trustworthy diagnostic physician.
- Empathetic and medically precise.

### ✅ Agent: `verifier`
- Transformed from careless approver to a skilled documentation verifier.
- Analyzes document structure, keywords, and lab markers.

### ✅ Agent: `nutritionist`
- Replaced influencer stereotype with a certified clinical nutritionist.
- Evidence-based, realistic, and personalized.

### ✅ Agent: `exercise_specialist`
- Upgraded from unsafe gym-bro coach to certified exercise physiologist.
- Prioritizes safety, progression, and adaptation to health metrics.

---

## ✅ Outcome

- System is now fully refactored to be safe, medically sound, and production-ready.
- All tools and agents follow ethical, professional design principles.
- Project can run offline or online depending on available LLM resources.


