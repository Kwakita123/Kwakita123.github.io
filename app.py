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

- Dosage measurements
- Concentration
- Ratios


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


25 ÷ 100 × 100 = 25%


Why:

Percentages are used for statistics,
patient data, and medical reports.
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


Why:

Healthcare workers use ratios to maintain
accurate measurements.
"""
},


{
"title":"Dimensional Analysis",
"text":
"""
Dimensional analysis converts between units.


Example:

mg → g


Units cancel until the correct answer remains.


Why:

This method prevents unit conversion mistakes.
"""
},


{
"title":"Dosage Calculations",
"text":
"""
Dosage calculations determine medication amounts.


Formula:

Desired Dose ÷ Available Dose × Quantity


Example:

500mg ÷ 250mg × 5mL

= 10mL


Why:

Correct dosage calculations help provide safe
and accurate medication amounts.
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


Why:

Healthcare workers use IV calculations to control
fluid delivery speed.
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


Why:

Statistics helps healthcare workers understand
data and make decisions.
"""
},


{
"title":"Probability",
"text":
"""
Probability measures chance.


Formula:

Possible Outcomes ÷ Total Outcomes


Example:

Probability helps predict possible outcomes
using data.


Why:

Healthcare uses probability when analyzing risks
and statistics.
"""
},


{
"title":"Geometry",
"text":
"""
Geometry measures shapes and space.


Area:

Length × Width


Volume:

Length × Width × Height


Why:

Geometry is used for measurements involving
space and objects.
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


Why:

Variables represent unknown measurements
that must be calculated.
"""
},


{
"title":"Graphs and Data",
"text":
"""
Charts and graphs display information.


Important skills:

- Reading trends
- Comparing data
- Understanding changes


Why:

Healthcare workers use graphs to analyze
information quickly.
"""
},


{
"title":"Scientific Notation",
"text":
"""
Scientific notation represents very large
or very small numbers.


Example:

0.0005 = 5 × 10^-4


Why:

Scientific notation makes difficult numbers
easier to read and calculate.
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


Why:

Strong strategies improve performance during
timed HOSA competitions.
"""
},


{
"title":"Advanced HOSA Review",
"text":
"""
Final review combines:


- Medical math
- Statistics
- Algebra
- Conversions


Practice mixed problems and review formulas.


Why:

