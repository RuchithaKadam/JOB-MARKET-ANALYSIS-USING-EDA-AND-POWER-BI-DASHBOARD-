#!/usr/bin/env python
# coding: utf-8

# ## Data Collection

# In[41]:


import requests


# In[42]:


url = 'https://www.workindia.in/jobs-in-bengaluru/'


# In[43]:


request_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'}


# In[44]:


page = requests.get(url,headers=request_header)


# In[45]:


page


# In[46]:


import pandas as pd
import numpy as np
from  bs4 import BeautifulSoup


# In[47]:


soup = BeautifulSoup(page.text)


# In[48]:


title=[]
for i in soup.find_all('div',class_='f14 f-bold'):
    title.append(i.text)
len(title)


# In[49]:


title


# In[50]:


price = []
company = []
role = []
Location =[]
JobType = []
exp = []
edu = []
lang=[]

citys=["Bengaluru","hyderabad","mumbai"]
for city in citys:
    for i in range(1,50):
        url = f"https://www.workindia.in/jobs-in-{city}/?pg={i}"
        page = requests.get(url,headers = request_header)
    #    page = requests.get(url)
        soup = BeautifulSoup(page.text)

        for i in soup.find_all("div",class_= "f14 f-bold"):
            price.append(i.text)

        for i in soup.find_all("div",class_= "JobDetail CompanyDetail text-secondary"):
            company.append(i.text)

        for i in soup.find_all("h2",class_= "text-brand f-bold f16"):
            role.append(i.text)

        for i in soup.find_all("div",class_= "JobDetail LocationDetail text-secondary"):
            Location.append(i.text)

        for i in soup.find_all("div",class_= "JobDetail JobTypeDetail text-secondary"):
            JobType.append(i.text)

        for i in soup.find_all("div",class_= "JobDetail ExperienceDetail text-secondary"):
            r = i.text
            if r:
                exp.append(r)
            else:
                exp.append(np.nan)

        for i in soup.find_all("div",class_= "JobDetail QualificationDetail text-secondary"):
            q = i.text
            if q:
                edu.append(q)
            else:
                edu.append(np.nan)

        for i in soup.find_all("div",class_= "JobDetail EnglishDetail text-secondary"):
            s = i.text
            if s:
                lang.append(s)
            else:
                lang.append(np.nan)


print(len(price))
print(len(company))
print(len(role))
print(len(Location))
print(len(JobType))
print(len(exp))
print(len(edu))
print(len(lang))


# In[79]:


df = pd.DataFrame({'Company':company,'Domain':role,'Role':JobType,'Salary':price,'Location':Location,'Education':edu,'Experience':exp,'Language':lang})
df


# In[80]:


df["city"]=df["Location"].str.split(", ").str.get(1)


# In[81]:


df["city"].value_counts()


# In[82]:


import numpy as np


# In[83]:


df["city"]=df["city"].apply(lambda x:np.nan if x in ["Hyderabad (remote)","Bengaluru (remote)","Mumbai (remote)"] else x)


# In[84]:


df.reset_index(drop=True,inplace=True)


# In[85]:


df


# ## Data Cleaning

# #### title

# In[19]:


#df['Company'].str.replace(r'')


# In[86]:


import re
def clean_name(name):
    return re.sub(
        r'\s*\((.*?)\)\s*$',
        lambda m: '' if m.group(1).strip().lower() == name.split('(')[0].strip().lower() else m.group(0),
        name
    )

# Apply cleaning to the column
df['Company_Name'] = df['Company'].apply(clean_name)

df


# #### salary

# In[87]:


df['Min_Salary'] = df['Salary'].str.extract(r'^Rs.\s(\d+)')
df['Min_Salary']


# In[88]:


df['Max_Salary'] = df['Salary'].str.extract(r'\sRs.\s(\d+)$')
df['Max_Salary']


# #### exp

# In[89]:


df['Experience'].value_counts()


# In[90]:


def experience_to_num(exp):
    if pd.isna(exp):
        return None   # keep NaN as is
    exp = exp.strip().lower()
    if "fresher" in exp:
        return 0
    elif "1 - 2" in exp:
        return 1
    elif "2+" in exp:
        return 2
    else:
        return None   # for unexpected values

