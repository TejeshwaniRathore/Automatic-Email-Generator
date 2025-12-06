import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Change if deployed elsewhere

# Title
st.title("📨 AI Email Reply Assistant")

# Fetch important emails
if st.button("Fetch Personal Emails"):
    with st.spinner("Fetching emails..."):
        response = requests.get(f"{API_URL}/emails")
        if response.status_code == 200:
            emails = response.json()
            st.session_state["emails"] = emails
            if not emails:
                st.info("No new personal emails found.")
        else:
            st.error(f"Failed to fetch emails: {response.text}")

# Display emails
emails = st.session_state.get("emails", [])
if emails:
    st.subheader("📬 Personal Emails Requiring a Reply")
    email_options = {f"{e['subject']} - {e['from']}": e for e in emails}
    selected_email = st.selectbox("Select an email:", list(email_options.keys()))

    if selected_email:
        email_info = email_options[selected_email]
        st.write(f"**From:** {email_info['from']}")
        st.write(f"**Subject:** {email_info['subject']}")
        st.markdown(f"**Body:** {email_info['body']}")

        # Clear previous reply if a new email is selected
        if st.session_state.get("current_message_id") != email_info["message_id"]:
            st.session_state["ai_reply"] = ""
            st.session_state["current_message_id"] = email_info["message_id"]

        # Generate reply
        if st.button("Generate AI Reply"):
            with st.spinner("Generating reply..."):
                reply_response = requests.post(
                    f"{API_URL}/generate-reply",
                    json={"message_id": email_info["message_id"]},
                )
                if reply_response.status_code == 200:
                    # The reply is now a JSON object with 'subject' and 'body'
                    st.session_state["ai_reply"] = reply_response.json().get("reply")
                else:
                    st.error(f"Failed to generate reply: {reply_response.text}")

        # Display reply and send button
        if st.session_state.get("ai_reply"):
            st.subheader("✍️ Generated Reply")
            
            reply_data = st.session_state["ai_reply"]
            
            reply_subject = st.text_input("Subject:", value=reply_data.get("subject", ""))
            reply_body = st.text_area("Body:", value=reply_data.get("body", ""), height=200)

            if st.button("Send Reply"):
                with st.spinner("Sending email..."):
                    send_payload = {
                        "message_id": email_info["message_id"],
                        "to": email_info["from"],
                        "subject": reply_subject,
                        "body": reply_body,
                    }
                    send_response = requests.post(f"{API_URL}/send-reply", json=send_payload)
                    if send_response.status_code == 200:
                        st.success("Reply sent successfully!")
                        st.session_state["ai_reply"] = "" # Clear reply after sending
                    else:
                        st.error(f"Failed to send reply: {send_response.text}")
else:
    st.info("Click **'Fetch Personal Emails'** to start.")
