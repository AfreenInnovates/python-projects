import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from collections import defaultdict
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import io  # For creating in-memory file downloads
import os
import yfinance as yf

# Initialize session state to store multiple chat sessions and quiz state
if "chats" not in st.session_state:
    st.session_state.chats = defaultdict(lambda: pd.DataFrame(columns=["Name", "Amount", "Currency", "Category", "Date"]))
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Default"
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None

def switch_chat(chat_name):
    st.session_state.current_chat = chat_name

def add_chat(chat_name):
    if chat_name not in st.session_state.chats:
        st.session_state.chats[chat_name] = pd.DataFrame(columns=["Name", "Amount", "Currency", "Category", "Date"])


with st.sidebar:
    st.title("Expense Tracker Sessions")
    chat_name_input = st.text_input("New Chat Name", key="new_chat_name")
    if st.button("Create New Chat"):
        if chat_name_input:
            add_chat(chat_name_input)
            switch_chat(chat_name_input)
    
    st.write("## Existing Chats")
    for chat_name in st.session_state.chats.keys():
        if st.button(chat_name):
            switch_chat(chat_name)

    
    country_name = st.text_input("Enter your Country", "India")  # Default to "India"


st.title(f"Expense Tracker - {st.session_state.current_chat} Session")

# Expense input form
with st.form("expense_form"):
    st.subheader("Input Expense Details")
    expense_name = st.text_input("Expense Name", value="")
    expense_amount = st.number_input("Amount", min_value=0.01, step=0.01, value=0.01)
    expense_currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
    expense_category = st.text_input("Category (e.g., Food, Transport, etc.)", value="")
    expense_date = st.date_input("Date", value=datetime.today())
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if expense_name and expense_category:
            new_expense = {
                "Name": expense_name,
                "Amount": expense_amount,
                "Currency": expense_currency,
                "Category": expense_category,
                "Date": pd.to_datetime(expense_date)  # Ensure Date is stored as datetime64
            }
            current_chat_df = st.session_state.chats[st.session_state.current_chat]
            st.session_state.chats[st.session_state.current_chat] = pd.concat(
                [current_chat_df, pd.DataFrame([new_expense])], ignore_index=True
            )

            st.success("Expense added successfully!")
        else:
            st.error("Please fill all required fields!")

# Display expenses in table format
st.subheader("Entered Expenses")
expenses_df = st.session_state.chats[st.session_state.current_chat]
if not expenses_df.empty:
    st.dataframe(expenses_df)
else:
    st.write("No expenses added yet.")

# Analytics Section
if st.button("Generate Analytics"):
    st.session_state.calculate_analytics = True

