import streamlit as st
import requests
import json
import uuid
import pandas as pd
from datetime import datetime
import io
import time
import os
import csv

# Import your existing functions (comment out the problematic import)
# from llm_as_judge import updated_response_llm_as_a_judge

# Initialize session state
if 'conversation_data' not in st.session_state:
    st.session_state.conversation_data = []
if 'current_depth' not in st.session_state:
    st.session_state.current_depth = 0
if 'flow_running' not in st.session_state:
    st.session_state.flow_running = False
if 'max_depth' not in st.session_state:
    st.session_state.max_depth = 6

# Your existing functions (copy from selfhelpGptFLow.py)
def generate_user_queries(query: str):
    """Generate follow-up queries using the LLM"""
    url = "http://gir.redbus.com/openai4/chat/completions"
    payload = json.dumps({
        "username": "mokshith.salian",
        "password": "Redbuss@2022!",
        "api": 40,
        "request": {
            "messages": [
                {
                    "role": "system",
                    "content": '''You are an autonomous evaluator and test query generator focused primarily on the domain of bus ticket services, including ticket cancellation, 
    rescheduling, ticket details retrieval, boarding and dropping point information, price and fare info, bus operator details, refund processing, and customer service escalation handling.
    And also You are a synthetic user simulator designed to mimic real-world users interacting with a virtual assistant for bus ticket-related services.

Your task is to generate realistic multi-turn conversations that begin with a standard service request but STRICTLY INCLUDE **organic follow-up questions or complaints** that represent **critical, dissatisfaction-driven or edge-case scenarios**.


Your role is to monitor a conversation between a user and an assistant (e.g., GPT) where the user is interacting with the assistant for any of the above tasks.

Your job is to:

1. Evaluate whether the assistant’s most recent message adheres to the expected task-specific flow.
2. Identify if the assistant should escalate the conversation to a human agent.
3. Classify any probing questions asked by the assistant during the process.
4. Generate new user queries based on the assistant’s most recent message, to test and challenge the service logic.

FLOW EVALUATION RULES (Extended with Escalation Case Injection)
Determine if the assistant’s response:

For cancellation: Follows this sequence:

User initiates cancellation  
User initiates partial cancellation
User initiates question for refund details 
User initiates question about Free cancellation opted or not 
Assistant checks eligibility
Assistant provides refund details (amount, time, method)  
User confirms or cancels
Assistant processes cancellation  
Assistant optionally requests feedback or offers further help  

**For Ticket Refunding**: Follow this sequence:
User initiates a query regarding refund
Assistant validates ticket or booking reference
Assistant confirms refund status (amount, method, timeline)
Assistant explains refund policy (e.g., deductions, refund window, non-refundable rules)
Assistant offers to assist with any related next steps (e.g., cancellation confirmation, escalation, or delay clarification)
Assistant asks if the user needs anything else and politely concludes if resolved
At any stage in this flow, the user may inject:
Dissatisfaction with the refund amount or deductions
User already received a refund communication but is not satisfied
Multiple payment deductions and refund not processed correctly
Refund delayed beyond promised time
Partial ticket cancellation refund issues
Bus operator cancelled the bus, and user is demanding full refund
User remains unhappy after apology or policy explanation
User claims redBus support did not help or delayed resolution
Legal threat or social media escalation is mentioned
The assistant must **respond appropriately** and **escalate to a human agent** if resolution cannot be offered or if the situation aligns with escalation rules.

 **For Ticket Rescheduling**:

Expected sequence:
- User initiates reschedule request  
- Assistant fetches original ticket details  
- Assistant provides alternate options (date/time/bus)  
- User selects a new schedule  
- Assistant confirms changes and any additional charges/refunds  
- Assistant completes the reschedule 
 At any stage in this flow, the user may inject:
- Partial ticket cancellation requested  
- Bus operator cancelled the bus  
- Bus operator cancellation reported more than 2 days later  
- User remains unhappy after apology from assistant  
- Customer expresses dissatisfaction with Redbus  
- Customer threatens or mentions social media/legal escalation 
The assistant must **respond appropriately** and **escalate to a human agent** if resolution cannot be offered or if the situation aligns with escalation rules.


 For **Ticket Details**: Expected sequence:

- User requests details for the ticket details
- User asks I need booking confirmation on email or SMS
- Assistant verifies identity or booking reference if needed  
- Assistant provides key information: ticket ID, passenger name, date, time, route, bus type, operator  
- Assistant confirms if anything else is needed (e.g., downloading ticket or boarding pass)  
- Assistant closes the loop politely or asks if the user needs help with cancellation/rescheduling
 Interruptible cases:
- Duplicate ticket booking reported  
- Multiple payment deductions reported  
- Seat was changed  
- Complaint arises after journey completion  
- Customer expresses dissatisfaction with Redbus  
- Complaint against Redbus customer care  
- Customer threatens or mentions social media/legal escalation  
These may appear as follow-up interjections. The assistant should **not dismiss them** and must **offer agent handoff** when user remains unsatisfied.

 For **Boarding/Dropping Point**: Expected sequence:

- User asks about boarding or dropping point  
- Assistant verifies ticket or PNR if needed  
- Assistant fetches and displays boarding/dropping location with time and coordinates if available  
- Assistant optionally offers map links or operator contact if user is unfamiliar  
- Assistant confirms if user needs further help and transitions smoothly
 Interruptible concerns:
- Boarding/dropping point was changed and user is dissatisfied  
- Customer disputes boarding point change or refuses to travel  
- Bus was delayed  
- User was not allowed to board  
- Bus did not arrive  
- Driver demanded extra fare  

For **CASE UPDATE QUERIES** :Expected sequence:

- User asks for case updates or complaint status
- User asks for case number and comments
- Assistant verifies user identity or case reference
- Assistant fetches and provides current status of the case or complaint
- Assistant explains next steps or expected resolution time
- Assistant confirms if user needs further assistance or has additional questions
- Assistant closes the loop politely or asks if the user needs help with cancellation/rescheduling
Interruptible concerns:
- User expresses dissatisfaction with case handling or resolution
- User demands immediate resolution or threatens escalation
- User claims case was mishandled or not addressed properly
- User threatens or mentions social media/legal escalation
- User demands to speak with a human agent immediately
**strictly follow this sequence**      

These concerns require the assistant to **acknowledge, not deflect**, and escalate if the issue cannot be addressed directly or if it violates terms of service 

 For **Price/Fare Information**: Expected sequence:

- User requests fare details  
- Assistant confirms the route or ticket details  
- Assistant provides total price with breakdown (base fare, taxes, etc.)  
- Assistant optionally explains dynamic pricing if price seems high  
- Assistant closes with options to view alternate dates or buses if asked
 Interruptible scenarios:
- Multiple payment deductions reported  
- Duplicate booking  
- Customer dissatisfied with price logic or refund terms  
- Customer expresses dissatisfaction with Redbus  
- Complaint arises after journey completion  
- Customer threatens or mentions legal/social action  

If the assistant fails to justify or remedy, **agent escalation is mandatory**.

 For **Bus Information**: Expected sequence:

- User requests Bus details  
- Assistant confirms the route or ticket details  
- Assistant provides total price with breakdown (base fare, taxes, etc.)  
- Assistant optionally explains the bus amenities 
- Assistant closes with options to view alternate dates or buses if asked
Interruptible scenarios:
- Multiple payment deductions reported  
- Duplicate booking  
- Customer dissatisfied with price logic or refund terms  
- Customer expresses dissatisfaction with Redbus  
- Complaint arises after journey completion  
- Customer threatens or mentions legal/social action  

If the assistant fails to justify or remedy, **agent escalation is mandatory**.

 For **Train Details query**: Expected sequence:

- User requests Train details
- User asks Where is my train?
- User asks Latest status of my train?
- User asks When will my train reach xx station
- User asks What is the latest status of my ticket / PNR
- User asks Coach Position Check
- User asks Meaning of Status <WL/RAC/ etc.>
- User asks Need help with ticket details
- User asks I need booking confirmation on email or SMS
- User asks Ticket cancellation        
- User want to cancel my ticket
- User asks Any other info on FC / Cancellation
- User asks Information on Seat Guarantee
- User Can you infor me when my PNR status updates (PNR subscription)
- User When will my train reach xx station
- Assistant confirms the route or ticket details  
- Assistant provides total price with breakdown (base fare, taxes, etc.)  
- Assistant optionally explains the bus amenities 
- Assistant closes with options to view alternate dates or buses if asked
- Assistant Retrieves live status information for a specific train.
- Assistant Checks current status of a railway booking using PNR number.
- Assistant Provides information about coach positions in a train.
- Assistant Provides a complete schedule of a specific train.
- Assistant Retrieves user's booking history.
- Assistant Subscribes users to PNR status updates.
- Assistant  Subscribes users to PNR status updates.
  Interruptible concerns:
- Payment debited twice
- My train hasn't reached yet

If the assistant fails to justify or remedy, **agent escalation is mandatory**.

For **Bus Operator Details**: Expected sequence:

- User asks about the bus or operator  
- Assistant identifies the booked service or asks for route/date  
- Assistant shares name, service rating (if applicable), contact/helpdesk number, amenities offered  
- Assistant addresses any concern about bus/operator professionalism or punctuality if raised  
- Assistant closes by offering to help with related tasks (reschedule, refund, etc.)
 Relevant escalations:
- Bus broke down  
- Poor bus quality complaint  
- Amenities not provided  
- Driver demanded extra fare  
- Bus delayed or didn’t show  
- Seat was changed  
- Complaint against Redbus customer care  
- Customer still unhappy after apology  
- Legal/social media escalation mentioned  

These user issues must **trigger escalation** when not resolvable by the assistant, especially post-journey or when user demands agent involvement.

All escalation cases must be captured by the assistant mid-flow. If escalation is needed but **not initiated**, flag the assistant response as **flow break**.

 Provides accurate, relevant, and supportive information  
 Maintains continuity of the task at hand  
 Avoids off-topic diversions or interruptions

DO NOT TERMINATE THE FLOW 
Do **not** mark the flow as broken if the assistant's message offers an appropriate next step such as:

- Connecting the user to a human agent
- Redirecting the user to the correct responsible party (e.g., bus operator), **while acknowledging the concern**
- Offering follow-up assistance or confirming if escalation is required
- Providing user information like personal mobile number or Personal email adress of the user.
- The assistant response did not adhere to the expected task-specific flow. 
- The user query addressing bus operator policies was met with an information statement instead of a direct confirmation or escalation path. 
- A users concern or request for more specific details was not appropriately acknowledged.

** STRICTLY FOLLOW ONLY TRAIN RELATED QUERIES , DO NOT GO TO BUS FLOW SEQUENCE**

In escalation-prone scenarios (e.g., post-journey complaint, refund dissatisfaction, bus cancellation), the flow should continue **if** the assistant:
- **Acknowledges the issue clearly**
- **Does not deflect or ignore the user's concern**
- Provides **an escalation path** (agent connect, operator referral, ticket creation)

**DO NOT** Break the flow in any case **Keep on Asking questions**

PROBING QUESTION CLASSIFICATION  
For each assistant question, classify it as one of:
Valid Curiosity → Clarifies intent or confirms user action (e.g., "Do you want to proceed with the cancellation?")  
Flow-breaking → Introduces unrelated or distracting content  
Divergent But Tolerable → Slightly off-topic but acceptable for UX (e.g., optional feedback)

DYNAMIC TEST QUERY GENERATION  
If the flow is valid and continuous, generate 2-3 realistic next user queries that:
Fit logically as the next user input.
Stay strictly within the respective task domain (cancellation, rescheduling, escalation, etc.).  
Stress-test the assistant’s logic (e.g., partial refunds, delayed buses, post-journey complaints)

Return these in the following Json format like:
{{
  "possible_user_responses": [
    "query1"
  ]
}}

user_queries: {user_queries_with_response}

### **Output Format:**  
Output should be in json format. Don't add any other field to the output.
'''.format(user_queries_with_response=query)
                }
            ]
        }
    })

    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        response_json = response.json()
        
        if "response" in response_json and response_json["response"]:
            content = response_json["response"]["openAIResponse"]["choices"][0]["message"]["content"]
            
            # Clean and parse JSON
            if "json" in content:
                content = content.replace("```json", "").replace("```", "").strip()
            
            parsed_response = json.loads(content)
            return parsed_response.get("possible_user_responses", [])
    except Exception as e:
        st.error(f"Error generating queries: {e}")
        return ["I'm not satisfied with this response", "Can you escalate this to a human agent?"]

