
# coding: utf-8

# In[1]:


import os
import pandas as pd
import numpy as np


# In[2]:


student = os.path.join("Raw Data", "students_complete.csv")
school = os.path.join("Raw Data", "schools_complete.csv")
student_df=pd.read_csv(student)
school_df=pd.read_csv(school)
#student_df.head()
    #school_df.head()
#student_df.count() ##39170 rows
    #school_df.count() ##15 rows
#student_df.columns ##'Student ID', 'name', 'gender', 'grade', 'school', 'reading_score', 'math_score'
    #school_df.columns ##'School ID', 'name', 'type', 'size', 'budget'
    #school_df['name'].value_counts()


# In[3]:


#Renaming the common index on both csv to 'School_Name' to enable join'
student_df1 = student_df.rename(columns={'school':'School_Name'})
school_df1 = school_df.rename(columns={'name':'School_Name'})


# In[4]:


#Join tables, so that the school info is associated for all students
table_df = pd.merge(student_df1, school_df1, on="School_Name", how="left")
#merge_table.head()
#merge_table.columns


# In[5]:


#####################################################District Summary########################################################

    #Create a high level snapshot (in table form) of the district's key metrics, including:
print("District Data Summary")
print("-------------------------------------------------------------------------------------------")    
    # Total Schools
print("Total Number of Schools: " + str(len(table_df['School_Name'].unique())))
#t_school=table_df['School_Name'].unique() ##Method 2 by creating a new variable
#len(t_school)
    
      # Total Students
print("Total Number of Students: " + str(len(table_df['Student ID'].unique())))
#>>>39170 which corresponds to the total number of rows, meaning also that there is not either a single student or two students with the same ID enrolled in two schools :D
      
    # Total Budget
print("Total Budget: $" + str(table_df['budget'].unique().sum()))
        ##Method 2 by creating a new variable;   #budget = table_df['budget'].unique() 
                                                #budget.sum()
      # Average Math Score
print("Average Math Score: " + str(table_df['math_score'].mean()))
      #>>> 78.98537145774827

      # Average Reading Score
print("Average Reading Score: " + str(table_df['reading_score'].mean()))
      #>>> 81.87784018381414
      
      # % Passing Math
print("% Passing Math: " + str(len(table_df.loc[table_df["math_score"] >= 70,:]) /  len(table_df['Student ID'].unique())))
math=len(table_df.loc[table_df["math_score"] >= 70,:]) / len(table_df['Student ID'].unique())
    #>>>0.749808526933878
    
    # % Passing Reading
print("% Passing Math: " + str(len(table_df.loc[table_df["reading_score"] >= 70,:]) /  len(table_df['Student ID'].unique())))
reading=len(table_df.loc[table_df["reading_score"] >= 70,:]) /  len(table_df['Student ID'].unique())
    #>>>0.8580546336482001
    
      # Overall Passing Rate (Average of the above two)
print("% Average Passing Rate: " + str((math+reading)/2))


# In[6]:


###############################################################################################################################


# In[7]:


########################################################School Summary########################################################

#Instructions + starting notes

    #Create an overview table that summarizes key metrics about each school, including:
  # School Name
#print("Schools: " + str(table_df['School_Name'].unique()))
  # School Type
#print("School Type" + str(table_df)
  # Total Students
  # Total School Budget
  # Per Student Budget
  # Average Math Score
  # Average Reading Score
  # % Passing Math
  # % Passing Reading
  # Overall Passing Rate (Average of the above two)


# In[8]:


#Filter main table attributes
table_dfl=table_df.loc[:,["School_Name","type", "size", "budget", "math_score", "reading_score"]]


# In[9]:


table_dfl #retains 39170 rows
#table_df2=table_dfl.groupby("School_Name")
#table_df2.head() #75 rows, why???? Doesn't even group properly
r70=table_dfl.loc[table_dfl["reading_score"] >= 70,:] #Filters properly
m70=table_dfl.loc[table_dfl["math_score"] >= 70,:]
#count of students who passed per school / size
r70=r70.groupby("School_Name").count() #counts all who passed per school. Cool, now isolate one row.
m70=m70.groupby("School_Name").count()
r70=r70["reading_score"] #choosing just one row. All values are the same per rows, since each row represent a student who passed.
m70=m70["math_score"]

table_df1=table_dfl.groupby("School_Name").mean() #Averages of the tests scores by schools
table_df1_type=table_dfl.groupby("School_Name")
table_df1_type=table_df1_type['type']


# In[10]:


#school_sum_df = table_df.loc[:,["School_Name","type", "size", "budget", "math_score", "reading_score"]]
#x=school_sum_df.groupby("School_Name")

#Creating my variables for the summary table dataframe
size=table_df1["size"].unique() #Is fine, unique attribute
pm=m70/size #Passing rate, math
rm=r70/size #Passing rate, reading
stype=table_df1_type.unique() #Is fine, unique attribute
budget=table_df1["budget"].unique() #Is fine, unique attribute
math_score=table_df1["math_score"].mean() #"table_df1.head()" outputs 75 rows; however the avg numbers checks out
reading_score=table_df1["reading_score"].mean() #"table_df1.head()" outputs 75 rows; however the avg numbers checks out
##method 2 to gather averages:
#av_r=scores["reading_score"] #avg math score per school
#av_m=scores["math_score"] #avg reading score per school
psb = table_df1["budget"].unique() / table_df1["size"].unique() #Error prob contigent on prior variables
#o_avg = (table_df1["math_score"].mean() + table_df1["reading_score"].mean())/2 #That's actually the avg overall score
opr = (pm + rm) /2 #got it :) !


# In[51]:


school_summary_table = pd.DataFrame({"Type":stype,
                                    "Total_Students":size,
                                     "Total_School_Budget":budget,
                                     "Per_Student_Budget":psb,
                                     "Average_Math_Score":math_score,
                                     "Average_Reading_Score":reading_score,
                                     "Passing_Math":pm*100,
                                     "Passing_Reading":rm*100,
                                   "Overall_Passing_Rate":opr*100})

#mapping (cleaning up how values are displayed)
school_summary_table["Total_School_Budget"] = school_summary_table["Total_School_Budget"].map("${:,.0f}".format)
school_summary_table["Per_Student_Budget"] = school_summary_table["Per_Student_Budget"].map("${:,.0f}".format)
school_summary_table["Total_Students"]=school_summary_table["Total_Students"].map("{:,.0f}".format)
school_summary_table["Passing_Math"]=school_summary_table["Passing_Math"].map("{:.2f}%".format)
school_summary_table["Passing_Reading"]=school_summary_table["Passing_Reading"].map("{:.2f}%".format)
school_summary_table["Overall_Passing_Rate"]=school_summary_table["Overall_Passing_Rate"].map("{:.2f}%".format)
school_summary_table["Average_Math_Score"]=school_summary_table["Average_Math_Score"].map("{:,.2f}".format)
school_summary_table["Average_Reading_Score"]=school_summary_table["Average_Reading_Score"].map("{:,.2f}".format)

school_summary_table.head(15)


# In[12]:


#mapping columns (work in progress)

#school_summary_table["Total School Budget"]=school_summary_table["Total School Budget"].map("${:.2f}".format)
#school_summary_table["Total Students"]=school_summary_table["Total Students"].map("{:,}".format)
#school_summary_table.dtypes


# In[13]:


###############################################################################################################################


# In[14]:


#######################################Top Performing Schools (By Passing Rate)################################################


# In[53]:


top_schools=school_summary_table.sort_values("Overall_Passing_Rate", ascending=False)
top_schools.head(5)


# In[ ]:


#######################################Low Performing Schools (By Passing Rate)#############################################


# In[61]:


top_schools=school_summary_table.sort_values("Overall_Passing_Rate", ascending=True)
top_schools.head(5)


# In[16]:


###############################################################################################################################


# In[17]:


#################################################Average Scores by Grades#######################################################


# In[310]:


#Creating the variables for Avg Reading score, per grade, per school
table_grade_read_df=table_df.loc[:,["reading_score","grade","School_Name"]]
table_grade_read_df.head()
#9th, Read
table_grade_df_9=table_grade_read_df[table_grade_read_df["grade"]=="9th"]
gr_avgread_9=table_grade_df_9.groupby(["School_Name"]).mean().reset_index()
#10th, Read
table_grade_df_10=table_grade_read_df[table_grade_read_df["grade"]=="10th"]
gr_avgread_10=table_grade_df_10.groupby(["School_Name"]).mean().reset_index() #Mean reading score for 10th graders, for each school
#11th, Read
table_grade_df_11=table_grade_read_df[table_grade_read_df["grade"]=="11th"]
gr_avgread_11=table_grade_df_11.groupby(["School_Name"]).mean().reset_index()
#12th, Read
table_grade_df_12=table_grade_read_df[table_grade_read_df["grade"]=="12th"]
gr_avgread_12=table_grade_df_12.groupby(["School_Name"]).mean().reset_index()

#Creating the variables for Avg Math score, per grade, per school
table_grade_math_df=table_df.loc[:,["math_score","grade","School_Name"]]
table_grade_math_df.head()
#9th, Math
table_grade_math_df_9=table_grade_math_df[table_grade_math_df["grade"]=="9th"]
gr_avgmath_9=table_grade_math_df_9.groupby(["School_Name"]).mean().reset_index()
#10th, Math
table_grade_math_df_10=table_grade_math_df[table_grade_math_df["grade"]=="10th"]
gr_avgmath_10=table_grade_math_df_10.groupby(["School_Name"]).mean().reset_index() 
#11th, Math
table_grade_math_df_11=table_grade_math_df[table_grade_math_df["grade"]=="11th"]
gr_avgmath_11=table_grade_math_df_11.groupby(["School_Name"]).mean().reset_index()
#12th, Math
table_grade_math_df_12=table_grade_math_df[table_grade_math_df["grade"]=="12th"]
gr_avgmath_12=table_grade_math_df_12.groupby(["School_Name"]).mean().reset_index()


# In[356]:


#Merging Dataframes for Avg Math Scores per Grade & Schools because I couldn't be bothered with f#%$*ing creating a DataFrame that doesn't recognize the "School_Name" key despite being f&&*$ there
m_910=pd.merge(gr_avgmath_9,gr_avgmath_10,on='School_Name')
m_91011=pd.merge(m_910,gr_avgmath_11,on='School_Name')
m_finalmerge=pd.merge(m_91011,gr_avgmath_12,on='School_Name')
m_finalmerge.columns = ["School_Name","9th","10th","11th","12th"]

m_finalmerge["9th"]=m_finalmerge["9th"].map("{:,.2f}".format)
m_finalmerge["10th"]=m_finalmerge["10th"].map("{:,.2f}".format)
m_finalmerge["11th"]=m_finalmerge["11th"].map("{:,.2f}".format)
m_finalmerge["12th"]=m_finalmerge["12th"].map("{:,.2f}".format)

m_finalmerge
#m_finalmerge.rename(columns={'math_score_x':'9th','math_score_y':'10th','math_score_x':'11th','math_score_y':'12th'})


# In[357]:


#Merging Dataframes for Avg Reading Scores per Grade & Schools
r_910=pd.merge(gr_avgread_9,gr_avgread_10,on='School_Name')
r_91011=pd.merge(r_910,gr_avgread_11,on='School_Name')
r_finalmerge=pd.merge(r_91011,gr_avgread_12,on='School_Name')
r_finalmerge.columns = ["School_Name","9th","10th","11th","12th"]

r_finalmerge["9th"]=r_finalmerge["9th"].map("{:,.2f}".format)
r_finalmerge["10th"]=r_finalmerge["10th"].map("{:,.2f}".format)
r_finalmerge["11th"]=r_finalmerge["11th"].map("{:,.2f}".format)
r_finalmerge["12th"]=r_finalmerge["12th"].map("{:,.2f}".format)

r_finalmerge
#r_finalmerge=r_finalmerge.rename(columns={'reading_score_x':'9th','reading_score_y':'10th','reading_score_x':'11th','reading_score_y':'12th'})


# In[330]:


##Problems with combining DFs into one due to error pertaining to keys. Which is why I merged instead.

##.keys() I am losing the School_Name index somehow after grouping, which is why I can't combine into one dataframe.

#score_summary_read_grades=pd.DataFrame({"9th":gr_avgread_9,
#                                    "10th":gr_avgread_10,
#                                          "11th":gr_avgread_11,
#                                         "12th": gr_avgread_12
#                                     })


#Error: If using all scalar values, you must pass an index

#score_summary_math_grades=pd.DataFrame({"9th":gr_avgmath_9,
#                                    "10th":gr_avgmath_10,
#                                         "11th":gr_avgmath_11,
#                                         "12th": gr_avgmath_12
#                                    })

#merge_test=pd.merge(gr_avgread_9,gr_avgread_10,on='School_Name')
#merge_test.head()
#gr_avgread_9.head()


# In[331]:


##Didn't Index correctly (previous attempt, original submission)

#table_m_gr=table_df.loc[:,["School_Name", "math_score","reading_score","grade"]]
#table_m_gr1=table_m_gr.groupby(['School_Name','grade'])
#m_gr=table_m_gr1["math_score"].mean()
#r_gr=table_m_gr1["reading_score"].mean()
#school_score_grades = pd.DataFrame({"Average Math Score":m_gr,
#                                    "Average Reading Score":r_gr,
#                                     })
#school_score_grades


# In[19]:


###############################################################################################################################


# In[67]:


###################################################Scores by School Spending##################################################

#Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
  #Average Math Score
  #Average Reading Score
  #% Passing Math
  #Passing Reading
  #Overall Passing Rate (Average of the above two)

#Observe budget data to create reasonable ranges for the bins

budget=table_df1["budget"].unique() #Variable previously created, for reference.

#school_summary_table["Total_School_Budget"].mean() #Doesn't work because mapping prob modified the type from int to str.
budget.mean() #Just use the variable instead #>>>1643295.2
budget.min() #248087
budget.max() #3124928

spending_bin = [200000,1000000,2000000,3500000]


# In[68]:


table_budget_bins=pd.cut(table_df["budget"], spending_bin) #changed df from school_summary_table["Total_School_Budget"] 
table_budget_bins.head
budget_summary_table = pd.DataFrame({"Budget Range": table_budget_bins, #Need to recreated variables to index by bins
                                     "Average Math Score":math_score,
                                     "Average Reading Score":reading_score,
                                     "% Passing Math":pm,
                                     "% Passing Reading":rm,
                                   "Overall Passing Rate":opr
                                    })
budget_summary_table.head(15)


# In[22]:


budget_summary_table.dtypes


# In[23]:


###############################################################################################################################


# In[24]:


###################################################Scores by School Size######################################################


# In[25]:


school_summary_table["Total Students"].mean() #2611
school_summary_table["Total Students"].min() #427
school_summary_table["Total Students"].max() #4976

groups = ['Small (> 2,000)', 'Medium (2,000 - 3,000)', 'Large (3,000 - 5,000)']
bins = [400,2000,3000,5000]


# In[26]:


table_size_bins=pd.cut(school_summary_table["Total Students"], bins,labels=groups)
table_size_bins.head
size_summary_table = pd.DataFrame({"Size Range": table_size_bins,
                                     "Average Math Score":math_score,
                                     "Average Reading Score":reading_score,
                                     "% Passing Math":pm,
                                     "% Passing Reading":rm,
                                   "Overall Passing Rate":opr
                                    })
size_summary_table.head(15)


# In[27]:


###############################################################################################################################


# In[28]:


###################################################Scores by School Type######################################################


# In[29]:


#Prior functions (for reference)
table_dfl_type=table_df.loc[:,["type", "math_score", "reading_score"]]
table_dfl_type
table_dfl_math=table_df.loc[:,["type","math_score"]]
table_dfl_read=table_df.loc[:,["type","reading_score"]]

###################
t_scores=table_dfl_type.groupby("type").mean() #Avg for all my attributes selected above # !Cannot import into new Dataframe

t_math=t_scores["math_score"] #Mean for Math only * or...t_scores.math_score

