from flask import Flask, render_template, request, redirect, session
import sqlite3
import random
import os

app = Flask(__name__)

app.secret_key = "hosa_math_secret_key"


DATABASE = "database.db"



# -------------------------
# DATABASE SETUP
# -------------------------

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn



def init_db():

    conn = get_db()

    print("DATABASE INITIALIZATION STARTED")


    conn.execute("""
    CREATE TABLE IF NOT EXISTS progress(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        completed INTEGER DEFAULT 0,

        correct INTEGER DEFAULT 0

    )
    """)


    conn.execute("""
    CREATE TABLE IF NOT EXISTS tools(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        default_name TEXT,

        custom_name TEXT

    )
    """)


    tools = [
        "Unit Converter",
        "Fraction Calculator",
        "Percentage Calculator",
        "Ratio Calculator",
        "Proportion Solver",
        "Dosage Calculator",
        "IV Flow Calculator",
        "Average Calculator",
        "Probability Calculator",
        "Area Calculator",
        "Volume Calculator",
        "Equation Solver"
    ]


    existing = conn.execute(
        "SELECT COUNT(*) FROM tools"
    ).fetchone()[0]


    if existing == 0:

        for tool in tools:

            conn.execute(
                """
                INSERT INTO tools(default_name, custom_name)

                VALUES (?,?)
                """,

                (tool, tool)

            )


    conn.commit()


    print("DATABASE INITIALIZATION COMPLETE")


    conn.close()
# -------------------------
# TEXTBOOK DATA
# -------------------------


chapters = [

{
"title":"Medical Math Foundations",
"text":
"""
Medical math focuses on accuracy, measurements,
and conversions used in healthcare.

Important skills:

- Unit conversion
- Measurement
- Precision

Formula:

Kilograms = Pounds ÷ 2.2

Example:

154 pounds ÷ 2.2 = 70 kilograms

Why:

Healthcare calculations must use correct units.
"""
},


{
"title":"Fractions and Decimals",
"text":
"""
Fractions represent parts of a whole.

Medical examples:

Dosage measurements
Concentration
Ratios


Example:

1/2 = 0.5


Why:

Many healthcare calculations require precise decimal values.
"""
},


{
"title":"Percentages",
"text":
"""
Percentages show parts per 100.

Formula:

Percent = Part ÷ Whole × 100


Example:

25 out of 100 patients

25/100 × 100 = 25%

Used for statistics and medical reports.
"""
},


{
"title":"Ratios and Proportions",
"text":
"""
Ratios compare two quantities.

Example:

250mg : 5mL

This relationship helps calculate medication amounts.
"""
},


{
"title":"Dimensional Analysis",
"text":
"""
Dimensional analysis converts units.

Example:

mg → g

Units cancel until the correct answer remains.

This prevents calculation mistakes.
"""
},


{
"title":"Dosage Calculations",
"text":
"""
Formula:

Desired Dose ÷ Available Dose × Quantity


Example:

500mg ÷ 250mg × 5mL

= 10mL


Used for medication calculations.
"""
},


{
"title":"IV Flow Rate Math",
"text":
"""
IV calculations determine fluid delivery.

Formula:

Volume ÷ Time

Example:

500mL over 5 hours

500 ÷ 5 = 100mL/hr
"""
},


{
"title":"Statistics",
"text":
"""
Statistics helps analyze healthcare data.

Mean:

Total ÷ Number of Values


Median:

Middle value


Mode:

Most common value
"""
},


{
"title":"Probability",
"text":
"""
Probability measures chance.

Formula:

Possible Outcomes ÷ Total Outcomes


Used for medical predictions.
"""
},


{
"title":"Geometry",
"text":
"""
Geometry measures shapes.

Area:

Length × Width


Volume:

Length × Width × Height


Used for measurements.
"""
},


{
"title":"Algebra",
"text":
"""
Algebra solves unknown values.

Example:

x + 5 = 10

x = 5


Variables represent unknown measurements.
"""
},


{
"title":"Graphs and Data",
"text":
"""
Charts display information.

Important skills:

- Reading trends
- Comparing data
- Understanding changes
"""
},


{
"title":"Scientific Notation",
"text":
"""
Scientific notation represents very large
or small numbers.

Example:

0.0005 = 5 × 10^-4
"""
},


{
"title":"Competition Strategies",
"text":
"""
Competition success requires:

- Speed
- Accuracy
- Understanding formulas
- Checking work
"""
},


{
"title":"Advanced HOSA Review",
"text":
"""
Final review combines:

Medical math
Statistics
Algebra
Conversions

Practice mixed problems.
"""
}

]



