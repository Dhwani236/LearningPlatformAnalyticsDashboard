import pandas as pd
import numpy as np
import plotly.express as px


data=pd.read_csv("C:/Users/dhwan/OneDrive/Documents/college/SEM 4/DVD/online_learning_platform_dataset.csv")

df=pd.DataFrame(data)

# Calculate average study hours per difficulty level
avg_hours = df.groupby("Course_Difficulty")["Hours_Spent_Per_Week"].mean().reset_index()

# Arrange levels in proper order
difficulty_order = ["Beginner", "Intermediate", "Advanced"]
avg_hours["Course_Difficulty"] = pd.Categorical(
    avg_hours["Course_Difficulty"],
    categories=difficulty_order,
    ordered=True
)

avg_hours = avg_hours.sort_values("Course_Difficulty")

# Create line chart
fig = px.line(
    avg_hours,
    x="Course_Difficulty",
    y="Hours_Spent_Per_Week",
    title="Study Hours Trend by Course Difficulty",
    markers=True
)

# Customize line and markers
fig.update_traces(
    line=dict(width=4),
    marker=dict(size=10, symbol="diamond"),
)

# Axis labels
fig.update_layout(
    xaxis_title="Course Difficulty Level",
    yaxis_title="Average Study Hours per Week"
)

# QUESTION 2

course_wise_student=df['Course_Category'].value_counts().reset_index()
course_wise_student.columns=["Course_Category","Student_Count"]

# Create bar chart
fig = px.bar(
    course_wise_student,
    x='Course_Category',
    y='Student_Count',
    text="Student_Count",
    title="Students Enrolled in Each Course Category",
    color="Course_Category"
)

# Customize bar appearance
fig.update_traces(
    width=0.6,              # bar width
    textposition="outside"  # display count above bars
)

# Add axis labels
fig.update_layout(
    xaxis_title="Course Category",
    yaxis_title="Number of Students",
    showlegend=False
)

# QUESTION 3

df["Completion_Group"] = pd.cut(
    df["Quiz_Score"],
    bins=[0, 25, 50, 75, 100],
    labels=["0–25%", "25–50%", "50–75%", "75–100%"]
)

# Count students in each group
completion_dist = df["Completion_Group"].value_counts().reset_index()
completion_dist.columns = ["Completion_Group", "Student_Count"]

# Create donut chart
fig = px.pie(
    completion_dist,
    names="Completion_Group",
    values="Student_Count",
    title="Student Distribution by Course Completion Percentage",
    color_discrete_sequence=px.colors.qualitative.Set3,
    hole=0.4
)

# Customize labels and hover info
fig.update_traces(
    textinfo="percent+label",
)

# QUESTION 4

fig = px.box(
    df,
    x="Course_Category",
    y="Quiz_Score",
    color="Course_Category",
    points="outliers",   # show only outliers
    title="Quiz Performance by Course Category"
)

# Customize appearance
fig.update_traces(
    marker=dict(size=6),
    line=dict(width=2)
)

# Axis labels
fig.update_layout(
    xaxis_title="Course Category",
    yaxis_title="Quiz Score"
)

# QUESTION 5

fig = px.violin(
    df,
    x="Course_Difficulty",
    y="Hours_Spent_Per_Week",
    color="Course_Difficulty",
    box=True,          # show mini box plot inside
    points="all",      # show all data points
    title="Study Hours Comparison by Course Difficulty"
)

# Show mean line
fig.update_traces(meanline_visible=True)

# Axis labels
fig.update_layout(
    xaxis_title="Course Difficulty",
    yaxis_title="Study Hours per Week"
)

# QUESTION 6

stages = [
    "Students Enrolled",
    "Videos Watched",
    "Assignments Submitted",
    "Quiz Attempted",
    "Course Completed"
]

values = [
    len(df),                                      # total students
    df["Videos_Watched"].gt(0).sum(),             # watched at least 1 video
    df["Assignments_Submitted"].gt(0).sum(),      # submitted assignment
    df["Quiz_Score"].notnull().sum(),             # attempted quiz
    (df["Completion_Status"] == "Completed").sum() # completed course
]

# Create funnel chart
fig = px.funnel(
    x=values,
    y=stages,
    title="Learning Engagement Funnel"
)

# Customize labels
fig.update_traces(
    textinfo="value+percent initial"
)

# QUESTION 7

fig = px.scatter(
    df,
    x="Assignments_Submitted",
    y="Quiz_Score",
    title="Assignments Submitted vs Quiz Average Score",
    hover_data=["Student_ID", "Course_Category"]
)

# Customize markers
fig.update_traces(
    marker=dict(
        size=10,
        opacity=0.6
    )
)

# Axis labels
fig.update_layout(
    xaxis_title="Assignments Submitted",
    yaxis_title="Quiz Average Score"
)


# QUESTION 8

tree_data = (
    df.groupby(["City", "Course_Category"])
      .size()
      .reset_index(name="Student_Count")
)

# Create treemap
fig = px.treemap(
    tree_data,
    path=["City", "Course_Category"],
    values="Student_Count",
    color="Student_Count",
    color_continuous_scale="Blues",
    title="Hierarchical Distribution of Students by City and Course Category"
)

# QUESTION 9

# Create certificate status column
df["Certificates_Earned"] = df["Completion_Status"].apply(
    lambda x: "Yes" if x == "Completed" else "No"
)

# Create sunburst chart
fig = px.sunburst(
    df,
    path=["Course_Category", "Course_Difficulty", "Certificates_Earned"],
    title="Course Category → Difficulty → Certificates Earned",
    color="Course_Difficulty",
    color_discrete_sequence=px.colors.qualitative.Set2
)

# QUESTION 10

num_cols = [
    "Hours_Spent_Per_Week",
    "Videos_Watched",
    "Assignments_Submitted",
    "Quiz_Score"
]

# Create correlation matrix
corr_matrix = df[num_cols].corr()

# Create heatmap
fig = px.imshow(
    corr_matrix,
    text_auto=True,                 # annotations
    color_continuous_scale="Blues",
    title="Correlation Heatmap of Numerical Variables"
)

# Customize grid lines
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=True)
fig.show()