df["Experience"] = df["Experience"].apply(experience_to_num)


# In[91]:


df.drop(columns=['Company','Salary'],inplace=True)


# #### Gender

# In[92]:


import re

def extract_gender(edu):
    if pd.isna(edu):
        return None
    match = re.search(r"(Male|Female)", edu, re.IGNORECASE)
    if match:
        return match.group(0).capitalize()
    return 'M/F'

df["Gender"] = df["Education"].apply(extract_gender)


# #### lang

# In[93]:


def Lang(lng):
    if pd.isna(lng):
        return None   # keep NaN as is
    #ed = ed.strip().lower()
    if "Speak Thoda English"  in lng:
        return 'Required'
    elif "No English Required" in lng:
        return 'Not Required'
    elif "Speak Good English" in lng:
        return 'Fluent'
    elif "Speak Fluent English" in lng:
        return 'Fluent'
    else:
        return np.nan   # for unexpected values

df["English Communication"] = df["Language"].apply(Lang)


# In[94]:


# First check exact column names
print(df.columns.tolist())


# #### education

# In[95]:


# Convert column to string (handles NaN also)
df['Education'] = df['Education'].astype(str).str.strip()

# Replace patterns
df['Education'] = df['Education'].replace({
    r'^Tenth Pass.*': 'SSLC',
    r'^< 10th Pass.*': 'SSLC',
    r'.*12th Pass.*': 'PUC',
    r'.*Graduate.*': 'Graduate'
}, regex=True)

df


# In[96]:


df.drop(columns=['Language','Location'],inplace=True)


# In[97]:


df.describe()


# In[98]:


df['Min_Salary'] = pd.to_numeric(df['Min_Salary'], errors='coerce')
df['Max_Salary'] = pd.to_numeric(df['Max_Salary'], errors='coerce')


# In[99]:


df["Max_Salary"]=df["Max_Salary"].fillna(df["Max_Salary"].median())


# In[100]:


df['Avg_Salary'] = (df['Min_Salary'] + df['Max_Salary']) / 2


# In[101]:


df['Min_Salary'] = df['Min_Salary'].astype('float')


# In[162]:


df.info()


# In[103]:


df.head()


# In[10]:


df.shape


# In[11]:


df.to_csv('workindia.csv',index=False)


# In[9]:


df = df.dropna()


# ## Data Analysis

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df = pd.read_csv('workindia.csv')


# In[4]:


df


# In[ ]:





# In[15]:


print("Total Jobs:", len(df))
print('*'*20)
print("Jobs per City:\n", df['city'].value_counts())
print('*'*20)
print("Jobs per Education:\n", df['Education'].value_counts())
print('*'*20)
print("Jobs per Experience:\n", df['Experience'].value_counts())


# In[16]:


print('Top companies hiring: ')
print(df['Company_Name'].value_counts().head(10))
print("\n")
print('*'*20)
print('Top companies by average salary:')
top_salary = df.groupby("Company_Name")['Avg_Salary'].mean().sort_values(ascending=False).head(10)
print(top_salary)


# In[246]:


plt.figure(figsize=(15,6))
plt.bar(df['Role'],df['Min_Salary'])
plt.xticks(rotation=80)
plt.grid(axis='y')
plt.title('Min_salary by Role')
plt.xlabel('Role')
plt.ylabel('Min_salary')
plt.show()


# In[11]:


salary_quantiles = df['Avg_Salary'].quantile([0.01, 0.25, 0.5, 0.75, 0.95, 0.99])
print(salary_quantiles)


# In[16]:


sns.scatterplot(data=df, x='Experience', y='Avg_Salary')
plt.title("Experience vs Avg Salary")
plt.show()


# In[19]:


plt.figure(figsize=(15,6))
plt.bar(df['Role'],df['Max_Salary'],color='c')
plt.xticks(rotation=80)
plt.grid(axis='y')
plt.title('Max_salary by Role')
plt.xlabel('Role')
plt.ylabel('Max_salary')
plt.show()


# In[244]:


sns.boxplot(x='city',y='Avg_Salary',data=df)
plt.title('Avg_salary by City')
plt.show()


# In[143]:


'''
Q1 = df["Avg_Salary"].quantile(0.25)
Q3 = df["Avg_Salary"].quantile(0.75)
IQR = Q3 - Q1

# Define bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers
df_no_outliers = df[(df["Avg_Salary"] >= lower_bound) & (df["Avg_Salary"] <= upper_bound)]

df_no_outliers
'''


# In[144]:


#df_no_outliers['Avg_Salary'].plot(kind='box')


# In[142]:


#df_no_outliers.describe()


# In[251]:


df.describe()


# In[258]:


#1. Average Salary by Education
edu_salary = df.groupby("Education")["Avg_Salary"].mean().reset_index()
sns.barplot(data=edu_salary, x="Education", y="Avg_Salary")
plt.title("Average Salary by Education Level")
plt.show()


# In[17]:


numeric_cols = ['Experience', 'Min_Salary', 'Max_Salary', 'Avg_Salary']
corr = df[numeric_cols].corr()

sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()



# In[179]:


# Salary Growth with Experience
exp_salary = df.groupby("Experience")["Avg_Salary"].mean().reset_index()
sns.lineplot(data=exp_salary, x="Experience", y="Avg_Salary", marker="o")
plt.title("Salary Growth with Experience")
plt.show()


# In[181]:


# 3. Top Paying Domains
domain_salary = df.groupby("Domain")["Avg_Salary"].mean().sort_values(ascending=False).reset_index()
sns.barplot(data=domain_salary.head(10), x="Avg_Salary", y="Domain")
plt.title("Top 10 Paying Domains")
plt.show()


# In[34]:


## English Communication Requirement Impact on Salary
eng_salary = df.groupby("English Communication")["Avg_Salary"].mean().reset_index()
sns.barplot(data=eng_salary, x="English Communication", y="Avg_Salary",palette="Set2")
plt.title("English Communication vs Salary")
plt.show()


# In[35]:


## Companies Offering Highest Salaries
company_salary = df.groupby("Company_Name")["Avg_Salary"].mean().sort_values(ascending=False).head(10).reset_index()
sns.barplot(data=company_salary, x="Avg_Salary", y="Company_Name",palette="Paired")
plt.title("Top 10 Companies Offering Highest Salaries")
plt.show()


# In[37]:


## Roles with Most Demand
role_count = df["Role"].value_counts().head(10).reset_index()
role_count.columns = ["Role","Count"]
sns.barplot(data=role_count, x="Count", y="Role",palette = 'tab20')
plt.title("Top 10 Roles in Demand")
plt.show()


# In[39]:


# 5. Min vs Max Salary Range per Domain (Line Plot with Fill)
domain_range = df.groupby("Domain")[["Min_Salary","Max_Salary"]].mean().reset_index()
domain_range = domain_range.sort_values("Max_Salary", ascending=False).head(8)
plt.plot(domain_range["Domain"], domain_range["Min_Salary"], marker="o", label="Min Salary")
plt.plot(domain_range["Domain"], domain_range["Max_Salary"], marker="o", label="Max Salary")
plt.fill_between(domain_range["Domain"], domain_range["Min_Salary"], domain_range["Max_Salary"], alpha=0.2)
plt.xticks(rotation=80)
plt.legend()
plt.xlabel('Domain')
plt.ylabel('Min vs Max Salary Range')
plt.title("Min vs Max Salary Range per Domain")
plt.grid()
plt.show()


# In[252]:


sns.countplot(data=df, x="Experience", palette="dark")
plt.title("Job Count by Experience")
plt.show()


# In[38]:


sns.histplot(df["Avg_Salary"], bins=30, kde=True, color="blue")
plt.title("Distribution of Average Salary")
plt.grid(axis='y')
plt.show()


# In[253]:


df["Gender"].value_counts().plot(kind="pie", autopct="%1.1f%%", colors=sns.color_palette("colorblind"))
plt.title("Gender Preference in Jobs")
plt.show()


# In[249]:


# Experience vs Max Salary
plt.figure(figsize=(8,6))
sns.violinplot(data=df, x="Experience", y="Max_Salary", inner="box", palette="Set2")
plt.title("Experience vs Maximum Salary Distribution", fontsize=14)
plt.xlabel("Experience (Years)")
plt.ylabel("Max Salary (INR)")
plt.show()


# In[ ]:




