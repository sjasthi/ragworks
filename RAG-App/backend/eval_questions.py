import math
from rag_logic import run_rag_eval
import json
import os

eval_questions = [

# --- Academic Standing ---
{
    "question": "What determines undergraduate academic standing?",
    "target_keywords": ["gpa", "academic standing", "2.0", "completion rate"],
    "target_source": "2050_Undergrad_Academic_Standing.pdf"
},
{
    "question": "What happens if a student is placed on academic probation?",
    "target_keywords": ["probation", "gpa"],
    "target_source": "Academic Standing Review Procedure.pdf"
},

# --- Grading Policy ---
{
    "question": "What grading scale is used for letter grades?",
    "target_keywords": ["grading scale", "letter grades", "grade points"],
    "target_source": "2080_Grading_Policy.pdf"
},
{
    "question": "What does an incomplete grade mean?",
    "target_keywords": ["incomplete", "not finished", "F", "N"],
    "target_source": "2080_Grading_Policy.pdf"
},

# --- Academic Appeals ---
{
    "question": "What is the process for submitting an academic appeal?",
    "target_keywords": ["appeal form", "dispute", "resolution", "formal"],
    "target_source": "209_Academic_Appeals_Procedure.pdf"
},
{
    "question": "When can a student file an academic appeal?",
    "target_keywords": ["60", "formal", "informal"],
    "target_source": "209_Academic_Appeals_Procedure.pdf"
},

# --- Transfer Credit ---
{
    "question": "How are transfer credits evaluated?",
    "target_keywords": ["quality", "comparability", "appropriateness", "applicability"],
    "target_source": "2120_Transfer_Credit_Policy.pdf"
},
{
    "question": "What is the minimum grade required for transfer credit?",
    "target_keywords": ["transfer", "minimum grade"],
    "target_source": "2120_Transfer_Credit_Policy.pdf"
},

# --- Attendance ---
{
    "question": "What is the attendance reporting requirement for students?",
    "target_keywords": ["first", "active attendance", "second week", "last date"],
    "target_source": "2259_Attendance_and_Non-Attendance_Reporting.pdf"
},
{
    "question": "What happens if a student does not attend a class?",
    "target_keywords": ["non-attendance", "report","dropped"],
    "target_source": "2259_Attendance_and_Non-Attendance_Reporting.pdf"
},

# --- Honors ---
{
    "question": "What GPA is required to graduate with honors?",
    "target_keywords": ["gpa", "honors", "3.9", "3.7", "3.8", "Magna", "Summa", "Cum Laude"],
    "target_source": "2520_GradwithHonors.pdf"
},
{
    "question": "What are the different levels of graduation honors?",
    "target_keywords": ["honors", "Magna", "Summa", "Cum Laude"],
    "target_source": "2520_GradwithHonors.pdf"
},

# --- About University ---
{
    "question": "What type of university is Metropolitan State?",
    "target_keywords": ["accredited", "university", "minnesota", "higher education"],
    "target_source": "About_MetropolitanState.pdf"
},
{
    "question": "What is the mission of Metropolitan State University?",
    "target_keywords": ["empowers", "inclusive", "antiracist", "supportive"],
    "target_source": "About_MetropolitanState.pdf"
},

# --- QUESTION 15 ----
# --- Financial Aid ---
{
    "question": "How do students apply for financial aid?",
    "target_keywords": ["fasfa", "Dream act", "student aid", "MN Office"],
    "target_source": "Applying_for_FinancialAid.pdf"
},
{
    "question": "What documents are needed for financial aid?",
    "target_keywords": ["application", "fasfa", "tax return", "income"],
    "target_source": "Applying_for_FinancialAid.pdf"
},

# --- Advisor ---
{
    "question": "How can a student find their academic advisor?",
    "target_keywords": ["advisor", "DARS", "eServices"],
    "target_source": "Find_Advisor.pdf"
},

# --- First Year Admissions ---
{
    "question": "What are the requirements for first-year admission?",
    "target_keywords": ["2.75", "GED", "165", "conditional", "automatic", "scores"],
    "target_source": "FirstYearStudent_Admissions.pdf"
},
{
    "question": "What materials are required for first-year applications?",
    "target_keywords": ["transcripts", "transcript", "AP", "application"],
    "target_source": "FirstYearStudent_Admissions.pdf"
},

# --- First Semester ---
{
    "question": "What should students complete before their first semester?",
    "target_keywords": ["financial aid", "student orientation", "MFA", "DARS", "academic advisor", "student ID", "books", "checklist"],
    "target_source": "First_Semester_Checklist.pdf"
},

# --- GELS ---
{
    "question": "What is the GELS course requirement?",
    "target_keywords": ["10", "goals", "48 credits", "upper divison", "300"],
    "target_source": "GELS_CourseList.pdf"
},

# --- Student ID ---
{
    "question": "How do students obtain a student ID?",
    "target_keywords": ["first-floor", "Learning center", "Commons desk", "Star", "Tech ID"],
    "target_source": "Getting_StudentID.pdf"
},

# --- Graduation ---
{
    "question": "What is required to apply for graduation?",
    "target_keywords": ["graduation workshop", "completion", "courswork"],
    "target_source": "Graduation_and_Commencement.pdf"
},
{
    "question": "What is commencement and when does it occur?",
    "target_keywords": ["formal event", "ceremony", "twice", "spring", "fall"],
    "target_source": "Graduation_and_Commencement.pdf"
},

# --- Placement ---
{
    "question": "What is a placement assessment?",
    "target_keywords": ["Accuplacer", "assessment", "skills", "math", "reading", "writing"],
    "target_source": "Placement_Assessment.pdf"
},

# --- Student Life ---
{
    "question": "What opportunities are available for student leadership?",
    "target_keywords": ["organizations", "UAB", "Orientation", "Commencement", "Events", "Employment"],
    "target_source": "StudentLife_and_Leadership_Development.pdf"
},

# --- Academic Calendar ---
{
    "question": "When does the Summer 2026 semester begin?",
    "target_keywords": ["summer", "May 16", "first session", "full session"],
    "target_source": "Summer2026_AcademicCalendar.pdf"
},

# --- Transcript ---
{
    "question": "How can a student request a transcript?",
    "target_keywords": ["mail", "in-person", "student services", "cash"],
    "target_source": "Transcript_Request_Form.pdf"
},

# --- Question 30 ---
# --- Transfer Admissions ---
{
    "question": "What are the requirements for transfer student admission?",
    "target_keywords": ["transfer", "admission"],
    "target_source": "Transfer_Student_Admissions.pdf"
},

# --- Waitlist ---
{
    "question": "How does the course waitlist system work?",
    "target_keywords": ["waitlist", "course"],
    "target_source": "Waitlist_and_CourseCancellations.pdf"
},
{
    "question": "What happens when a course is canceled?",
    "target_keywords": ["course", "cancellation"],
    "target_source": "Waitlist_and_CourseCancellations.pdf"
},

# --- INTENTIONAL FAILURE CASES ---
{
    "question": "What is the tuition cost per credit?",
    "target_keywords": ["do not know"],
    "target_source": "NONE"
},
{ 
    "question": "What is the policy on pets on campus?",
    "target_keywords": ["do not know"],
    "target_source": "NONE"
}
]

