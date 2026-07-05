# Exam Agent X: Multi-Agent Syllabus & Evaluation Engine

An interactive, terminal-based study optimization dashboard engineered for the Kaggle x Google 5-Day AI Agents Intensive. This application leverages the Google GenAI SDK and a multi-agent framework to break down complex syllabus into targeted study schedules with an integrated Human-in-the-Loop evaluation checkpoint.

## 🚀 Key Features
- **Agentic Syllabus Planning:** Automatically structures raw syllabus inputs into distinct, color-coded study modules via Agent 1.
- **Human-in-the-Loop Checkpoint:** Halts execution to give the user real-time control over secondary asset generation.
- **Dynamic Evaluation Engine:** Ingests the planner's context via Agent 2 to generate custom mock viva questions, interactive terminal flashcards, or concise text summaries based on user input.
- **Screen-Responsive Interface:** Utilizes the Rich Python library to provide a clean, modern CLI without raw markdown formatting leakage.

## 🛠️ Local Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/exam-agent-x.git](https://github.com/YOUR_GITHUB_USERNAME/exam-agent-x.git)
   cd exam-agent-x
   ```
2. **Install Dependencies:**
     ```bash
     pip install -r requirements.txt
     ```
3. **Set Your API Key:**
    * **On Windows(Command Prompt):**
       ```DOS
       set GEMINI_API_KEY=your_actual_api_key_here
       ```
   * **On WIndows(PowerShell):**
       ```PowerShell
       $env:GEMINI_API_KEY="your_actual_api_key_here"
       ```
4. **Run the Application:
     ```bash
     python app.py
     ```
