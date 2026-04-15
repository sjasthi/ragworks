import math
from rag_logic import run_rag_eval, client
import json
import os
import time

eval_questions = [

# --- Academic Standing ---
{
    "question": "What determines undergraduate academic standing?",
    "target_answer": "Undergraduate academic standing is determined by a student's GPA and completion rate, including maintaining at least a 2.0 GPA.",
    "target_source": "2050_Undergrad_Academic_Standing.pdf"
},
{
    "question": "What happens if a student is placed on academic probation?",
    "target_answer": "If a student is placed on academic probation, it means their GPA has fallen below required standards and they must improve their academic performance to remain in good standing.",
    "target_source": "2050_Undergrad_Academic_Standing.pdf"
},

# --- Grading Policy ---
{
    "question": "What grading scale is used for letter grades?",
    "target_answer": "Letter grades are assigned based on a grading scale that corresponds to grade points for each letter grade.",
    "target_source": "2080_Grading_Policy.pdf"
},
{
    "question": "What does an incomplete grade mean?",
    "target_answer": "An incomplete grade means that a student did not finish required coursework and may receive a temporary grade such as N or F until completion.",
    "target_source": "2080_Grading_Policy.pdf"
},

# --- Academic Appeals ---
{
    "question": "What is the process for submitting an academic appeal?",
    "target_answer": "The process for submitting an academic appeal involves completing a formal appeal form to dispute a decision and seeking resolution through the academic appeals procedure.",
    "target_source": "209_Academic_Appeals_Procedure.pdf"
},
{
    "question": "When can a student file an academic appeal?",
    "target_answer": "A student can file an academic appeal within a specified time period, often within 60 days, following both informal and formal processes.",
    "target_source": "209_Academic_Appeals_Procedure.pdf"
},

# --- Transfer Credit ---
{
    "question": "How are transfer credits evaluated?",
    "target_answer": "Transfer credits are evaluated based on quality, comparability, appropriateness, and applicability to the student’s program.",
    "target_source": "2120_Transfer_Credit_Policy.pdf"
},
{
    "question": "What is the minimum grade required for transfer credit?",
    "target_answer": "A minimum grade is required for transfer credit, typically meaning the course must meet a certain academic standard to be accepted.",
    "target_source": "2120_Transfer_Credit_Policy.pdf"
},

# --- Attendance ---
{
    "question": "What is the attendance reporting requirement for students?",
    "target_answer": "Students must demonstrate active attendance, typically within the first or second week of class, and attendance must be reported accordingly.",
    "target_source": "2259_Attendance_and_Non-Attendance_Reporting.pdf"
},
{
    "question": "What happens if a student does not attend a class?",
    "target_answer": "If a student does not attend a class, they may be reported for non-attendance and could be dropped from the course.",
    "target_source": "2259_Attendance_and_Non-Attendance_Reporting.pdf"
},

# --- Honors ---
{
    "question": "What GPA is required to graduate with honors?",
    "target_answer": "To graduate with honors, students must meet GPA thresholds such as approximately 3.7 to 3.9 depending on distinctions like Cum Laude, Magna Cum Laude, or Summa Cum Laude.",
    "target_source": "2520_GradwithHonors.pdf"
},
{
    "question": "What are the different levels of graduation honors?",
    "target_answer": "The different levels of graduation honors include Cum Laude, Magna Cum Laude, and Summa Cum Laude.",
    "target_source": "2520_GradwithHonors.pdf"
},

# --- About University ---
{
    "question": "What type of university is Metropolitan State?",
    "target_answer": "Metropolitan State University is an accredited public university in Minnesota focused on higher education.",
    "target_source": "About_MetropolitanState.pdf"
},
{
    "question": "What is the mission of Metropolitan State University?",
    "target_answer": "The mission of Metropolitan State University is to provide inclusive, accessible, and empowering education in an antiracist and supportive environment.",
    "target_source": "About_MetropolitanState.pdf"
},

# --- QUESTION 15 ----
# --- Financial Aid ---
{
    "question": "How do students apply for financial aid?",
    "target_answer": "Students apply for financial aid by completing the FAFSA or Dream Act application and working with the Minnesota Office of Higher Education.",
    "target_source": "Applying_for_FinancialAid.pdf"
},
{
    "question": "What documents are needed for financial aid?",
    "target_answer": "Financial aid applications typically require documents such as tax returns, income information, and completed FAFSA forms.",
    "target_source": "Applying_for_FinancialAid.pdf"
},

# --- Advisor ---
{
    "question": "How can a student find their academic advisor?",
    "target_answer": "Students can find their academic advisor using tools like DARS or eServices provided by the university.",
    "target_source": "Find_Advisor.pdf"
},

# --- First Year Admissions ---
{
    "question": "What are the requirements for first-year admission?",
    "target_answer": "First-year admission requirements include meeting GPA thresholds such as around 2.75 or equivalent scores like GED scores and may include conditional or automatic admission criteria.",
    "target_source": "FirstYearStudent_Admissions.pdf"
},
{
    "question": "What materials are required for first-year applications?",
    "target_answer": "First-year applications require materials such as transcripts, application forms, and possibly AP or other academic records.",
    "target_source": "FirstYearStudent_Admissions.pdf"
},

# --- First Semester ---
{
    "question": "What should students complete before their first semester?",
    "target_answer": "Before their first semester, students should complete tasks such as financial aid, orientation, meeting an academic advisor, activating MFA, reviewing DARS, getting a student ID, and preparing course materials.",
    "target_source": "First_Semester_Checklist.pdf"
},

# --- GELS ---
{
    "question": "What is the GELS course requirement?",
    "target_answer": "The GELS requirement includes completing multiple goal areas, typically around 10 goals and approximately 48 credits, including upper division coursework.",
    "target_source": "GELS_CourseList.pdf"
},

# --- Student ID ---
{
    "question": "How do students obtain a student ID?",
    "target_answer": "Students can obtain a student ID at locations such as the Learning Center, Commons desk, or similar campus services.",
    "target_source": "Getting_StudentID.pdf"
},

# --- Graduation ---
{
    "question": "What is required to apply for graduation?",
    "target_answer": "To apply for graduation, students must complete required coursework and may need to attend a graduation workshop or complete application steps.",
    "target_source": "Graduation_and_Commencement.pdf"
},
{
    "question": "What is commencement and when does it occur?",
    "target_answer": "Commencement is a formal graduation ceremony that typically occurs twice per year, in the spring and fall.",
    "target_source": "Graduation_and_Commencement.pdf"
},

# --- Placement ---
{
    "question": "What is a placement assessment?",
    "target_answer": "A placement assessment such as Accuplacer evaluates a student’s skills in areas like math, reading, and writing to determine appropriate course placement.",
    "target_source": "Placement_Assessment.pdf"
},

# --- Student Life ---
{
    "question": "What opportunities are available for student leadership?",
    "target_answer": "Students can participate in leadership opportunities such as student organizations, UAB, orientation programs, events, and campus employment.",
    "target_source": "StudentLife_and_Leadership_Development.pdf"
},

# --- Academic Calendar ---
{
    "question": "When does the Summer 2026 semester begin?",
    "target_answer": "The Summer 2026 semester begins around mid-May, with sessions such as the first session starting around May 16.",
    "target_source": "Summer2026_AcademicCalendar.pdf"
},

# --- Transcript ---
{
    "question": "How can a student request a transcript?",
    "target_answer": "Students can request a transcript through methods such as mail, in-person requests, or through student services, often requiring payment.",
    "target_source": "Transcript_Request_Form.pdf"
},

# --- Question 30 ---
# --- Transfer Admissions ---
{
    "question": "What are the requirements for transfer student admission?",
    "target_answer": "Transfer student admission requires submitting transcripts from previous institutions and meeting academic requirements set by the university.",
    "target_source": "Transfer_Student_Admissions.pdf"
},

# --- Waitlist ---
{
    "question": "How does the course waitlist system work?",
    "target_answer": "The course waitlist system allows students to join a list for full courses, where they may be notified if a seat becomes available.",
    "target_source": "Waitlist_and_CourseCancellations.pdf"
},
{
    "question": "What happens when a course is canceled?",
    "target_answer": "When a course is canceled, students are notified and may receive refunds or need to register for alternative courses.",
    "target_source": "Waitlist_and_CourseCancellations.pdf"
},

# --- INTENTIONAL FAILURE CASES ---
{
    "question": "What is the tuition cost per credit?",
    "target_answer": "The answer is not available in the provided documents.",
    "target_source": "NONE"
},
{ 
    "question": "What is the policy on pets on campus?",
    "target_answer": "The answer is not available in the provided documents.",
    "target_source": "NONE"
}
]

def score_answer(question, generated_answer, target_answer):
    """
    Uses an LLM judge to compare the generated answer to the target answer.
    Returns 1 if the generated answer is correct, otherwise 0.
    """

    judge_prompt = f"""
You are evaluating a RAG system's answer.

Question:
{question}

Expected Answer:
{target_answer}

Generated Answer:
{generated_answer}

Decide whether the generated answer is correct based on meaning, not exact wording.
A correct answer may use different phrasing than the expected answer.
If the generated answer is correct or semantically equivalent, return 1.
If it is incorrect, incomplete in a meaningful way, or contradicts the expected answer, return 0.

Respond with ONLY a single character:
1 or 0
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict evaluator that returns only 1 or 0."
                },
                {
                    "role": "user",
                    "content": judge_prompt
                }
            ],
            temperature=0.0
        )

        result = response.choices[0].message.content.strip()
        return 1 if result == "1" else 0

    except Exception as e:
        print(f"LLM judge failed: {e}")
        return 0


def score_source(retrieved_docs, target_source):
    """
    Basic 0/1 source scoring.
    Returns 1 if the expected source appears in retrieved docs.
    """
    if target_source == "NONE":
        return 1
    
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
        target_answer = item["target_answer"]
        target_source = item["target_source"]

        rag_result = run_rag_eval(
            user_input=question,
            top_k=top_k,
            temperature=temperature,
            top_p=top_p
        )

        generated_answer = rag_result.get("answer", "")
        retrieved_docs = rag_result.get("retrieved_docs", [])

        answer_score = score_answer(question, generated_answer, target_answer)
        source_score = score_source(retrieved_docs, target_source)

        total_answer_score += answer_score
        total_source_score += source_score

        results.append({
            "question": question,
            "target_answer": target_answer,
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

#not beinging used in the current loop but can be used for quick single-run testing and logging
def print_results(summary):
    print("\nRESULTS SUMMARY")
    print("===================================")
    print(f"Parameters: {summary['parameters']}")
    print(f"Total Questions: {summary['total_questions']}")
    print(f"Answer Accuracy: {summary['answer_accuracy']:.2f}")
    print(f"Source Accuracy: {summary['source_accuracy']:.2f}")
    print("===================================")


def save_results(summary, filename="eval_results.json3"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

# Define parameter grid for evaluation
top_k_values = [2, 5, 8]
temperature_values = [0.0, 0.2]
top_p_values = [0.8, 1.0]

# main execution block to run evaluations across the parameter grid loop and save results
if __name__ == "__main__":

    test_questions = eval_questions #can be adjuested to run on a subset for quicker testing
    run_count = 0 #to track total runs for logging purposes
    total_runs = len(top_k_values) * len(temperature_values) * len(top_p_values)
    start_time = time.time()
    all_summaries = []

    for k in top_k_values:
        for temp in temperature_values:
            for p in top_p_values:

                run_count += 1
                elapsed = time.time() - start_time
                progress = (run_count / total_runs) * 100

                avg_time_per_run = elapsed / run_count
                estimated_total = avg_time_per_run * total_runs
                remaining = estimated_total - elapsed

                print("\n===================================")
                print(f"Starting evaluation run {run_count}/{total_runs}")
                print(f"Running eval: top_k={k}, temp={temp}, top_p={p}")
                print(f"Progress: {progress:.1f}%")
                print(f"Elapsed Time: {elapsed:.1f}s")
                print(f"Estimated Remaining Time: {remaining:.1f}s")
                print("===================================")

                summary = run_evaluation(
                    test_questions,
                    top_k=k,
                    temperature=temp,
                    top_p=p
                )

                all_summaries.append(summary)

                time.sleep(1)  # brief pause between runs to avoid overwhelming the system 

    # Save ALL runs together
    save_results(all_summaries, filename="eval_results_grid3.json")
    print("\nAll evaluations completed. Results saved to eval_results_grid.json")
    print("\n========== FINAL RESULTS ==========")
    for summary in all_summaries:
        params = summary["parameters"]
        print(
            f"top_k={params['top_k']}, "
            f"temp={params['temperature']}, "
            f"top_p={params['top_p']} | "
            f"Answer Acc={summary['answer_accuracy']:.2f} | "
            f"Source Acc={summary['source_accuracy']:.2f}"
        )
    print("===================================")