Combining skills prepares students for advanced
HOSA Medical Math questions.
"""
}

]





# -------------------------
# QUESTIONS
# -------------------------

questions = [

{
    "chapter":"Medical Math Foundations",
    "question":"A patient weighs 176 pounds. What is the weight in kilograms?",
    "answers":["70 kg","75 kg","80 kg","85 kg"],
    "correct":"80 kg",
    "explanation":"176 ÷ 2.2 = 80 kg.",
    "why":"Many medication calculations require weight in kilograms."
},

{
    "chapter":"Medical Math Foundations",
    "question":"How many milligrams are in 2 grams?",
    "answers":["20 mg","200 mg","2000 mg","20000 mg"],
    "correct":"2000 mg",
    "explanation":"1 gram = 1000 mg. 2 × 1000 = 2000 mg.",
    "why":"Metric conversions are important for medication accuracy."
},

{
    "chapter":"Medical Math Foundations",
    "question":"How many milliliters are in 2.5 liters?",
    "answers":["250 mL","2500 mL","25 mL","25000 mL"],
    "correct":"2500 mL",
    "explanation":"1 liter = 1000 mL. 2.5 × 1000 = 2500 mL.",
    "why":"Healthcare workers frequently convert fluid measurements."
},

{
    "chapter":"Medical Math Foundations",
    "question":"A patient weighs 132 pounds. What is the weight in kilograms?",
    "answers":["50 kg","60 kg","70 kg","80 kg"],
    "correct":"60 kg",
    "explanation":"132 ÷ 2.2 = 60 kg.",
    "why":"Correct weight conversions are needed for safe dosing."
},

{
    "chapter":"Dosage",
    "question":"A medication order is 500 mg. Each tablet contains 250 mg. How many tablets are needed?",
    "answers":["1 tablet","2 tablets","3 tablets","4 tablets"],
    "correct":"2 tablets",
    "explanation":"500 ÷ 250 = 2 tablets.",
    "why":"Dosage calculations determine correct medication amounts."
},

{
    "chapter":"Temperature Conversion",
    "question":"Convert 102°F to Celsius.",
    "answers":["35°C","38.9°C","40°C","42°C"],
    "correct":"38.9°C",
    "explanation":"(102 - 32) × 5/9 = 38.9°C.",
    "why":"Healthcare uses temperature conversions between systems."
},

{
    "chapter":"IV Flow Rate",
    "question":"A patient receives 1200 mL over 8 hours. What is the flow rate?",
    "answers":["100 mL/hr","150 mL/hr","200 mL/hr","250 mL/hr"],
    "correct":"150 mL/hr",
    "explanation":"1200 ÷ 8 = 150 mL/hr.",
    "why":"IV calculations control fluid delivery speed."
},

{
    "chapter":"Percentages",
    "question":"A hospital has 200 patients. 25% need additional monitoring. How many patients is this?",
    "answers":["25","50","75","100"],
    "correct":"50",
    "explanation":"200 × 0.25 = 50 patients.",
    "why":"Percentages help analyze medical data."
},

{
    "chapter":"Statistics",
    "question":"Find the average of 40, 50, and 60.",
    "answers":["45","50","55","60"],
    "correct":"50",
    "explanation":"(40 + 50 + 60) ÷ 3 = 50.",
    "why":"Averages summarize groups of data."
},

{
    "chapter":"Volume",
    "question":"A container is 5 cm long, 4 cm wide, and 3 cm tall. What is the volume?",
    "answers":["12 cm³","20 cm³","60 cm³","120 cm³"],
    "correct":"60 cm³",
    "explanation":"Volume = length × width × height.\n5 × 4 × 3 = 60 cm³.",
    "why":"Volume measures the space inside an object."
},

{
    "chapter":"Fractions",
    "question":"What is 3/4 as a decimal?",
    "answers":["0.25","0.50","0.75","1.25"],
    "correct":"0.75",
    "explanation":"3 ÷ 4 = 0.75.",
    "why":"Decimals are commonly used in medical measurements."
},

{
    "chapter":"Ratios",
    "question":"A medication ratio is 200 mg : 4 mL. How many mg are in 1 mL?",
    "answers":["25 mg","50 mg","100 mg","200 mg"],
    "correct":"50 mg",
    "explanation":"200 ÷ 4 = 50 mg/mL.",
    "why":"Ratios help calculate medication concentration."
},

{
    "chapter":"Probability",
    "question":"A patient has a 75% chance of recovery. What decimal represents this?",
    "answers":["0.25","0.50","0.75","1.75"],
    "correct":"0.75",
    "explanation":"75% ÷ 100 = 0.75.",
    "why":"Probability can be represented as decimals."
},

{
    "chapter":"Algebra",
    "question":"Solve: x + 8 = 15",
    "answers":["5","7","8","23"],
    "correct":"7",
    "explanation":"Subtract 8 from both sides. x = 7.",
    "why":"Algebra helps solve unknown medical values."
},

{
    "chapter":"Dosage",
    "question":"A medication contains 20 mg/mL. How many mL are needed for 100 mg?",
    "answers":["2 mL","5 mL","10 mL","20 mL"],
    "correct":"5 mL",
    "explanation":"100 ÷ 20 = 5 mL.",
    "why":"Medication concentration calculations prevent errors."
},

{
    "chapter":"Medical Math Foundations",
    "question":"Convert 4500 mL into liters.",
    "answers":["0.45 L","4.5 L","45 L","450 L"],
    "correct":"4.5 L",
    "explanation":"4500 ÷ 1000 = 4.5 L.",
    "why":"Fluid measurements often require unit conversion."
},

{
    "chapter":"Statistics",
    "question":"What is the median of 10, 20, 30, 40, 50?",
    "answers":["10","20","30","50"],
    "correct":"30",
    "explanation":"The middle number is 30.",
    "why":"Median helps analyze healthcare data."
},

{
    "chapter":"Percentage",
    "question":"A $100 medical item increases by 10%. What is the new price?",
    "answers":["$105","$110","$115","$120"],
    "correct":"$110",
    "explanation":"10% of 100 is 10. 100 + 10 = 110.",
    "why":"Percent changes are used in healthcare costs."
},

{
    "chapter":"IV Flow Rate",
    "question":"A 500 mL IV bag runs at 50 mL/hr. How many hours will it last?",
    "answers":["5 hours","10 hours","15 hours","20 hours"],
    "correct":"10 hours",
    "explanation":"500 ÷ 50 = 10 hours.",
    "why":"IV calculations determine treatment duration."
},
{
    "chapter":"Medical Math Foundations",
    "question":"A patient weighs 242 pounds. Convert the weight to kilograms.",
    "answers":["90 kg","100 kg","110 kg","120 kg"],
    "correct":"110 kg",
    "explanation":"242 ÷ 2.2 = 110 kg.",
    "why":"Weight conversion is required for many medication calculations."
},

{
    "chapter":"Dosage",
    "question":"A patient needs 750 mg of medication. Each tablet contains 250 mg. How many tablets are needed?",
    "answers":["1 tablet","2 tablets","3 tablets","4 tablets"],
    "correct":"3 tablets",
    "explanation":"750 ÷ 250 = 3 tablets.",
    "why":"Dosage calculations ensure the correct amount of medication is given."
},

{
    "chapter":"Percentages",
    "question":"A hospital has 500 gloves. 40% are used. How many gloves are used?",
    "answers":["100","150","200","250"],
    "correct":"200",
    "explanation":"500 × 0.40 = 200 gloves.",
    "why":"Percentages help calculate portions of medical supplies."
},

{
    "chapter":"IV Flow Rate",
    "question":"A patient receives 900 mL of IV fluid in 6 hours. What is the rate?",
    "answers":["100 mL/hr","150 mL/hr","200 mL/hr","250 mL/hr"],
    "correct":"150 mL/hr",
    "explanation":"900 ÷ 6 = 150 mL/hr.",
    "why":"IV rates control how quickly fluids are delivered."
},

{
    "chapter":"Temperature Conversion",
    "question":"Convert 98.6°F to Celsius.",
    "answers":["35°C","37°C","39°C","42°C"],
    "correct":"37°C",
    "explanation":"98.6°F is approximately 37°C.",
    "why":"Healthcare workers convert temperatures between Fahrenheit and Celsius."
},

{
    "chapter":"Statistics",
    "question":"A nurse records patient ages: 20, 30, 40, 50. What is the average age?",
    "answers":["30","35","40","45"],
    "correct":"35",
    "explanation":"(20 + 30 + 40 + 50) ÷ 4 = 35.",
    "why":"Average values summarize patient data."
},

{
    "chapter":"Fractions",
    "question":"What fraction represents 0.5?",
    "answers":["1/4","1/2","3/4","1"],
    "correct":"1/2",
    "explanation":"0.5 equals one-half.",
    "why":"Fractions and decimals represent parts of a whole."
},

{
    "chapter":"Ratios",
    "question":"A solution contains 300 mg in 6 mL. How many mg are in 1 mL?",
    "answers":["25 mg","50 mg","75 mg","100 mg"],
    "correct":"50 mg",
    "explanation":"300 ÷ 6 = 50 mg/mL.",
    "why":"Medication concentration uses ratios."
},

{
    "chapter":"Algebra",
    "question":"Solve: x × 5 = 25",
    "answers":["3","4","5","6"],
    "correct":"5",
    "explanation":"25 ÷ 5 = 5.",
    "why":"Algebra helps find unknown measurements."
},

{
    "chapter":"Geometry",
    "question":"A medical tray is 12 inches long and 5 inches wide. What is the area?",
    "answers":["17 in²","50 in²","60 in²","120 in²"],
    "correct":"60 in²",
    "explanation":"Area = length × width. 12 × 5 = 60 in².",
    "why":"Area calculations measure surfaces and spaces."
},

{
    "chapter":"Medical Math Foundations",
    "question":"How many milligrams are in 5 grams?",
    "answers":["50 mg","500 mg","5000 mg","50000 mg"],
    "correct":"5000 mg",
    "explanation":"5 × 1000 = 5000 mg.",
    "why":"Metric conversions are important for medication measurements."
},

{
    "chapter":"Dosage",
    "question":"A medication order is 1000 mg. Capsules contain 200 mg each. How many capsules are needed?",
    "answers":["3 capsules","4 capsules","5 capsules","6 capsules"],
    "correct":"5 capsules",
    "explanation":"1000 ÷ 200 = 5 capsules.",
    "why":"Correct dosage prevents medication mistakes."
},

{
    "chapter":"Percentages",
    "question":"A clinic has 80 patients. 25% leave early. How many patients leave early?",
    "answers":["10","20","30","40"],
    "correct":"20",
    "explanation":"80 × 0.25 = 20.",
    "why":"Percentages measure parts of a group."
},

{
    "chapter":"IV Flow Rate",
    "question":"A 1000 mL IV bag runs at 125 mL/hr. How long will it last?",
    "answers":["4 hours","6 hours","8 hours","10 hours"],
    "correct":"8 hours",
    "explanation":"1000 ÷ 125 = 8 hours.",
    "why":"IV calculations determine fluid administration time."
},

{
    "chapter":"Probability",
    "question":"A test has 8 possible outcomes and 2 successful outcomes. What is the probability?",
    "answers":["0.10","0.25","0.50","0.75"],
    "correct":"0.25",
    "explanation":"2 ÷ 8 = 0.25.",
    "why":"Probability measures the chance of an event."
},

{
    "chapter":"Statistics",
    "question":"Find the mode: 2, 3, 3, 4, 5.",
    "answers":["2","3","4","5"],
    "correct":"3",
    "explanation":"The mode is the value that appears most often.",
    "why":"Mode identifies the most common value in data."
},

{
    "chapter":"Medical Math Foundations",
    "question":"Convert 0.5 liters into milliliters.",
    "answers":["50 mL","500 mL","5000 mL","5 mL"],
    "correct":"500 mL",
    "explanation":"0.5 × 1000 = 500 mL.",
    "why":"Fluid conversions are common in healthcare."
},

{
    "chapter":"Dosage",
    "question":"A patient receives 4 mL of medication twice daily. How much medication is given each day?",
    "answers":["4 mL","6 mL","8 mL","12 mL"],
    "correct":"8 mL",
    "explanation":"4 × 2 = 8 mL.",
    "why":"Daily dosage calculations determine total medication amount."
},

{
    "chapter":"BMI",
    "question":"A patient weighs 80 kg and is 2 meters tall. Calculate BMI.",
    "answers":["10","20","30","40"],
    "correct":"20",
    "explanation":"BMI = 80 ÷ (2 × 2) = 20.",
    "why":"BMI compares weight and height measurements."
},
{
    "chapter":"Medical Math Foundations",
    "question":"Convert 3 kilograms into grams.",
    "answers":["30 g","300 g","3000 g","30000 g"],
    "correct":"3000 g",
    "explanation":"1 kilogram = 1000 grams. 3 × 1000 = 3000 g.",
    "why":"Metric conversions are used frequently in healthcare."
},

{
    "chapter":"Dosage",
    "question":"A medication order requires 800 mg. Each tablet contains 400 mg. How many tablets are needed?",
    "answers":["1 tablet","2 tablets","3 tablets","4 tablets"],
    "correct":"2 tablets",
    "explanation":"800 ÷ 400 = 2 tablets.",
    "why":"Medication calculations determine the correct dose."
},

{
    "chapter":"Percentages",
    "question":"A hospital has 1000 supplies. 15% are damaged. How many supplies are damaged?",
    "answers":["100","150","200","250"],
    "correct":"150",
    "explanation":"1000 × 0.15 = 150 supplies.",
    "why":"Percentages help track healthcare inventory."
},

{
    "chapter":"IV Flow Rate",
    "question":"A patient receives 2000 mL of fluid over 10 hours. What is the rate?",
    "answers":["100 mL/hr","150 mL/hr","200 mL/hr","250 mL/hr"],
    "correct":"200 mL/hr",
    "explanation":"2000 ÷ 10 = 200 mL/hr.",
    "why":"IV rates control fluid delivery."
},

{
    "chapter":"Temperature Conversion",
    "question":"Convert 104°F to Celsius.",
    "answers":["35°C","40°C","45°C","50°C"],
    "correct":"40°C",
    "explanation":"(104 - 32) × 5/9 = 40°C.",
    "why":"Temperature conversion is important for patient assessment."
},

{
    "chapter":"Statistics",
    "question":"Find the average of 70, 80, and 90.",
    "answers":["75","80","85","90"],
    "correct":"80",
    "explanation":"(70 + 80 + 90) ÷ 3 = 80.",
    "why":"Averages summarize groups of measurements."
},

{
    "chapter":"Fractions",
    "question":"What is 1/4 as a decimal?",
    "answers":["0.20","0.25","0.50","0.75"],
    "correct":"0.25",
    "explanation":"1 ÷ 4 = 0.25.",
    "why":"Decimals are used when measuring medication amounts."
},

{
    "chapter":"Ratios",
    "question":"A medication contains 600 mg in 12 mL. What is the concentration?",
    "answers":["25 mg/mL","50 mg/mL","75 mg/mL","100 mg/mL"],
    "correct":"50 mg/mL",
    "explanation":"600 ÷ 12 = 50 mg/mL.",
    "why":"Concentration calculations determine medication strength."
},

{
    "chapter":"Algebra",
    "question":"Solve: x - 12 = 20",
    "answers":["8","20","32","40"],
    "correct":"32",
    "explanation":"Add 12 to both sides. x = 32.",
    "why":"Algebra helps find missing healthcare values."
},

{
    "chapter":"Geometry",
    "question":"A room is 10 meters long and 6 meters wide. What is the area?",
    "answers":["16 m²","40 m²","60 m²","100 m²"],
    "correct":"60 m²",
    "explanation":"Area = length × width. 10 × 6 = 60 m².",
    "why":"Area measures the size of a space."
},

{
    "chapter":"Medical Math Foundations",
    "question":"How many milliliters are in 4 liters?",
    "answers":["40 mL","400 mL","4000 mL","40000 mL"],
    "correct":"4000 mL",
    "explanation":"4 × 1000 = 4000 mL.",
    "why":"Fluid measurements must often be converted."
},

{
    "chapter":"Dosage",
    "question":"A patient needs 250 mg. The medication concentration is 50 mg/mL. How many mL are needed?",
    "answers":["2 mL","5 mL","10 mL","15 mL"],
    "correct":"5 mL",
    "explanation":"250 ÷ 50 = 5 mL.",
    "why":"Medication volume depends on concentration."
},

{
    "chapter":"Percentages",
    "question":"A patient's oxygen level changes from 90% to 95%. What is the increase?",
    "answers":["3%","5%","7%","10%"],
    "correct":"5%",
    "explanation":"95 - 90 = 5%.",
    "why":"Changes in patient measurements are calculated using differences."
},

{
    "chapter":"IV Flow Rate",
    "question":"A 750 mL IV bag runs at 75 mL/hr. How long will it last?",
    "answers":["5 hours","8 hours","10 hours","12 hours"],
    "correct":"10 hours",
    "explanation":"750 ÷ 75 = 10 hours.",
    "why":"IV calculations determine treatment duration."
},

{
    "chapter":"Probability",
    "question":"A medication works successfully 9 out of 10 times. What is the probability?",
    "answers":["0.09","0.50","0.90","1.00"],
    "correct":"0.90",
    "explanation":"9 ÷ 10 = 0.90.",
    "why":"Probability represents likelihood."
},

{
    "chapter":"Statistics",
    "question":"Find the median: 5, 10, 15, 20, 25.",
    "answers":["5","10","15","25"],
    "correct":"15",
    "explanation":"The middle number is 15.",
    "why":"Median helps analyze healthcare data sets."
},

{
    "chapter":"Medical Math Foundations",
    "question":"Convert 2500 mg into grams.",
    "answers":["0.25 g","2.5 g","25 g","250 g"],
    "correct":"2.5 g",
    "explanation":"2500 ÷ 1000 = 2.5 g.",
    "why":"Medication units must be converted accurately."
},

{
    "chapter":"Dosage",
    "question":"A patient takes 2 tablets three times per day. How many tablets are taken daily?",
    "answers":["3 tablets","4 tablets","6 tablets","8 tablets"],
    "correct":"6 tablets",
    "explanation":"2 × 3 = 6 tablets.",
    "why":"Daily medication totals help prevent errors."
},

{
    "chapter":"BMI",
    "question":"A patient weighs 90 kg and is 1.5 meters tall. Calculate BMI.",
    "answers":["20","30","40","50"],
    "correct":"40",
    "explanation":"90 ÷ (1.5 × 1.5) = 40.",
    "why":"BMI compares weight and height."
},

{
    "chapter":"Graphs and Data",
    "question":"A chart shows patients increasing from 50 to 75. What is the increase?",
    "answers":["15","20","25","30"],
    "correct":"25",
    "explanation":"75 - 50 = 25.",
    "why":"Healthcare workers analyze changes in data trends."
},
{
    "chapter":"Medical Math Foundations",
    "question":"Convert 5.5 kilograms into grams.",
    "answers":["55 g","550 g","5500 g","55000 g"],
    "correct":"5500 g",
    "explanation":"1 kg = 1000 g. 5.5 × 1000 = 5500 g.",
    "why":"Metric conversions are necessary for accurate healthcare measurements."
},

{
    "chapter":"Dosage",
    "question":"A medication order requires 1200 mg. Each capsule contains 300 mg. How many capsules are needed?",
    "answers":["2 capsules","3 capsules","4 capsules","5 capsules"],
    "correct":"4 capsules",
    "explanation":"1200 ÷ 300 = 4 capsules.",
    "why":"Dosage calculations determine the correct medication amount."
},

{
    "chapter":"Percentages",
    "question":"A hospital has 800 masks. 25% are used. How many masks are used?",
    "answers":["100","150","200","250"],
    "correct":"200",
    "explanation":"800 × 0.25 = 200 masks.",
    "why":"Percent calculations are used for supply tracking."
},

{
    "chapter":"IV Flow Rate",
    "question":"A patient receives 1500 mL over 12 hours. What is the flow rate?",
    "answers":["100 mL/hr","125 mL/hr","150 mL/hr","200 mL/hr"],
    "correct":"125 mL/hr",
    "explanation":"1500 ÷ 12 = 125 mL/hr.",
    "why":"IV calculations determine how fast fluids are delivered."
},

{
    "chapter":"Temperature Conversion",
    "question":"Convert 86°F to Celsius.",
    "answers":["20°C","25°C","30°C","35°C"],
    "correct":"30°C",
    "explanation":"(86 - 32) × 5/9 = 30°C.",
    "why":"Healthcare uses both Fahrenheit and Celsius."
},

{
    "chapter":"Statistics",
    "question":"Find the average of 65, 70, 75, and 80.",
    "answers":["70","72.5","75","80"],
    "correct":"72.5",
    "explanation":"(65 + 70 + 75 + 80) ÷ 4 = 72.5.",
    "why":"Average values summarize patient information."
},

{
    "chapter":"Fractions",
    "question":"What is 2/5 as a decimal?",
    "answers":["0.20","0.40","0.50","0.75"],
    "correct":"0.40",
    "explanation":"2 ÷ 5 = 0.40.",
    "why":"Fractions are often converted into decimals in calculations."
},

{
    "chapter":"Ratios",
    "question":"A solution contains 400 mg in 8 mL. What is the concentration?",
    "answers":["25 mg/mL","50 mg/mL","75 mg/mL","100 mg/mL"],
    "correct":"50 mg/mL",
    "explanation":"400 ÷ 8 = 50 mg/mL.",
    "why":"Concentration calculations are important for medications."
},

{
    "chapter":"Algebra",
    "question":"Solve: 3x = 21",
    "answers":["5","6","7","8"],
    "correct":"7",
    "explanation":"21 ÷ 3 = 7.",
    "why":"Algebra helps solve unknown measurements."
},

{
    "chapter":"Geometry",
    "question":"A rectangle has a length of 15 cm and width of 4 cm. What is the area?",
    "answers":["19 cm²","40 cm²","60 cm²","75 cm²"],
    "correct":"60 cm²",
    "explanation":"15 × 4 = 60 cm².",
    "why":"Area calculations measure two-dimensional space."
},

{
    "chapter":"Medical Math Foundations",
    "question":"Convert 7500 mL into liters.",
    "answers":["0.75 L","7.5 L","75 L","750 L"],
    "correct":"7.5 L",
    "explanation":"7500 ÷ 1000 = 7.5 L.",
    "why":"Fluid conversions are common in healthcare."
},

{
    "chapter":"Dosage",
    "question":"A medication concentration is 10 mg/mL. How many mL are needed for 500 mg?",
    "answers":["25 mL","50 mL","75 mL","100 mL"],
    "correct":"50 mL",
    "explanation":"500 ÷ 10 = 50 mL.",
    "why":"Medication concentration determines volume needed."
},

{
    "chapter":"Percentages",
    "question":"A patient's heart rate decreases from 100 bpm to 80 bpm. What is the decrease?",
    "answers":["10 bpm","20 bpm","30 bpm","40 bpm"],
    "correct":"20 bpm",
    "explanation":"100 - 80 = 20 bpm.",
    "why":"Healthcare workers monitor changes in vital signs."
},

{
    "chapter":"IV Flow Rate",
    "question":"A 2400 mL IV order is given over 24 hours. What is the hourly rate?",
    "answers":["50 mL/hr","100 mL/hr","150 mL/hr","200 mL/hr"],
    "correct":"100 mL/hr",
    "explanation":"2400 ÷ 24 = 100 mL/hr.",
    "why":"IV formulas calculate safe fluid delivery."
},

{
    "chapter":"Probability",
    "question":"A patient test has 3 successful results out of 4 trials. What is the probability?",
    "answers":["0.25","0.50","0.75","1.25"],
    "correct":"0.75",
    "explanation":"3 ÷ 4 = 0.75.",
    "why":"Probability measures chances using numbers."
},

{
    "chapter":"Statistics",
    "question":"Find the mode: 10, 15, 15, 20, 25.",
    "answers":["10","15","20","25"],
    "correct":"15",
    "explanation":"15 appears more than any other number.",
    "why":"Mode identifies the most common value."
},

{
    "chapter":"Medical Math Foundations",
    "question":"Convert 0.25 kilograms into grams.",
    "answers":["25 g","250 g","2500 g","0.25 g"],
    "correct":"250 g",
    "explanation":"0.25 × 1000 = 250 g.",
    "why":"Small metric conversions are common in medical math."
},

{
    "chapter":"Dosage",
    "question":"A patient receives 15 mL of medication per day for 5 days. How much medication is needed?",
    "answers":["50 mL","75 mL","100 mL","150 mL"],
    "correct":"75 mL",
    "explanation":"15 × 5 = 75 mL.",
    "why":"Total dosage calculations help plan medication supplies."
},

{
    "chapter":"BMI",
    "question":"A patient weighs 72 kg and is 1.8 meters tall. Calculate BMI.",
    "answers":["18.2","22.2","25.5","30.0"],
    "correct":"22.2",
    "explanation":"72 ÷ (1.8 × 1.8) = 22.2.",
    "why":"BMI compares weight and height."
},

{
    "chapter":"Graphs and Data",
    "question":"A hospital records 120 patients Monday and 150 Tuesday. How many more patients were seen Tuesday?",
    "answers":["20","25","30","35"],
    "correct":"30",
    "explanation":"150 - 120 = 30.",
    "why":"Data comparisons help identify healthcare trends."
},
{
    "chapter":"Medical Math Foundations",
    "question":"Convert 6.2 liters into milliliters.",
    "answers":["62 mL","620 mL","6200 mL","62000 mL"],
    "correct":"6200 mL",
    "explanation":"1 liter = 1000 mL. 6.2 × 1000 = 6200 mL.",
    "why":"Fluid measurements must often be converted in healthcare."
},

{
    "chapter":"Dosage",
    "question":"A patient needs 900 mg of medication. Each tablet contains 150 mg. How many tablets are needed?",
    "answers":["3 tablets","5 tablets","6 tablets","9 tablets"],
    "correct":"6 tablets",
    "explanation":"900 ÷ 150 = 6 tablets.",
    "why":"Dosage calculations help provide accurate medication amounts."
},

{
    "chapter":"Percentages",
    "question":"A clinic has 400 patients. 30% require follow-up visits. How many patients require follow-up?",
    "answers":["80","100","120","150"],
    "correct":"120",
    "explanation":"400 × 0.30 = 120 patients.",
    "why":"Percentages are used to analyze patient populations."
},

{
    "chapter":"IV Flow Rate",
    "question":"A patient receives 1800 mL over 9 hours. What is the flow rate?",
    "answers":["100 mL/hr","150 mL/hr","200 mL/hr","250 mL/hr"],
    "correct":"200 mL/hr",
    "explanation":"1800 ÷ 9 = 200 mL/hr.",
    "why":"IV calculations control fluid administration."
},

{
    "chapter":"Temperature Conversion",
    "question":"Convert 95°F to Celsius.",
    "answers":["25°C","30°C","35°C","40°C"],
    "correct":"35°C",
    "explanation":"(95 - 32) × 5/9 = 35°C.",
    "why":"Temperature conversion is used when reading medical equipment."
},

{
    "chapter":"Statistics",
    "question":"Find the average of 90, 85, and 95.",
    "answers":["85","90","92","95"],
    "correct":"90",
    "explanation":"(90 + 85 + 95) ÷ 3 = 90.",
    "why":"Average values help summarize healthcare measurements."
},

{
    "chapter":"Fractions",
    "question":"What is 3/5 as a decimal?",
    "answers":["0.30","0.50","0.60","0.80"],
    "correct":"0.60",
    "explanation":"3 ÷ 5 = 0.60.",
    "why":"Decimals allow precise medical calculations."
},

{
    "chapter":"Ratios",
    "question":"A medication contains 800 mg in 16 mL. What is the concentration?",
    "answers":["25 mg/mL","40 mg/mL","50 mg/mL","80 mg/mL"],
    "correct":"50 mg/mL",
    "explanation":"800 ÷ 16 = 50 mg/mL.",
    "why":"Medication strength is determined using ratios."
},

{
    "chapter":"Algebra",
    "question":"Solve: x ÷ 4 = 8",
    "answers":["16","24","32","40"],
    "correct":"32",
    "explanation":"8 × 4 = 32.",
    "why":"Algebra helps solve unknown values."
},

{
    "chapter":"Geometry",
    "question":"A storage box is 8 cm long, 5 cm wide, and 4 cm tall. What is the volume?",
    "answers":["80 cm³","120 cm³","160 cm³","200 cm³"],
    "correct":"160 cm³",
    "explanation":"8 × 5 × 4 = 160 cm³.",
    "why":"Volume measures the amount of space inside an object."
},

{
    "chapter":"Medical Math Foundations",
    "question":"Convert 3500 mg into grams.",
    "answers":["0.35 g","3.5 g","35 g","350 g"],
    "correct":"3.5 g",
    "explanation":"3500 ÷ 1000 = 3.5 g.",
    "why":"Medication units frequently require conversion."
},

{
    "chapter":"Dosage",
    "question":"A medication order is 2 grams. How many milligrams is this?",
    "answers":["200 mg","500 mg","1000 mg","2000 mg"],
    "correct":"2000 mg",
    "explanation":"2 × 1000 = 2000 mg.",
    "why":"Healthcare uses both grams and milligrams."
},

{
    "chapter":"Percentages",
    "question":"A medical bill is $500. Insurance covers 70%. How much does insurance pay?",
    "answers":["$250","$300","$350","$400"],
    "correct":"$350",
    "explanation":"500 × 0.70 = $350.",
    "why":"Percent calculations are used in healthcare costs."
},

{
    "chapter":"IV Flow Rate",
    "question":"A 1000 mL IV bag runs at 250 mL/hr. How long will it last?",
    "answers":["2 hours","4 hours","6 hours","8 hours"],
    "correct":"4 hours",
    "explanation":"1000 ÷ 250 = 4 hours.",
    "why":"IV formulas determine treatment duration."
},

{
    "chapter":"Probability",
    "question":"A treatment works 18 times out of 20 trials. What is the probability?",
    "answers":["0.50","0.75","0.90","1.20"],
    "correct":"0.90",
    "explanation":"18 ÷ 20 = 0.90.",
    "why":"Probability measures likelihood of outcomes."
},

{
    "chapter":"Statistics",
    "question":"Find the median: 12, 18, 25, 30, 35.",
    "answers":["12","18","25","35"],
    "correct":"25",
    "explanation":"The middle value is 25.",
    "why":"Median helps organize and interpret data."
},

{
    "chapter":"Medical Math Foundations",
    "question":"How many centimeters are in 3 meters?",
    "answers":["30 cm","100 cm","300 cm","3000 cm"],
    "correct":"300 cm",
    "explanation":"1 meter = 100 centimeters. 3 × 100 = 300 cm.",
    "why":"Metric measurements are used in healthcare."
},

{
    "chapter":"Dosage",
    "question":"A medication contains 25 mg/mL. How many mL are needed for 250 mg?",
    "answers":["5 mL","10 mL","15 mL","20 mL"],
    "correct":"10 mL",
    "explanation":"250 ÷ 25 = 10 mL.",
    "why":"Medication concentration determines the correct volume."
},

{
    "chapter":"BMI",
    "question":"A patient weighs 100 kg and is 2 meters tall. Calculate BMI.",
    "answers":["20","25","30","50"],
    "correct":"25",
    "explanation":"100 ÷ (2 × 2) = 25.",
    "why":"BMI calculations compare weight and height."
},

{
    "chapter":"Graphs and Data",
    "question":"A chart shows patient visits increasing from 200 to 260. What is the increase?",
    "answers":["40","50","60","70"],
    "correct":"60",
    "explanation":"260 - 200 = 60.",
    "why":"Healthcare w{
    "chapter":"Medical Math Foundations",
    "question":"Convert 8.5 kilograms into grams.",
    "answers":["85 g","850 g","8500 g","85000 g"],
    "correct":"8500 g",
    "explanation":"1 kilogram = 1000 grams. 8.5 × 1000 = 8500 g.",
    "why":"Metric conversions are used frequently in healthcare."
},

{
    "chapter":"Dosage",
    "question":"A patient needs 1500 mg of medication. Each capsule contains 300 mg. How many capsules are needed?",
    "answers":["3 capsules","4 capsules","5 capsules","6 capsules"],
    "correct":"5 capsules",
    "explanation":"1500 ÷ 300 = 5 capsules.",
    "why":"Accurate dosage calculations prevent medication errors."
},

{
    "chapter":"Percentages",
    "question":"A hospital has 600 patients. 20% need additional testing. How many patients need testing?",
    "answers":["60","100","120","150"],
    "correct":"120",
    "explanation":"600 × 0.20 = 120 patients.",
    "why":"Percentages help analyze healthcare data."
},

{
    "chapter":"IV Flow Rate",
    "question":"A patient receives 2400 mL over 12 hours. What is the IV rate?",
    "answers":["100 mL/hr","150 mL/hr","200 mL/hr","250 mL/hr"],
    "correct":"200 mL/hr",
    "explanation":"2400 ÷ 12 = 200 mL/hr.",
    "why":"IV calculations determine fluid delivery speed."
},

{
    "chapter":"Temperature Conversion",
    "question":"Convert 77°F to Celsius.",
    "answers":["20°C","25°C","30°C","35°C"],
    "correct":"25°C",
    "explanation":"(77 - 32) × 5/9 = 25°C.",
    "why":"Medical equipment may display different temperature scales."
},

{
    "chapter":"Statistics",
    "question":"Find the average of 100, 90, and 80.",
    "answers":["85","90","95","100"],
    "correct":"90",
    "explanation":"(100 + 90 + 80) ÷ 3 = 90.",
    "why":"Averages summarize groups of measurements."
},

{
    "chapter":"Fractions",
    "question":"What is 4/5 as a decimal?",
    "answers":["0.40","0.60","0.80","1.20"],
    "correct":"0.80",
    "explanation":"4 ÷ 5 = 0.80.",
    "why":"Decimals are used for accurate medical measurements."
},

{
    "chapter":"Ratios",
    "question":"A solution contains 1000 mg in 20 mL. What is the concentration?",
    "answers":["25 mg/mL","50 mg/mL","75 mg/mL","100 mg/mL"],
    "correct":"50 mg/mL",
    "explanation":"1000 ÷ 20 = 50 mg/mL.",
    "why":"Medication concentration calculations use ratios."
},

{
    "chapter":"Algebra",
    "question":"Solve: x + 25 = 50",
    "answers":["15","20","25","30"],
    "correct":"25",
    "explanation":"50 - 25 = 25.",
    "why":"Algebra finds unknown values in calculations."
},

{
    "chapter":"Geometry",
    "question":"A medical room is 20 feet long and 10 feet wide. What is the area?",
    "answers":["100 ft²","200 ft²","300 ft²","400 ft²"],
    "correct":"200 ft²",
    "explanation":"20 × 10 = 200 ft².",
    "why":"Area measures the size of a space."
},

{
    "chapter":"Medical Math Foundations",
    "question":"Convert 9000 mL into liters.",
    "answers":["0.9 L","9 L","90 L","900 L"],
    "correct":"9 L",
    "explanation":"9000 ÷ 1000 = 9 L.",
    "why":"Fluid conversions are common in patient care."
},

{
    "chapter":"Dosage",
    "question":"A patient receives 75 mg of medication. The concentration is 15 mg/mL. How many mL are needed?",
    "answers":["3 mL","5 mL","7 mL","10 mL"],
    "correct":"5 mL",
    "explanation":"75 ÷ 15 = 5 mL.",
    "why":"Medication volume depends on the concentration."
},

{
    "chapter":"Percentages",
    "question":"A clinic has 300 appointments. 10% are canceled. How many remain?",
    "answers":["250","270","280","290"],
    "correct":"270",
    "explanation":"10% of 300 is 30. 300 - 30 = 270.",
    "why":"Percent changes are used for scheduling and reports."
},

{
    "chapter":"IV Flow Rate",
    "question":"A 500 mL IV bag runs at 100 mL/hr. How long will it last?",
    "answers":["3 hours","5 hours","7 hours","10 hours"],
    "correct":"5 hours",
    "explanation":"500 ÷ 100 = 5 hours.",
    "why":"IV calculations determine infusion time."
},

{
    "chapter":"Probability",
    "question":"A patient improves in 16 out of 20 cases. What is the probability?",
    "answers":["0.40","0.60","0.80","1.20"],
    "correct":"0.80",
    "explanation":"16 ÷ 20 = 0.80.",
    "why":"Probability measures chances using data."
},

{
    "chapter":"Statistics",
    "question":"Find the mode: 5, 10, 10, 15, 20.",
    "answers":["5","10","15","20"],
    "correct":"10",
    "explanation":"10 appears the most times.",
    "why":"Mode identifies the most common value."
},

{
    "chapter":"Medical Math Foundations",
    "question":"How many milligrams are in 0.75 grams?",
    "answers":["75 mg","750 mg","7500 mg","7.5 mg"],
    "correct":"750 mg",
    "explanation":"0.75 × 1000 = 750 mg.",
    "why":"Medication measurements require accurate conversions."
},

{
    "chapter":"Dosage",
    "question":"A patient takes 10 mL twice daily for 14 days. How much medication is needed?",
    "answers":["140 mL","200 mL","280 mL","300 mL"],
    "correct":"280 mL",
    "explanation":"10 × 2 × 14 = 280 mL.",
    "why":"Total medication amounts help manage supplies."
},

{
    "chapter":"BMI",
    "question":"A patient weighs 60 kg and is 1.5 meters tall. Calculate BMI.",
    "answers":["20","26.7","30","40"],
    "correct":"26.7",
    "explanation":"60 ÷ (1.5 × 1.5) = 26.7.",
    "why":"BMI compares weight and height measurements."
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

        a = request.form.get("value1")
        b = request.form.get("value2")
        c = request.form.get("value3")


        try:

            a = float(a) if a else 0
            b = float(b) if b else 0
            c = float(c) if c else 0


            if id == 1:

                result = round(a/2.2,2)

                explanation = f"""
