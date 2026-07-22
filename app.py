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
{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 154 pounds. What is the weight in kilograms?",
"answers":["60 kg","65 kg","70 kg","75 kg"],
"correct":"70 kg",
"explanation":"Convert pounds to kilograms by dividing by 2.2.\n154 ÷ 2.2 = 70 kg.",
"why":"Healthcare professionals commonly use kilograms when calculating medication dosages."
},

{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 220 pounds. What is the weight in kilograms?",
"answers":["90 kg","95 kg","100 kg","105 kg"],
"correct":"100 kg",
"explanation":"220 ÷ 2.2 = 100 kg.",
"why":"Weight conversions are used for dosage calculations."
},

{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 132 pounds. What is the weight in kilograms?",
"answers":["55 kg","60 kg","65 kg","70 kg"],
"correct":"60 kg",
"explanation":"132 ÷ 2.2 = 60 kg.",
"why":"Always convert pounds into kilograms before using mg/kg formulas."
},

{
"chapter":"Medical Math Foundations",
"question":"Which unit is commonly used for patient body weight in medication calculations?",
"answers":["Kilograms","Miles","Liters","Inches"],
"correct":"Kilograms",
"explanation":"Medication dosing formulas usually require kilograms.",
"why":"Using the correct unit prevents dosage errors."
},

{
"chapter":"Medical Math Foundations",
"question":"How many grams are in 1000 milligrams?",
"answers":["10","100","1000","1"],
"correct":"1",
"explanation":"1000 mg = 1 g.",
"why":"Metric conversions are essential in healthcare."
},

{
"chapter":"Medical Math Foundations",
"question":"How many milliliters are in one liter?",
"answers":["10","100","1000","10000"],
"correct":"1000",
"explanation":"1 L = 1000 mL.",
"why":"Fluid measurements are often converted in medicine."
},

{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 198 pounds. What is the weight in kilograms?",
"answers":["80 kg","85 kg","90 kg","95 kg"],
"correct":"90 kg",
"explanation":"198 ÷ 2.2 = 90 kg.",
"why":"Kilograms are the standard weight unit in healthcare."
},

{
"chapter":"Medical Math Foundations",
"question":"Which conversion is correct?",
"answers":["1 kg = 2.2 lb","1 lb = 2.2 kg","1 kg = 10 lb","1 lb = 5 kg"],
"correct":"1 kg = 2.2 lb",
"explanation":"One kilogram equals approximately 2.2 pounds.",
"why":"Knowing common conversions improves calculation speed."
},

{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 110 pounds. What is the weight in kilograms?",
"answers":["45 kg","50 kg","55 kg","60 kg"],
"correct":"50 kg",
"explanation":"110 ÷ 2.2 = 50 kg.",
"why":"Weight conversions are one of the most common HOSA Medical Math questions."
},

{
"chapter":"Medical Math Foundations",
"question":"Why is accurate unit conversion important in healthcare?",
"answers":[
"To prevent medication errors",
"To make numbers larger",
"To save computer memory",
"To increase patient age"
],
"correct":"To prevent medication errors",
"explanation":"Incorrect unit conversions can lead to incorrect dosages.",
"why":"Patient safety depends on accurate mathematical calculations."
},
]
{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 176 pounds. What is the weight in kilograms?",
"answers":["70 kg","75 kg","80 kg","85 kg"],
"correct":"80 kg",
"explanation":"Convert pounds to kilograms by dividing by 2.2.\n176 ÷ 2.2 = 80 kg.",
"why":"Many medication dosages are calculated using kilograms."
},

{
"chapter":"Medical Math Foundations",
"question":"How many milligrams are in 2 grams?",
"answers":["20 mg","200 mg","2,000 mg","20,000 mg"],
"correct":"2,000 mg",
"explanation":"Multiply grams by 1,000.\n2 × 1,000 = 2,000 mg.",
"why":"Medication labels commonly switch between grams and milligrams."
},

