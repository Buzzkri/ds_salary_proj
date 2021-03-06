import pandas as pd
df = pd.read_csv("glassdoor_jobs.csv")

#Salary parsing

df["hourly"] = df["Salary Estimate"].apply(lambda x: 1 if "per hour" in x.lower() else 0)
df["employer_provided"] = df["Salary Estimate"].apply(lambda x: 1 if "employer provided salary:" in x.lower() else 0)


df = df[df["Salary Estimate"] != "-1"]
salary = df["Salary Estimate"].apply(lambda x: x.split("(")[0])
minus_kd = salary.apply(lambda x: x.replace( "K", "").replace("$",""))
min_hr = minus_kd.apply(lambda x: x.lower().replace("per hour","").replace("employer provided salary:",""))

df["min_salary"] = min_hr.apply(lambda x: int(x.split("-")[0]))
df["max_salary"] = min_hr.apply(lambda x: int(x.split("-")[1]))
df["avg_salary"] = (df.min_salary+df.max_salary)/2

#Company name text only
df["company_txt"] = df.apply(lambda x: x["Company Name"] if x["Rating"] <0 else x["Company Name"][:-3], axis = 1)

#Job city, state, match
df["job_city"] = df["Location"].apply(lambda x: x.split(",")[0])
df["job_state"] = df["Location"].apply(lambda x: x.split(",")[1])
df["same_state"] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)

#age of company
df["age"] = df.Founded.apply(lambda x: x if x <1 else 2020 - x)

#parsing job description (python, SQL, R, etc.)
#Python
df["python_yn"] = df["Job Description"].apply(lambda x: 1 if "python" in x.lower() else 0)
#spark
df["spark"] = df["Job Description"].apply(lambda x: 1 if "spark" in x.lower() else 0)
#aws
df["aws"] = df["Job Description"].apply(lambda x: 1 if "aws" in x.lower() else 0)
#excel
df["excel"] = df["Job Description"].apply(lambda x: 1 if "excel" in x.lower() else 0)

df_out = df.drop(["Unnamed: 0"], axis =1)

# df_out.to_csv("personal_salary_data_cleaned.csv",index = False)

pd.read_csv("personal_salary_data_cleaned.csv")


def title_simplifier(title):
    if "data scientist" in title.lower():
        return "data scientist"
    elif "data engineer" in title.lower():
        return "data engineer"
    elif "analyst" in title.lower():
        return "analyst"
    elif "machine learning" in title.lower():
        return "machine learning"
    elif "manager" in title.lower():
        return "manager"
    elif "director" in title.lower():
        return "director"
    else:
        return "na"
    
def seniority(title):
    if "sr" in title.lower() or "senior" in title.lower() or "lead" in title.lower() or "principal" in title.lower():
        return "senior"
    elif "jr" in title.lower() or "jr." in title.lower():
        return "jr"
    else:
        return "na"