def get_assistant_response(question: str, orderuuid: str):
    """Get response from the assistant API"""
    api_url = "http://selfhelp-gpt.redbus.com:17714/chat/query"
    payload = json.dumps({
        "message": question,
        "orderItemUUID": orderuuid
    })

    headers = {
        "X-CLIENT": "SELF_HELP",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, headers=headers, data=payload, verify=False, timeout=30)
        response_data = response.json()
        return response_data["data"]["message"], response_data["data"]["caseCreationFlag"]
    except Exception as e:
        st.error(f"Error getting assistant response: {e}")
        return f"I understand your query about '{question}'. Let me help you with that. Due to a technical issue, I'll need to connect you with our support team.", True

def build_single_turn(user_query: str, depth: int, orderuuid: str = "b5c464b033f7e0067b069bf904020100"):
    """Build a single conversation turn"""
    node_id = str(uuid.uuid4())[:8].upper()
    
    # Get assistant response
    assistant_response, case_creation = get_assistant_response(user_query, orderuuid)
    
    conversation_turn = {
        "timestamp": datetime.now().isoformat(),
        "depth": depth,
        "node_id": node_id,
        "case_creation": case_creation,
        "user_query": user_query,
        "assistant_response": assistant_response
    }
    
    return conversation_turn

def save_conversation_to_files(conversation_data):
    """Save conversation data to CSV and JSON files"""
    # Save to CSV
    csv_file = 'streamlit_conversation.csv'
    write_headers = not os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        if conversation_data:
            writer = csv.DictWriter(file, fieldnames=conversation_data[0].keys())
            if write_headers:
                writer.writeheader()
            for turn in conversation_data:
                writer.writerow(turn)
    
    # Save to JSON
    json_file = 'streamlit_conversation.json'
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(conversation_data, file, indent=2, ensure_ascii=False)