{
"chapter":"Medical Math Foundations",
"question":"How many liters are equal to 2,500 mL?",
"answers":["0.25 L","2.5 L","25 L","250 L"],
"correct":"2.5 L",
"explanation":"Divide milliliters by 1,000.\n2500 ÷ 1000 = 2.5 L.",
"why":"Fluid conversions are common in IV therapy."
},

{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 88 pounds. What is the weight in kilograms?",
"answers":["35 kg","40 kg","45 kg","50 kg"],
"correct":"40 kg",
"explanation":"88 ÷ 2.2 = 40 kg.",
"why":"Weight-based calculations require kilograms."
},

{
"chapter":"Medical Math Foundations",
"question":"Which measurement is larger?",
"answers":["500 mg","1 g","They are equal","100 mg"],
"correct":"1 g",
"explanation":"1 gram = 1000 milligrams, so 1 g is greater than 500 mg.",
"why":"Understanding metric units helps prevent dosage errors."
},

{
"chapter":"Medical Math Foundations",
"question":"How many centimeters are in 1 meter?",
"answers":["10","100","1,000","10,000"],
"correct":"100",
"explanation":"1 meter = 100 centimeters.",
"why":"Metric length conversions appear in healthcare measurements."
},

{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 242 pounds. What is the weight in kilograms?",
"answers":["100 kg","105 kg","110 kg","115 kg"],
"correct":"110 kg",
"explanation":"242 ÷ 2.2 = 110 kg.",
"why":"Always convert pounds to kilograms before dosage calculations."
},

{
"chapter":"Medical Math Foundations",
"question":"How many milliliters are in 0.75 liters?",
"answers":["75 mL","750 mL","7,500 mL","0.75 mL"],
"correct":"750 mL",
"explanation":"0.75 × 1000 = 750 mL.",
"why":"Healthcare professionals frequently convert liters to milliliters."
},

{
"chapter":"Medical Math Foundations",
"question":"Which unit is commonly used to measure medication mass?",
"answers":["Milligrams","Miles","Gallons","Yards"],
"correct":"Milligrams",
"explanation":"Many medications are measured in milligrams (mg).",
"why":"Correct units are essential for patient safety."
},

