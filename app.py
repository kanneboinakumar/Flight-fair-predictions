import streamlit as st
import pandas as pd
import pickle
st.title("Flight Fair Predictions")

# model
pickle_in = open("Selection.pkl","rb")
Model=pickle.load(pickle_in)

# predict
def predict_note_authentication(values):
    ans=Model.predict(values)
    return ans
def main():
    st.title("Flight Fair Predictions")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit Wine quality ML App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    
    # Airline selection
    Airline_options = ['Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 
                       'SpiceJet', 'Vistara', 'Air Asia', 'GoAir', 
                       'Multiple carriers Premium economy', 'Jet Airways Business', 
                       'Vistara Premium economy', 'Trujet']
    Airline = st.selectbox('Airline', options=Airline_options)
    Airline_dict = {'Jet Airways': 3849, 'IndiGo': 2053, 'Air India': 1751, 
                    'Multiple carriers': 1196, 'SpiceJet': 818, 'Vistara': 479, 
                    'Air Asia': 319, 'GoAir': 194, 'Multiple carriers Premium economy': 13, 
                    'Jet Airways Business': 6, 'Vistara Premium economy': 3, 'Trujet': 1}
    Airline_value = Airline_dict.get(Airline, 0)  # default to 0 if not found
    
    # Total Stops selection
    Total_Stops_options = ['non-stop', '1 stop', '2 stops', '3 stops', '4 stops']
    Total_Stops = st.selectbox('Total Stops', options=Total_Stops_options)
    Total_Stops_dict = {'non-stop': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3, '4 stops': 4}
    Total_Stops_value = Total_Stops_dict.get(Total_Stops, 0)  # default to 0 if not found
    
    # Date_of_Journey
    Date_of_Journey=st.date_input('Date_of_Journey')
    Day_of_Journey=pd.to_datetime(Date_of_Journey).day
    Month_of_Journey=pd.to_datetime(Date_of_Journey).month
    
    # Dep_Time
    Dep_Time=st.text_input("Departure Time (HH:MM)", "10:00")
    # Convert Dep_Time to string in the format "HH:MM"
    time_dep = pd.to_datetime(Dep_Time, format='mixed')
    Dep_hour=time_dep.hour
    Dep_min=time_dep.minute
    
    # Arrival_Time
    Arrival_Time=st.text_input("Arrival Time (HH:MM)", "13:30")
    time_arr = pd.to_datetime(Arrival_Time, format='mixed')
    Arrival_hour=time_arr.hour
    Arrival_min=time_arr.minute
    
    # Duration
    departure_hour, departure_minute = map(int, Dep_Time.split(':'))
    arrival_hour, arrival_minute = map(int, Arrival_Time.split(':'))
    Duration_hour = arrival_hour - departure_hour   # Calculate the duration
    Duration_minute = arrival_minute - departure_minute

    if Duration_minute < 0:
        Duration_hour -= 1
        Duration_minute += 60
        
    Duration_in_min = Duration_hour*60 + Duration_minute
    
    # In-flight meal not included
    In_flight_meal_not_included=st.selectbox('In-flight meal not included',options=['yes','no'])
    if In_flight_meal_not_included=='yes':
        In_flight_meal_not_included=1
    else:
        In_flight_meal_not_included=0
        
    # No check-in baggage included
    No_check_in_baggage_included=st.selectbox('No check-in baggage included',options=['yes','no'])
    if No_check_in_baggage_included=='yes':
        No_check_in_baggage_included=1
    else:
        No_check_in_baggage_included=0
    
    # Source
    Source=st.selectbox('Source',options=['Banglore','Chennai','Delhi','Kolkata','Mumbai'])
    source_index = ['Banglore', 'Chennai', 'Delhi', 'Kolkata', 'Mumbai']
    source_value = [1 if src == Source else 0 for src in source_index]
    
    # Destination
    Destination=st.selectbox('Destination',options=['Banglore',
                                                    'Cochin',
                                                    'Delhi',
                                                    'Hyderabad',
                                                    'Kolkata'])
    destination_index = ['Banglore', 'Cochin', 'Delhi', 'Hyderabad', 'Kolkata']
    destination_value = [1 if dest == Destination else 0 for dest in destination_index]
        
    values=[Airline_value, Total_Stops_value, Day_of_Journey, Month_of_Journey,
            Dep_hour, Dep_min, Arrival_hour, Arrival_min, Duration_in_min,
            In_flight_meal_not_included, No_check_in_baggage_included]+source_value+destination_value
    
    if st.button("Predict"):
        result=predict_note_authentication(values)
        st.success(result)
    
if __name__ == "__main__":
    main()