Step 1:
Take the pounds value: {a}

Step 2:
Divide by 2.2

{a} ÷ 2.2 = {result} kg

Why:
Healthcare uses kilograms for accurate measurements.
"""


            elif id == 2:

                result = a+b

                explanation = """
Step:
Add the values together.

Why:
Fractions represent parts of a whole.
"""


            elif id == 3:

                result = a*(b/100)

                explanation = f"""
Step:
Convert percentage into decimal form.

{b}% = {b}/100

Then multiply:

{a} × {b/100}

Why:
Percent means parts per 100.
"""


            elif id == 4:

                result = a/b

                explanation = """
Formula:

First Value ÷ Second Value

Why:
Ratios compare quantities.
"""


            elif id == 5:

                result = a*b

                explanation = """
Formula:

Multiply known values.

Why:
Proportions keep relationships equal.
"""


            elif id == 6:

                result = (a/b)*c

                explanation = f"""
Formula:

Desired Dose ÷ Available Dose × Quantity


{a} ÷ {b} × {c}

= {result} mL


Why:

This calculates the correct medication volume.
"""


            elif id == 7:

                result = a/b

                explanation = f"""
Formula:

Volume ÷ Time


{a} ÷ {b}

= {result} mL/hr


Why:

This determines IV fluid delivery speed.
"""


            elif id == 8:

                result = (a+b)/2

                explanation = """
Formula:

(Total values) ÷ Number of values

Why:
Average finds the center value.
"""


            elif id == 9:

                result = a/b

                explanation = """
Formula:

Successful Outcomes ÷ Total Outcomes

Why:
Probability measures chance.
"""


            elif id == 10:

                result = a*b

                explanation = """
Formula:

Length × Width

Why:
Area measures space inside a shape.
"""


            elif id == 11:

                result = a*b

                explanation = """
Formula:

Length × Width × Height

Why:
Volume measures space an object contains.
"""


            elif id == 12:

                result = a-b

                explanation = """
Step:

Use algebra rules to find the unknown.

Why:
Equations solve missing values.
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