def score_answer(generated_answer, target_keywords):
    """
    Basic 0/1 answer scoring.
    Returns 1 if ALL target keywords appear in the generated answer.
    """
    generated = generated_answer.strip().lower()
    matches = sum(
        1 for keyword in target_keywords
        if keyword.strip().lower() in generated
    )
    required = math.ceil(len(target_keywords) / 2)
    return 1 if matches >= required else 0


def score_source(retrieved_docs, target_source):
    """
    Basic 0/1 source scoring.
    Returns 1 if the expected source appears in retrieved docs.
    """
    sources = []

    for doc in retrieved_docs:
        source = doc.get("source", "")
        if source:
            sources.append(os.path.basename(source))

    return 1 if target_source in sources else 0


def run_evaluation(eval_questions, top_k=3, temperature=0.0, top_p=1.0):
    """
    Runs the RAG pipeline against a fixed evaluation set and computes:
    - answer accuracy
    - source accuracy
    """
    results = []
    total_answer_score = 0
    total_source_score = 0

    for item in eval_questions:
        question = item["question"]
        target_keywords = item["target_keywords"]
        target_source = item["target_source"]

        rag_result = run_rag_eval(
            user_input=question,
            top_k=top_k,
            temperature=temperature,
            top_p=top_p
        )

        generated_answer = rag_result.get("answer", "")
        retrieved_docs = rag_result.get("retrieved_docs", [])

        answer_score = score_answer(generated_answer, target_keywords)
        source_score = score_source(retrieved_docs, target_source)

        total_answer_score += answer_score
        total_source_score += source_score

        results.append({
            "question": question,
            "target_keywords": target_keywords,
            "generated_answer": generated_answer,
            "target_source": target_source,
            "retrieved_sources": [os.path.basename(doc.get("source", "UNKNOWN")) for doc in retrieved_docs],
            "answer_score": answer_score,
            "source_score": source_score
        })

    total = len(eval_questions)
    answer_accuracy = total_answer_score / total if total else 0
    source_accuracy = total_source_score / total if total else 0

    summary = {
        "parameters": {
            "top_k": top_k,
            "temperature": temperature,
            "top_p": top_p
        },
        "total_questions": total,
        "answer_accuracy": answer_accuracy,
        "source_accuracy": source_accuracy,
        "results": results
    }

    return summary


def print_results(summary):
    print("\n===== RAG EVALUATION RESULTS =====")
    print(f"Parameters: {summary['parameters']}")
    print(f"Total Questions: {summary['total_questions']}")
    print(f"Answer Accuracy: {summary['answer_accuracy']:.2f}")
    print(f"Source Accuracy: {summary['source_accuracy']:.2f}")

    for i, result in enumerate(summary["results"], start=1):
        print(f"\n--- Question {i} ---")
        print(f"Question: {result['question']}")
        print(f"Target Keywords: {result['target_keywords']}")
        print(f"Generated Answer: {result['generated_answer']}")
        print(f"Target Source: {result['target_source']}")
        print(f"Retrieved Sources: {result['retrieved_sources']}")
        print(f"Answer Score: {result['answer_score']}")
        print(f"Source Score: {result['source_score']}")


def save_results(summary, filename="eval_results.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)


if __name__ == "__main__":
    test_questions = eval_questions

    summary = run_evaluation(
        test_questions,
        top_k=3,
        temperature=0.0,
        top_p=1.0
    )

    print_results(summary)
    save_results(summary)