# -------------------------
# QUESTIONS
# -------------------------

questions = [

{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 154 pounds. What is the weight in kilograms?",
"answers":["50 kg","60 kg","70 kg","90 kg"],
"correct":"70 kg",
"explanation":
"To convert pounds to kilograms, divide by 2.2.\n\n154 ÷ 2.2 = 70 kg.",
"why":
"Healthcare uses standard units. Dividing by 2.2 keeps the measurement accurate."
},


{
"chapter":"Percentages",
"question":"What is 25% of 200?",
"answers":["25","50","75","100"],
"correct":"50",
"explanation":
"Convert 25% into decimal form:\n25 ÷ 100 = 0.25\n\n200 × 0.25 = 50.",
"why":
"Percent means 'out of 100', so we find the matching fraction of the total."
},


{
"chapter":"Geometry",
"question":"A rectangle has a length of 8cm and width of 5cm. What is the area?",
"answers":["13 cm²","20 cm²","40 cm²","80 cm²"],
"correct":"40 cm²",
"explanation":
"Area = length × width.\n\n8 × 5 = 40 cm².",
"why":
"Area measures the amount of space inside a shape."
},


{
"chapter":"IV Flow Rate",
"question":"500mL of fluid is given over 5 hours. What is the rate?",
"answers":["50mL/hr","100mL/hr","200mL/hr","500mL/hr"],
"correct":"100mL/hr",
"explanation":
"Rate = Volume ÷ Time.\n\n500 ÷ 5 = 100mL/hr.",
"why":
"Dividing by time tells us how much fluid is delivered each hour."
},


{
"chapter":"Fractions",
"question":"What is 1/2 as a decimal?",
"answers":["0.25","0.5","1.5","2"],
"correct":"0.5",
"explanation":
"1 divided by 2 equals 0.5.",
"why":
"Decimals represent parts of a whole."
},


{
"chapter":"Statistics",
"question":"Find the average of 10, 20, and 30.",
"answers":["15","20","25","30"],
"correct":"20",
"explanation":
"Add values and divide by amount:\n60 ÷ 3 = 20.",
"why":
"Mean gives the center value of a data set."
},


{
"chapter":"Ratios",
"question":"A ratio is used to compare what?",
"answers":["Numbers","Colors","Shapes","Letters"],
"correct":"Numbers",
"explanation":
"Ratios compare two quantities.",
"why":
"Healthcare calculations often compare measurements."
},


{
"chapter":"Dosage",
"question":"Desired dose is 500mg and available dose is 250mg in 5mL. How much is needed?",
"answers":["5mL","10mL","15mL","20mL"],
"correct":"10mL",
"explanation":
"500 ÷ 250 × 5 = 10mL.",
"why":
"The ratio between medicine amount and volume stays constant."
},


{
"chapter":"Probability",
"question":"Probability values are between:",
"answers":["0 and 1","1 and 10","10 and 100","-1 and 1"],
"correct":"0 and 1",
"explanation":
"Probability represents chance.",
"why":
"0 means impossible and 1 means certain."
}

]
user_progress = {

    "questions_completed":0,

    "correct_answers":0,

    "topics":{

        "Medical Math":0,

        "Fractions":0,

        "Percentages":0,

        "Geometry":0,

        "Dosage":0,

        "Statistics":0

    }

}


# -------------------------
# HOME
# -------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )



# -------------------------
# TEXTBOOK
# -------------------------

@app.route("/textbook")
def textbook():

    return render_template(
        "textbook.html",
        chapters=chapters
    )



@app.route("/chapter/<int:id>")
def chapter(id):

    chapter = chapters[id]


    return render_template(
        "chapter.html",
        chapter=chapter
    )



# -------------------------
# TOOLS
# -------------------------

@app.route("/tools")
def tools():

    conn=get_db()

    tools=conn.execute(
        "SELECT * FROM tools"
    ).fetchall()

    conn.close()


    return render_template(
        "tools.html",
        tools=tools
    )



@app.route("/rename_tool/<int:id>", methods=["POST"])
def rename_tool(id):

    name=request.form["name"]


    conn=get_db()

    conn.execute(
        """
        UPDATE tools

        SET custom_name=?

        WHERE id=?
        """,

        (name,id)

    )


    conn.commit()

    conn.close()


    return redirect("/tools")



# -------------------------
# QUIZ
# -------------------------

@app.route("/quiz")
def quiz():

    question=random.choice(questions)

    session["question"]=question


    return render_template(
        "quiz.html",
        question=question
    )



@app.route("/answer", methods=["POST"])
def answer():

    selected=request.form["answer"]

    question=session["question"]


    correct = selected == question["correct"]



    user_progress["questions_completed"] += 1



    if correct:

        user_progress["correct_answers"] += 1



    topic = question["chapter"]


    if topic in user_progress["topics"]:

        if not correct:

            user_progress["topics"][topic] += 1



    score = user_progress["correct_answers"]



    return render_template(

        "result.html",

        correct=correct,

        question=question,

        selected=selected,

        score=score

    )





# -------------------------
# AI ASSISTANT
# -------------------------

@app.route("/ai")
def ai():


    topics=user_progress["topics"]


    weakest=max(

        topics,

        key=topics.get

    )


    if user_progress["questions_completed"] == 0:


        message="""

Welcome to the AI Study Assistant!

Start practicing questions so I can analyze your performance.

"""


    else:


        message=f"""

AI Study Assistant Report


Questions Completed:

{user_progress["questions_completed"]}



Correct Answers:

{user_progress["correct_answers"]}



Recommended Improvement:


Your biggest improvement area is:

{weakest}



Study Plan:

1. Review the textbook chapter about {weakest}

2. Complete more practice questions

3. Use the math tools to improve accuracy



Remember:

Understanding why a formula works is more important than memorizing it.

"""



    return render_template(

        "ai.html",

        message=message

    )
# -------------------------
# TOOL CALCULATORS
# -------------------------


# -------------------------
# TOOL CALCULATORS
# -------------------------

tool_info = [

{
"name":"Unit Converter",
"description":"Converts pounds into kilograms.",
"why":"Healthcare uses kilograms for accurate measurements.",
"formula":"Kilograms = Pounds ÷ 2.2",
"inputs":["Pounds"]
},

{
"name":"Fraction Calculator",
"description":"Adds two fraction values.",
"why":"Fractions are used in measurements and dosage calculations.",
"formula":"Fraction calculations combine parts of a whole.",
"inputs":["Fraction Value"]
},

{
"name":"Percentage Calculator",
"description":"Finds a percentage of a number.",
"why":"Percentages are used in statistics and medical reports.",
"formula":"Number × Percentage ÷ 100",
"inputs":["Number","Percentage"]
},

{
"name":"Ratio Calculator",
"description":"Compares two quantities.",
"why":"Ratios are used for medication concentrations.",
"formula":"First Value ÷ Second Value",
"inputs":["First Value","Second Value"]
},

{
"name":"Proportion Solver",
"description":"Solves equal relationships.",
"why":"Proportions help calculate unknown medical measurements.",
"formula":"a/b = c/x",
"inputs":["Known Value","Multiplier"]
},

{
"name":"Dosage Calculator",
"description":"Calculates medication amount needed.",
"why":"Used to safely calculate medication doses.",
"formula":"Desired Dose ÷ Available Dose × Quantity",
"inputs":["Desired Dose (mg)","Available Dose (mg)","Quantity (mL)"]
},

{
"name":"IV Flow Calculator",
"description":"Calculates IV delivery speed.",
"why":"Used to determine fluid delivery rate.",
"formula":"Volume ÷ Time",
"inputs":["Volume (mL)","Time (hours)"]
},

{
"name":"Average Calculator",
"description":"Calculates the average of numbers.",
"why":"Used for analyzing patient data.",
"formula":"Total ÷ Number of Values",
"inputs":["Values"]
},

{
"name":"Probability Calculator",
"description":"Calculates chance.",
"why":"Used in healthcare statistics.",
"formula":"Successful Outcomes ÷ Total Outcomes",
"inputs":["Successful Outcomes","Total Outcomes"]
},

{
"name":"Area Calculator",
"description":"Calculates area.",
"why":"Used for measurement calculations.",
"formula":"Length × Width",
"inputs":["Length","Width"]
},

{
"name":"Volume Calculator",
"description":"Calculates volume.",
"why":"Used for fluid and measurement problems.",
"formula":"Length × Width × Height",
"inputs":["Length","Width","Height"]
},

{
"name":"Equation Solver",
"description":"Finds unknown values.",
"why":"Algebra helps solve medical math problems.",
"formula":"Solve for the missing variable.",
"inputs":["Known Number"]

}

]



@app.route("/calculator/<int:id>", methods=["GET","POST"])
def calculator(id):

    tool = tool_info[id-1]

    result = None
    explanation = ""


    if request.method=="POST":
a=request.form.get("value1")
b=request.form.get("value2")
c=request.form.get("value3")


        try:
a=float(a) if a else 0
b=float(b) if b else 0
c=float(c) if c else 0



            if id==1:

                result=round(a/2.2,2)

                explanation=f"""
Step 1:
Take the pounds value: {a}

Step 2:
Divide by 2.2

{a} ÷ 2.2 = {result} kg

Why:
Healthcare uses kilograms for many measurements.
"""


            elif id==2:

                result=a+b

                explanation="""
Step:
Add the two values together.

Why:
Fractions represent parts of a whole.
"""


            elif id==3:

                result=a*(b/100)

                explanation=f"""
Step 1:
Convert {b}% into decimal form.

{b}/100

Step 2:
Multiply by the total.

Why:
Percent means 'out of 100'.
"""


            elif id==4:

                result=a/b

                explanation="""
Step:
Divide the two values.

Why:
Ratios compare relationships between numbers.
"""


            elif id==5:

                result=a*b

                explanation="""
Step:
Multiply the known values.

Why:
Proportions keep relationships equal.
"""


           elif id==6:

    result=(a/b)*c

    explanation=f"""
Formula:

Desired Dose ÷ Available Dose × Quantity


{a} ÷ {b} × {c}

= {result} mL


Why:

This calculates the correct medication volume.
"""


          elif id==7:

    result=a/b

    explanation=f"""
Formula:

Volume ÷ Time


{a} ÷ {b}

= {result} mL/hr


Why:

This determines how fast IV fluid is delivered.
"""

            elif id==8:

                result=(a+b)/2

                explanation="""
Formula:

(Add values) ÷ Number of values

Why:
Average finds the middle measurement.
"""


            elif id==9:

                result=a/b

                explanation="""
Formula:

Successful Outcomes ÷ Total Outcomes

Why:
Probability measures chance.
"""


            elif id==10:

                result=a*b

                explanation="""
Formula:

Length × Width

Why:
Area measures space inside a shape.
"""


            elif id==11:

                result=a*b

                explanation="""
Formula:

Length × Width × Height

Why:
Volume measures the amount of space an object contains.
"""


            elif id==12:

                result=a-b

                explanation="""
Step:

Move known values away from the unknown.

Why:
Algebra helps solve missing measurements.
"""


        except:

            result="Please enter numbers only"



    return render_template(
        "calculator.html",
        tool=tool,
        result=result,
        explanation=explanation
    )
@app.route("/dashboard")
def dashboard():

    total = user_progress["questions_completed"]


    correct = user_progress["correct_answers"]



    if total > 0:

        accuracy = round(

            (correct / total) * 100,

            1

        )

    else:

        accuracy = 0



    return render_template(

        "dashboard.html",

        total=total,

        correct=correct,

        accuracy=accuracy,

        topics=user_progress["topics"]

    )


# -------------------------
init_db()


if __name__=="__main__":

    app.run(debug=True)