t_read=t_scores["reading_score"] #Mean for Read only *

#Means of Scores ###REDUNDANT
t_70_pass=table_df.loc[:,["type","math_score", "reading_score"]]
t_mean=t_70_pass.groupby("type").mean() #Averages of BOTH tests scores by types # !Cannot import into new Dataframe


t_r70=table_dfl_read.loc[table_dfl_read["reading_score"] >= 70,:] #Filters properly
t_r70=t_r70.groupby("type").count() #Number of students who passed the reading test for BOTH school types *
t_m70=table_dfl_math.loc[table_dfl_math["math_score"] >= 70,:]
t_m70=t_m70.groupby("type").count()  #Number of students who passed the math test for BOTH school types *

#Percentage of students who passed the tests

total_count_read=table_df.loc[:,["type","reading_score"]]
total_students_read=total_count_read.groupby("type").count() #total students; the same number of students took the math and reading exams.
                                                        #I'm only doing this twice to be able to divide by appropriate columns
total_count_math=table_df.loc[:,["type","math_score"]]
total_students_math=total_count_math.groupby("type").count()

student_perc_pass_reading=t_r70/total_students_read
student_perc_pass_reading=student_perc_pass_reading["reading_score"] #Avg read score of those who passed *
student_perc_pass_math=t_m70/total_students_math
student_perc_pass_math=student_perc_pass_math["math_score"] #Avg math score of those who passed *

#Average Passing Rate
avg_passing_rate=(student_perc_pass_reading+student_perc_pass_math)/2 #Avg Passing Rate *

#Counts for total students in Charter and District schools ###Redundant
#charter_student_count=table_dfl_type[table_dfl_type["type"]=='Charter'].count()
#charter_student_count=charter_student_count["type"] #12194
#district_student_count=table_dfl_type[table_dfl_type["type"]=='District'].count()
#district_student_count=district_student_count["type"] #26976


# In[30]:


district_summary_tableX = pd.DataFrame({"Average Math Scores":t_math,
                                        "Average Reading Scores":t_read,
                                    "% Passing Math":student_perc_pass_math,
                                    "% Passing Reading":student_perc_pass_reading,
                                    "% Overall Passing Rate": avg_passing_rate
                                       })
district_summary_tableX.head()


# In[31]:


#Count for students who passed, Charter & District ###Way Redundant, essentially if I want to isolate my variables by 
# score & district type. Keeping this here for reference.

#Charter, Passed Reading
#ctype_count_r70=r70[r70["type"]=='Charter'].count()
#ctype_count_r70=ctype_count_r70["type"] #>>> 11785

#Charter, Passed Math
#ctype_count_m70=m70[m70["type"]=='Charter'].count()
#ctype_count_m70=ctype_count_m70["type"] #>>> 11426

#District, Passed Reading
#dtype_count_r70=r70[r70["type"]=='District'].count()
#dtype_count_r70=dtype_count_r70["type"] #>>> 21825

#District, Passed Math
#dtype_count_m70=m70[m70["type"]=='District'].count()
#dtype_count_m70=dtype_count_m70["type"] #>>> 17944

#Total Count for students in Charter & District

#Total Students, Charter
#ctype_totalcount_r70=table_dfl[table_dfl["type"]=='Charter'].count()
#ctype_totalcount_r70=ctype_totalcount_r70["type"] #>>>12194

#ReadTotal Students, District
#dtype_totalcount_r70=table_dfl[table_dfl["type"]=='District'].count()
#dtype_totalcount_r70=dtype_totalcount_r70["type"] #>>>26976

#district_passed_reading= dtype_count_r70 / dtype_totalcount_r70 #0.8090524911032029
#district_passed_math= dtype_count_m70 / dtype_totalcount_r70 #0.6651838671411625
#charter_passed_reading= ctype_count_r70 / ctype_totalcount_r70 #0.9664589142201082
#charter_passed_math= ctype_count_m70 / ctype_totalcount_r70 #0.9370182056749221


# In[32]:


###############################################################################################################################


# In[ ]:


#Output pdf
    #<Insert function here>