if "calculate_analytics" in st.session_state and st.session_state.calculate_analytics:
    # Analytics section
    st.subheader("Analytics")

    # Total and average expenses
    total_expense = expenses_df["Amount"].sum()
    avg_expense = expenses_df["Amount"].mean()

    st.metric(label="Total Expenses", value=f"{total_expense:.2f}")
    st.metric(label="Average Expense", value=f"{avg_expense:.2f}")

    # Treemap Visualization
    st.write("### Treemap of Expense Categories")
    fig = px.treemap(expenses_df, path=["Category"], values="Amount", title="Expense Breakdown by Category")
    st.plotly_chart(fig)

    # Histogram of Expenses
    st.write("### Histogram of Expense Amounts")
    fig = px.histogram(expenses_df, x="Amount", nbins=20, title="Distribution of Expense Amounts")
    st.plotly_chart(fig)

    # Waterfall Chart for Monthly Expenses
    st.write("### Waterfall Chart of Monthly Expenses")
    expenses_df["Month"] = expenses_df["Date"].dt.to_period("M").astype(str)
    monthly_expenses = expenses_df.groupby("Month")["Amount"].sum().reset_index()
    waterfall_data = [{"label": row["Month"], "value": row["Amount"]} for _, row in monthly_expenses.iterrows()]
    fig = go.Figure(go.Waterfall(
        name="Monthly Expenses",
        orientation="v",
        x=[item["label"] for item in waterfall_data],
        y=[item["value"] for item in waterfall_data],
        connector=dict(line=dict(color="rgb(63, 63, 63)")),
    ))
    fig.update_layout(title="Monthly Expense Waterfall Chart")
    st.plotly_chart(fig)

    # Time-Series Forecasting
    st.write("### Time-Series Forecasting for Future Expenses")
    if len(monthly_expenses) > 2:  # Ensure there are enough data points for forecasting
        model = ExponentialSmoothing(monthly_expenses["Amount"], seasonal="add", seasonal_periods=12).fit()
        forecast = model.forecast(steps=6)  # Predict next 6 months
        forecast_df = pd.DataFrame({
            "Month": pd.date_range(start=pd.to_datetime(monthly_expenses["Month"].iloc[-1]) + pd.offsets.MonthBegin(1), periods=6, freq="MS").strftime("%Y-%m"),
            "Amount": forecast
        })
        forecast_combined = pd.concat([monthly_expenses, forecast_df], ignore_index=True)
        fig = px.line(forecast_combined, x="Month", y="Amount", title="Expense Forecasting")
        st.plotly_chart(fig)
    else:
        st.write("Not enough data for time-series forecasting.")

    
    st.subheader("Download Current Expenses")
    csv_data = expenses_df.to_csv(index=False)
    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name="expenses.csv",
        mime="text/csv"
    )

    # Upload CSV File for Insights
    st.subheader("Upload CSV File for Insights")
    uploaded_file = st.file_uploader("Upload your expenses CSV", type=["csv"])

    if uploaded_file:
        
        uploaded_expenses_df = pd.read_csv(uploaded_file)

        
        st.write("### Data from uploaded file:")
        st.dataframe(uploaded_expenses_df)

        # Mapping of country names to stock index symbols
        country_to_index = {
            "United States": "^GSPC",  # S&P 500 index
            "India": "^BSESN",  # Bombay Stock Exchange Sensex
            "Japan": "^N225",  # Nikkei 225
            "Germany": "^GDAXI",  # DAX index
            "UK": "^FTSE",  # FTSE 100 index
            "China": "000001.SS",  # Shanghai Composite
        }

        # Default to "India" if no valid input
        index_symbol = country_to_index.get(country_name, "^BSESN")

        # Fetch the stock data from Yahoo Finance
        try:
            index_data = yf.download(index_symbol, period="1mo", interval="1d")
            st.write(f"### Economic Data for {country_name}:")
            st.dataframe(index_data.tail(10))  # Show the last 10 days of data
        except Exception as e:
            st.error(f"Error fetching economic data for {country_name}: {str(e)}")

        
        combined_data = pd.concat([uploaded_expenses_df, index_data[['Close']]], axis=1)
        combined_data = combined_data.rename(columns={'Close': 'Economic Indicator'})

        
        prompt = (
            f"Expense data combined with economic data for {country_name}:\n{combined_data.to_string(index=False)}\n\n"
            "Based on the following combined data, provide insights on how the user can optimize their spending and start saving effectively. "
            "The user wants to manage their budget efficiently using only this platform, without the need for external tools or apps. "
            "The data includes expenses in different categories, currencies, amounts, and economic indicators. Even if the dataset is limited, generate practical, easy-to-apply tips that focus on reducing unnecessary spending, optimizing resources, and planning better for future expenses. "
            "Provide specific, actionable steps to manage finances, such as:\n"
            "- Identifying areas where the user can cut back without sacrificing essentials.\n"
            "- Offering suggestions for how to better allocate money across categories (e.g., food, transportation, entertainment).\n"
            "- Giving advice on how to create a more efficient and realistic budget based on the available data.\n"
            "- Offering basic tips on building savings or preparing for future expenses.\n"
            "If the dataset is incomplete, still provide general tips on financial management that can be applied universally without relying on external apps or services.\n"
            "Make sure to keep the points concise and short, and on point. Don't drag it unnecessarily."
        )

        
        try:
            import google.generativeai as genai
            genai.configure(api_key="YOUR_API_KEY")
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
            insights = response.text.strip()

            st.write("### Insights on Saving Money:")
            st.write(insights)

            # Generate Quiz Questions based on insights
            quiz_prompt = (
                f"Based on the following insights:\n\n{insights}\n\n"
                "Generate 5 multiple-choice questions. Each question should have 4 options, with only one correct answer."
            )

            quiz_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(quiz_prompt)
            quiz_questions = quiz_response.text.strip()

            st.write("### Quiz on Insights:")
            st.write(quiz_questions)

        except Exception as e:
            st.error(f"Error generating insights or quiz: {str(e)}")

# Quiz Section
if st.session_state.quiz_questions:
    st.subheader("Quiz Based on Insights")

    quiz_form = st.form("quiz_form")
    answers = {}

    for i, question in enumerate(st.session_state.quiz_questions):
        st.write(f"**{i+1}. {question}**")
        answers[i] = quiz_form.radio(f"Question {i+1}", ["Option 1", "Option 2", "Option 3", "Option 4"], key=f"q{i}")

    submitted_quiz = quiz_form.form_submit_button("Submit Quiz")

    if submitted_quiz:
        # For now, assume all correct answers are "Option 1" (placeholder logic)
        correct_answers = ["Option 1"] * len(st.session_state.quiz_questions)
        score = sum(1 for i, answer in answers.items() if answer == correct_answers[i])
        st.session_state.quiz_score = score

# Display Quiz Results
if st.session_state.quiz_score is not None:
    st.write(f"### Your Score: {st.session_state.quiz_score}/{len(st.session_state.quiz_questions)}")