def main():
    st.set_page_config(
        page_title="Conversation Flow Tester",
        page_icon="💬",
        layout="wide"
    )
    
    st.title("🤖 AI Conversation Flow Tester")
    st.markdown("Generate and analyze multi-turn conversations for train/bus ticket services")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.session_state.max_depth = st.slider("Max Conversation Depth", min_value=1, max_value=15, value=6)
        
        st.header("📋 Flow Options")
        flow_options = {
            "Ticket Cancellation": "I want to cancel this ticket, can i cancel this",
            "Ticket Details": "what is the latest status of my Tin",
            "Ticket Reschedule": "I want to reschedule my ticket",
            "Bus/Train Information": "where is my bus right now",
            "Refund Details": "My payment was debited twice",
            "Train/Bus Details": "what is my coach position",
            "Case Updates Query": "what is the status of my complaint",
        }
        
        selected_flow = st.selectbox("Select Flow Type", list(flow_options.keys()))
        
        # Custom query option
        st.subheader("🔧 Custom Query")
        custom_query = st.text_area(
            "Enter custom initial query:",
            placeholder="Enter your custom query here...",
            height=100
        )
        
        # Export options
        st.header("📥 Export Options")
        if st.session_state.conversation_data:
            
            # Download as CSV
            df = pd.DataFrame(st.session_state.conversation_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name=f"conversation_flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Download as JSON
            json_str = json.dumps(st.session_state.conversation_data, indent=2)
            st.download_button(
                label="📋 Download JSON",
                data=json_str,
                file_name=f"conversation_flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🚀 Start Conversation Flow")
        
        # Action buttons
        button_col1, button_col2, button_col3 = st.columns(3)
        
        with button_col1:
            if st.button("▶️ Start Predefined Flow", type="primary", disabled=st.session_state.flow_running):
                if selected_flow:
                    initial_query = flow_options[selected_flow]
                    st.session_state.conversation_data = []
                    st.session_state.current_depth = 0
                    st.session_state.flow_running = True
                    st.session_state.initial_query = initial_query
                    st.rerun()
        
        with button_col2:
            if st.button("🔧 Start Custom Flow", disabled=st.session_state.flow_running or not custom_query.strip()):
                if custom_query.strip():
                    st.session_state.conversation_data = []
                    st.session_state.current_depth = 0
                    st.session_state.flow_running = True
                    st.session_state.initial_query = custom_query.strip()
                    st.rerun()
        
        with button_col3:
            if st.button("🛑 Stop & Reset"):
                st.session_state.conversation_data = []
                st.session_state.current_depth = 0
                st.session_state.flow_running = False
                if 'initial_query' in st.session_state:
                    del st.session_state.initial_query
                st.rerun()
        
        # Process conversation flow
        if st.session_state.flow_running and 'initial_query' in st.session_state:
            
            # Build conversation turn by turn
            if st.session_state.current_depth == 0:
                # First turn
                with st.spinner("Getting assistant response..."):
                    turn = build_single_turn(st.session_state.initial_query, st.session_state.current_depth)
                if turn:
                    st.session_state.conversation_data.append(turn)
                    st.session_state.current_depth += 1
                    time.sleep(1)
                    st.rerun()
            
            elif st.session_state.current_depth < st.session_state.max_depth:
                # Generate follow-up and continue
                last_response = st.session_state.conversation_data[-1]["assistant_response"]
                
                with st.spinner("Generating follow-up queries..."):
                    follow_ups = generate_user_queries(last_response)
                
                if follow_ups:
                    next_query = follow_ups[0]
                    with st.spinner(f"Processing turn {st.session_state.current_depth + 1}..."):
                        turn = build_single_turn(next_query, st.session_state.current_depth)
                    if turn:
                        st.session_state.conversation_data.append(turn)
                        st.session_state.current_depth += 1
                        time.sleep(1)
                        st.rerun()
                else:
                    st.warning("No follow-up queries generated. Ending conversation.")
                    st.session_state.flow_running = False
                    save_conversation_to_files(st.session_state.conversation_data)
            else:
                st.success("✅ Conversation flow completed!")
                st.session_state.flow_running = False
                save_conversation_to_files(st.session_state.conversation_data)
        
        # Display conversation
        if st.session_state.conversation_data:
            st.header("💬 Conversation Flow")
            
            for i, turn in enumerate(st.session_state.conversation_data):
                with st.expander(f"Turn {turn['depth'] + 1} - {turn['node_id']}", expanded=True):
                    col_user, col_assistant = st.columns(2)
                    
                    with col_user:
                        st.markdown("**👤 User:**")
                        st.info(turn["user_query"])
                    
                    with col_assistant:
                        st.markdown("**🤖 Assistant:**")
                        st.success(turn["assistant_response"])
                    
                    # Metadata
                    st.caption(f"Case Creation: {'✅' if turn['case_creation'] else '❌'} | Time: {turn['timestamp']}")
    
    with col2:
        st.header("📊 Flow Statistics")
        
        if st.session_state.conversation_data:
            # Basic stats
            total_turns = len(st.session_state.conversation_data)
            case_creations = sum(1 for turn in st.session_state.conversation_data if turn["case_creation"])
            
            st.metric("Total Turns", total_turns)
            st.metric("Case Creations", case_creations)
            st.metric("Escalation Rate", f"{(case_creations/total_turns)*100:.1f}%" if total_turns > 0 else "0%")
            
            # Turn details
            st.subheader("📋 Turn Summary")
            for turn in st.session_state.conversation_data:
                status = "🚨" if turn["case_creation"] else "✅"
                st.write(f"{status} Turn {turn['depth'] + 1}: {turn['node_id']}")
        else:
            st.info("Start a conversation flow to see statistics")
        
        # Progress indicator
        if st.session_state.flow_running:
            progress = st.session_state.current_depth / st.session_state.max_depth
            st.progress(progress)
            st.caption(f"Progress: {st.session_state.current_depth}/{st.session_state.max_depth} turns")

if __name__ == "__main__":
    main()