import streamlit as st

def history_keeper(history):
    for role, message in history:
        print(message)
        if role == "User":
            st.markdown(
                f"""
                <div style="color:black;background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: left;">
                    {message.strip()}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="color:black;background-color: #E3E3E3; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: left;">
                    {message}
                </div>
                """,
                unsafe_allow_html=True
            )