{
"chapter":"Medical Math Foundations",
"question":"A patient weighs 66 pounds. What is the weight in kilograms?",
"answers":["25 kg","30 kg","35 kg","40 kg"],
"correct":"30 kg",
"explanation":"66 ÷ 2.2 = 30 kg.",
"why":"Weight conversion is one of the most common HOSA Medical Math skills."
},
    {
        "question": "A patient weighs 154 pounds. Convert the weight to kilograms. (1 kg = 2.2 lb)",
        "choices": ["50 kg", "60 kg", "70 kg", "80 kg"],
        "answer": "70 kg",
        "explanation": "Divide pounds by 2.2. 154 ÷ 2.2 = 70 kg."
    },

    {
        "question": "A medication is ordered at 500 mg. Tablets contain 250 mg each. How many tablets are needed?",
        "choices": ["1 tablet", "2 tablets", "3 tablets", "4 tablets"],
        "answer": "2 tablets",
        "explanation": "500 mg ÷ 250 mg per tablet = 2 tablets."
    },

    {
        "question": "Convert 102°F to Celsius. Formula: °C = (°F − 32) × 5/9",
        "choices": ["35°C", "38.9°C", "40°C", "42°C"],
        "answer": "38.9°C",
        "explanation": "(102 − 32) × 5/9 = 38.9°C."
    },

    {
        "question": "A syringe contains 3 mL of medication. Each mL contains 20 mg. How many mg are present?",
        "choices": ["20 mg", "40 mg", "60 mg", "80 mg"],
        "answer": "60 mg",
        "explanation": "3 mL × 20 mg = 60 mg."
    },

    {
        "question": "A solution contains 15 g of medication in 300 mL. What is the concentration?",
        "choices": ["0.05 g/mL", "0.5 g/mL", "5 g/mL", "20 g/mL"],
        "answer": "0.05 g/mL",
        "explanation": "15 ÷ 300 = 0.05 g/mL."
    },

    {
        "question": "A patient drinks 8 ounces of water every hour for 6 hours. How many ounces total?",
        "choices": ["14 oz", "24 oz", "48 oz", "64 oz"],
        "answer": "48 oz",
        "explanation": "8 × 6 = 48 ounces."
    },

    {
        "question": "A hospital room has 12 beds. 75% are occupied. How many beds are occupied?",
        "choices": ["6", "8", "9", "10"],
        "answer": "9",
        "explanation": "12 × 0.75 = 9 beds."
    },

    {
        "question": "A heart rate changes from 80 bpm to 100 bpm. What is the percent increase?",
        "choices": ["10%", "20%", "25%", "30%"],
        "answer": "25%",
        "explanation": "(100-80) ÷ 80 × 100 = 25%."
    },

    {
        "question": "Temperatures are 98°F, 99°F, 100°F, 101°F. What is the average?",
        "choices": ["98°F", "99°F", "99.5°F", "100°F"],
        "answer": "99.5°F",
        "explanation": "Add values and divide by 4: 398 ÷ 4 = 99.5."
    },

    {
        "question": "A medication costs $80. A hospital receives a 15% discount. What is the final cost?",
        "choices": ["$65", "$68", "$72", "$75"],
        "answer": "$68",
        "explanation": "15% of $80 is $12. $80-$12=$68."
    },
    {
        "question": "Convert 2.5 liters into milliliters.",
        "choices": ["25 mL", "250 mL", "2500 mL", "25000 mL"],
        "answer": "2500 mL",
        "explanation": "1 liter equals 1000 mL. 2.5 × 1000 = 2500 mL."
    },

    {
        "question": "A patient needs 1200 mL of fluid over 8 hours. How many mL per hour?",
        "choices": ["100 mL/hr", "150 mL/hr", "200 mL/hr", "250 mL/hr"],
        "answer": "150 mL/hr",
        "explanation": "1200 mL ÷ 8 hours = 150 mL/hr."
    },

    {
        "question": "A dosage requires 0.75 mg. Which fraction is equivalent?",
        "choices": ["1/4 mg", "1/2 mg", "3/4 mg", "4/5 mg"],
        "answer": "3/4 mg",
        "explanation": "0.75 written as a fraction is 75/100, simplified to 3/4."
    },

    {
        "question": "A patient's blood pressure is 120/80. What does the top number represent?",
        "choices": ["Pulse rate", "Systolic pressure", "Diastolic pressure", "Oxygen level"],
        "answer": "Systolic pressure",
        "explanation": "The top number in blood pressure is systolic pressure."
    },

    {
        "question": "A clinic sees 40 patients per day. How many patients are seen in 5 days?",
        "choices": ["100", "150", "200", "250"],
        "answer": "200",
        "explanation": "40 patients × 5 days = 200 patients."
    },

    {
        "question": "A medication bottle contains 100 mL. If 20 mL is used each day, how many days will it last?",
        "choices": ["2 days", "4 days", "5 days", "10 days"],
        "answer": "5 days",
        "explanation": "100 mL ÷ 20 mL per day = 5 days."
    },

    {
        "question": "A patient's oxygen level is 96%. It drops by 5%. What is the new oxygen level?",
        "choices": ["91%", "92%", "93%", "94%"],
        "answer": "91%",
        "explanation": "96% - 5% = 91%."
    },

    {
        "question": "A nurse works a 12-hour shift and takes three 20-minute breaks. How much working time remains?",
        "choices": ["10 hours", "11 hours", "11.5 hours", "12 hours"],
        "answer": "11 hours",
        "explanation": "Three 20-minute breaks = 60 minutes = 1 hour. 12 - 1 = 11 hours."
    },

    {
        "question": "A patient weighs 70 kg and is 1.75 m tall. Calculate BMI. Formula: BMI = weight ÷ height²",
        "choices": ["18.9", "22.9", "25.5", "30.0"],
        "answer": "22.9",
        "explanation": "70 ÷ (1.75 × 1.75) = 22.9 BMI."
    },

    {
        "question": "A medical supply order costs $250. Sales tax is 8%. What is the total cost?",
        "choices": ["$258", "$265", "$270", "$275"],
        "answer": "$270",
        "explanation": "8% of $250 is $20. $250 + $20 = $270."
    },
        {
        "question": "A patient receives 3 doses of medication per day for 7 days. How many total doses are given?",
        "choices": ["10 doses", "14 doses", "21 doses", "24 doses"],
        "answer": "21 doses",
        "explanation": "3 doses per day × 7 days = 21 total doses."
    },

    {
        "question": "A nurse measures a patient's pulse at 72 beats per minute. How many beats occur in 5 minutes?",
        "choices": ["240 beats", "300 beats", "360 beats", "420 beats"],
        "answer": "360 beats",
        "explanation": "72 beats/min × 5 minutes = 360 beats."
    },

    {
        "question": "A medical chart contains 80 pages. A nurse has completed 60 pages. What percentage is completed?",
        "choices": ["50%", "60%", "75%", "80%"],
        "answer": "75%",
        "explanation": "60 ÷ 80 × 100 = 75%."
    },

    {
        "question": "A patient drinks 1.5 liters of fluid. How many milliliters is this?",
        "choices": ["150 mL", "500 mL", "1000 mL", "1500 mL"],
        "answer": "1500 mL",
        "explanation": "1 liter = 1000 mL. 1.5 × 1000 = 1500 mL."
    },

    {
        "question": "A medication dose is increased from 200 mg to 300 mg. What is the increase?",
        "choices": ["50 mg", "75 mg", "100 mg", "150 mg"],
        "answer": "100 mg",
        "explanation": "300 mg - 200 mg = 100 mg increase."
    },

    {
        "question": "A patient has a temperature of 37°C. What is this approximately in Fahrenheit?",
        "choices": ["90.6°F", "98.6°F", "100°F", "102°F"],
        "answer": "98.6°F",
        "explanation": "°F = (37 × 9/5) + 32 = 98.6°F."
    },

    {
        "question": "A hospital orders 5 boxes of gloves. Each box contains 50 gloves. How many gloves are ordered?",
        "choices": ["100 gloves", "200 gloves", "250 gloves", "500 gloves"],
        "answer": "250 gloves",
        "explanation": "5 boxes × 50 gloves = 250 gloves."
    },

    {
        "question": "A patient needs 750 mL of IV fluid. The bag contains 1000 mL. How much remains after treatment?",
        "choices": ["150 mL", "200 mL", "250 mL", "500 mL"],
        "answer": "250 mL",
        "explanation": "1000 mL - 750 mL = 250 mL."
    },

    {
        "question": "A medical device costs $400. It is discounted by 20%. What is the new price?",
        "choices": ["$300", "$320", "$350", "$380"],
        "answer": "$320",
        "explanation": "20% of $400 is $80. $400 - $80 = $320."
    },

    {
        "question": "A nurse records 6 patient weights: 60, 65, 70, 75, 80, and 90 kg. What is the average weight?",
        "choices": ["70 kg", "73 kg", "75 kg", "80 kg"],
        "answer": "73 kg",
        "explanation": "Add weights: 440 ÷ 6 = approximately 73 kg."
    },

    {
        "question": "A patient is prescribed 1000 mg of medication. The tablets are 500 mg each. How many tablets are needed?",
        "choices": ["1 tablet", "2 tablets", "3 tablets", "4 tablets"],
        "answer": "2 tablets",
        "explanation": "1000 mg ÷ 500 mg = 2 tablets."
    },

    {
        "question": "A hospital has 250 employees. 40% work in patient care. How many employees work in patient care?",
        "choices": ["50", "75", "100", "125"],
        "answer": "100",
        "explanation": "250 × 0.40 = 100 employees."
    },

    {
        "question": "A patient’s respiratory rate is 18 breaths per minute. How many breaths occur in 10 minutes?",
        "choices": ["90", "120", "180", "200"],
        "answer": "180",
        "explanation": "18 breaths/min × 10 minutes = 180 breaths."
    },

    {
        "question": "A container holds 2 gallons of liquid. How many quarts are in the container? (1 gallon = 4 quarts)",
        "choices": ["4 quarts", "6 quarts", "8 quarts", "10 quarts"],
        "answer": "8 quarts",
        "explanation": "2 gallons × 4 quarts = 8 quarts."
    },

    {
        "question": "A patient’s heart rate decreases from 120 bpm to 90 bpm. What is the decrease?",
        "choices": ["20 bpm", "25 bpm", "30 bpm", "40 bpm"],
        "answer": "30 bpm",
        "explanation": "120 - 90 = 30 bpm decrease."
    },

    {
        "question": "A clinic schedules 15 patients every morning for 4 days. How many appointments are scheduled?",
        "choices": ["45", "50", "60", "75"],
        "answer": "60",
        "explanation": "15 patients × 4 days = 60 appointments."
    },

    {
        "question": "A medication concentration is 5 mg/mL. How many mg are in 10 mL?",
        "choices": ["15 mg", "25 mg", "50 mg", "100 mg"],
        "answer": "50 mg",
        "explanation": "5 mg/mL × 10 mL = 50 mg."
    },

    {
        "question": "A patient’s blood glucose changes from 150 mg/dL to 120 mg/dL. What is the decrease?",
        "choices": ["20 mg/dL", "30 mg/dL", "40 mg/dL", "50 mg/dL"],
        "answer": "30 mg/dL",
        "explanation": "150 - 120 = 30 mg/dL."
    },

    {
        "question": "A nurse works 36 hours in 3 days. What is the average number of hours worked per day?",
        "choices": ["10 hours", "12 hours", "14 hours", "18 hours"],
        "answer": "12 hours",
        "explanation": "36 hours ÷ 3 days = 12 hours/day."
    },

    {
        "question": "A patient takes a medication every 6 hours. How many doses are taken in 24 hours?",
        "choices": ["2 doses", "3 doses", "4 doses", "6 doses"],
        "answer": "4 doses",
        "explanation": "24 hours ÷ 6 hours = 4 doses."
    },
        {
        "question": "A patient weighs 176 pounds. Convert the weight to kilograms. (1 kg = 2.2 lb)",
        "choices": ["60 kg", "70 kg", "80 kg", "90 kg"],
        "answer": "80 kg",
        "explanation": "176 ÷ 2.2 = 80 kg."
    },

    {
        "question": "A nurse gives 2.5 mL of medication three times per day. How much medication is given daily?",
        "choices": ["5 mL", "7.5 mL", "10 mL", "12.5 mL"],
        "answer": "7.5 mL",
        "explanation": "2.5 mL × 3 doses = 7.5 mL."
    },

    {
        "question": "A patient's pulse is measured at 90 bpm. What does bpm stand for?",
        "choices": ["Breaths per minute", "Beats per minute", "Blood pressure measurement", "Body pressure measurement"],
        "answer": "Beats per minute",
        "explanation": "BPM means beats per minute and measures heart rate."
    },

    {
        "question": "A medication order requires 250 mg. Each capsule contains 50 mg. How many capsules are needed?",
        "choices": ["3 capsules", "4 capsules", "5 capsules", "6 capsules"],
        "answer": "5 capsules",
        "explanation": "250 mg ÷ 50 mg = 5 capsules."
    },

    {
        "question": "A hospital has 500 masks. Workers use 35% of them. How many masks are used?",
        "choices": ["150", "175", "200", "225"],
        "answer": "175",
        "explanation": "500 × 0.35 = 175 masks."
    },

    {
        "question": "A patient drinks 240 mL of water 5 times per day. How much water is consumed?",
        "choices": ["1000 mL", "1200 mL", "1400 mL", "1500 mL"],
        "answer": "1200 mL",
        "explanation": "240 × 5 = 1200 mL."
    },

    {
        "question": "Convert 3.2 kilograms into grams.",
        "choices": ["32 g", "320 g", "3200 g", "32000 g"],
        "answer": "3200 g",
        "explanation": "1 kg = 1000 g. 3.2 × 1000 = 3200 g."
    },

    {
        "question": "A patient’s temperature rises from 98°F to 101°F. What is the increase?",
        "choices": ["2°F", "3°F", "4°F", "5°F"],
        "answer": "3°F",
        "explanation": "101 - 98 = 3°F."
    },

    {
        "question": "A medical bill is $600. Insurance pays 80%. How much does insurance pay?",
        "choices": ["$400", "$480", "$500", "$520"],
        "answer": "$480",
        "explanation": "600 × 0.80 = $480."
    },

    {
        "question": "A patient has 16 ounces of medication solution. Convert this to cups. (1 cup = 8 ounces)",
        "choices": ["1 cup", "2 cups", "3 cups", "4 cups"],
        "answer": "2 cups",
        "explanation": "16 ÷ 8 = 2 cups."
    },

    {
        "question": "A nurse checks 8 patients every hour for 6 hours. How many patients are checked?",
        "choices": ["40", "48", "56", "64"],
        "answer": "48",
        "explanation": "8 × 6 = 48 patients."
    },

    {
        "question": "A medication is diluted from 100 mL to 250 mL. How much liquid was added?",
        "choices": ["100 mL", "125 mL", "150 mL", "200 mL"],
        "answer": "150 mL",
        "explanation": "250 - 100 = 150 mL added."
    },

    {
        "question": "A patient's oxygen saturation changes from 92% to 97%. What is the increase?",
        "choices": ["3%", "5%", "7%", "10%"],
        "answer": "5%",
        "explanation": "97 - 92 = 5% increase."
    },

    {
        "question": "A nurse works 8 hours per shift for 5 shifts. How many hours worked?",
        "choices": ["30 hours", "35 hours", "40 hours", "45 hours"],
        "answer": "40 hours",
        "explanation": "8 × 5 = 40 hours."
    },

    {
        "question": "A prescription says take 1 tablet every 8 hours. How many tablets are taken per day?",
        "choices": ["2 tablets", "3 tablets", "4 tablets", "8 tablets"],
        "answer": "3 tablets",
        "explanation": "24 ÷ 8 = 3 tablets."
    },

    {
        "question": "A hospital room temperature is 22°C. Which scale is this measured in?",
        "choices": ["Fahrenheit", "Celsius", "Kelvin", "Rankine"],
        "answer": "Celsius",
        "explanation": "°C is the Celsius temperature scale."
    },

    {
        "question": "A patient needs 1500 mL of fluid. The IV runs at 125 mL/hr. How many hours will it take?",
        "choices": ["10 hours", "12 hours", "15 hours", "20 hours"],
        "answer": "12 hours",
        "explanation": "1500 ÷ 125 = 12 hours."
    },

    {
        "question": "A clinic has 90 appointments. 20% are canceled. How many appointments remain?",
        "choices": ["60", "70", "72", "80"],
        "answer": "72",
        "explanation": "20% of 90 is 18. 90 - 18 = 72."
    },

    {
        "question": "A medication costs $120 and increases by 10%. What is the new cost?",
        "choices": ["$125", "$130", "$132", "$140"],
        "answer": "$132",
        "explanation": "10% of $120 is $12. $120 + $12 = $132."
    },

    {
        "question": "A patient has a BMI of 24. What category does this fall into?",
        "choices": ["Underweight", "Healthy range", "Overweight", "Obese"],
        "answer": "Healthy range",
        "explanation": "A BMI between about 18.5 and 24.9 is considered the healthy range."
    },
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
