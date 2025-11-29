class Train:
    def __init__(self,train_no,train_name,train_type,zone):
        # train_no stores the unique train number like 12345
        self.train_no=train_no
        # train_name holds the name of the train
        self.train_name=train_name
        # train_type tells if its Express or Passenger etc
        self.train_type=train_type
        # zone is the railway zone like South Central etc
        self.zone=zone
    
    def train_details(self):
        # details is a tuple that packs all train info together
        details=(self.train_no,self.train_name,self.train_type,self.zone)
        return details
    
    def get_number(self):
        # n is just a copy of train number to return
        n=self.train_no
        return n
    

class Schedule_entry:
    def __init__(self,train,platform_no,departure_days,arrival_time,departure_time,passing_through,from_station,to_station):
        # train object contains all train details
        self.train=train
        # platform_no is which platform like 1, 2, 3
        self.platform_no=platform_no
        # departure_days is list of days train runs like Mon, Tue
        self.departure_days=departure_days
        # arrival_time when train arrives in 24hr format
        self.arrival_time=arrival_time
        # departure_time when train leaves the station
        self.departure_time=departure_time
        # passing_through is True if train doesnt stop
        self.passing_through=passing_through
        # from_station is where train is coming from
        self.from_station=from_station
        # to_station is the destination
        self.to_station=to_station
        # status tracks if train is on time or delayed
        self.status="On Time"

    def update_platform(self,new_platform_no):
        self.platform_no=new_platform_no
    
    def update_arrival_departure(self,new_arrival_time,new_departure_time):
        self.arrival_time=new_arrival_time
        self.departure_time=new_departure_time
    
    def mark_passing_through(self,passing_time):
        self.passing_through=True
        self.arrival_time=None
        self.departure_time=None
        self.passing_time=passing_time

    def next_event(self,current_time):
        if self.passing_through==True:
            msg="Passing through at "+str(self.passing_time)
            return msg
        
        if current_time<self.arrival_time:
            msg="Arrival at "+str(self.arrival_time)
            return msg
        if current_time<self.departure_time:
            msg="Departure at "+str(self.departure_time)
            return msg
        
        return "Train has departed"
        
class Platform:
    def __init__(self,platform_no):
        # platform_no identifies this platform
        self.platform_no=platform_no
        # scheduled_trains is list of all trains scheduled on this platform
        self.scheduled_trains=[]
    
    def add_train_schedule(self,schedule_entry):
        self.scheduled_trains.append(schedule_entry)
    
    def remove_train_schedule(self,schedule_entry):
        if schedule_entry in self.scheduled_trains:
            self.scheduled_trains.remove(schedule_entry)
    
    def arrivals_in_next_hour(self,current_time):
        # arrivals stores all trains arriving in next hour
        arrivals=[]
        # i is loop counter to go through all trains
        i=0
        while i<len(self.scheduled_trains):
            # entry is current train schedule we are checking
            entry=self.scheduled_trains[i]
            if entry.passing_through==True:
                i=i+1
                continue
            if entry.arrival_time>current_time:
                if entry.arrival_time<=current_time+1:
                    arrivals.append(entry)
            i=i+1
        return arrivals
    
    def upcoming_departures(self,current_time):
        departures=[]
        idx=0
        num_trains=len(self.scheduled_trains)
        while idx<num_trains:
            t=self.scheduled_trains[idx]
            if t.passing_through==True:
                idx+=1
                continue
            if t.departure_time>current_time:
                departures.append(t)
            idx+=1
        return departures

class Station:
    def __init__(self,name):
        # station_name is the name like Durg or Mumbai etc
        self.station_name=name
        # platforms dictionary maps platform numbers to Platform objects
        self.platforms={}  # dictionary of platforms
        # schedules list keeps all train schedules at this station
        self.schedules=[]  # list of all train schedules
    
    def add_platform(self,platform_no):
        already_exists=platform_no in self.platforms
        if not already_exists:
            p=Platform(platform_no)
            self.platforms[platform_no]=p
    
    def get_platform(self,platform_no):
        if platform_no in self.platforms:
            platform_obj=self.platforms[platform_no]
            return platform_obj
        return None
    
    def add_schedule(self,entry):
        # add to master schedule list
        self.schedules.append(entry)
        platform_no=entry.platform_no
        p=self.get_platform(platform_no)
        if p!=None:
            p.add_train_schedule(entry)
        
    def find_train_no(self,train_no):
        # search through all schedules
        # result will store the found schedule or None
        result=None
        # i is counter for loop
        i=0
        # schedule_count is total number of schedules
        schedule_count=len(self.schedules)
        while i<schedule_count:
            # sched is current schedule entry being checked
            sched=self.schedules[i]
            # train_number extracted from current schedule
            train_number=sched.train.train_no
            if train_number==train_no:
                result=sched
                break
            i+=1
        return result
    

    def change_platform(self,train_no,new_platform_no):
        # sched holds the train schedule we want to change
        sched=self.find_train_no(train_no)
        if sched==None:
            print("Train not found in schedule")
            return
        
        # current_platform_no is where train is scheduled now
        current_platform_no=sched.platform_no
        # current_platform is the Platform object train is on now
        current_platform=self.get_platform(current_platform_no)
        # target_platform is the new Platform object we moving to
        target_platform=self.get_platform(new_platform_no)
        
        # remove from old platform
        if current_platform!=None:
            current_platform.remove_train_schedule(sched)
        # update entry
        sched.update_platform(new_platform_no)
        # add to new platform
        if target_platform!=None:
            target_platform.add_train_schedule(sched)

    def update_train_timing(self,train_no,new_arrival_time,new_departure_time):
        sched=self.find_train_no(train_no)
        if sched==None:
            print("Train not found in schedule")
            return
        else:
            sched.update_arrival_departure(new_arrival_time,new_departure_time)

    def arrivals_next_hour(self,current_time):
        all_arrivals=[]
        p_numbers=list(self.platforms.keys())
        i=0
        while i<len(p_numbers):
            p_num=p_numbers[i]
            p_obj=self.platforms[p_num]
            p_arrivals=p_obj.arrivals_in_next_hour(current_time)
            # add all arrivals to result
            j=0
            while j<len(p_arrivals):
                all_arrivals.append(p_arrivals[j])
                j+=1
            i+=1
        return all_arrivals
    
class Station_Master:
    def __init__(self,station):
        self.station=station
    
    def schedule_new_train(self,train_no,name,train_type,zone,platform_no,departure_days,arrival_time,departure_time,passing_through,from_station,to_station):
        t=Train(train_no,name,train_type,zone)
        from_station=self.station.station_name
        e=Schedule_entry(t,platform_no,departure_days,arrival_time,departure_time,passing_through,from_station,to_station)
        self.station.add_platform(platform_no)
        self.station.add_schedule(e)

    def re_assign_platform(self,train_no,new_platform_no):
        self.station.add_platform(new_platform_no)
        self.station.change_platform(train_no,new_platform_no)

    def _update_train_schedule(self,train_no,new_arrival_time,new_departure_time):
        self.station.update_train_timing(train_no,new_arrival_time,new_departure_time)

    def mark_train_passing_through(self,train_no,passing_time):
        entry=self.station.find_train_no(train_no)
        if entry==None:
            print("Train not found")
            return
        else:
            entry.mark_passing_through(passing_time)

    
class Interface:
    def __init__(self,station):
        self.station=station
    
    def display_arrivals_next_hour(self,current_time):
        arrivals=self.station.arrivals_next_hour(current_time)
        # print header
        header="\nArrivals in next hour from "+str(current_time)+":"
        print(header)
        col_headers="No. | Name | Type | Zone | PF | From | Arr | To | Dep"
        print(col_headers)
        line="-"*80
        print(line)
        
        count=len(arrivals)
        if count==0:
            print("No arrivals in the next hour")
            return
        
        # loop through arrivals
        idx=0    
        while idx<count:
           entry=arrivals[idx]
           t_details=entry.train.train_details()
           train_num=t_details[0]
           train_name=t_details[1]
           train_type=t_details[2]
           train_zone=t_details[3]
           platform=entry.platform_no
           source=entry.from_station
           arrival=entry.arrival_time
           destination=entry.to_station
           departure=entry.departure_time
           # build output string
           line_output=str(train_num)+" | "+str(train_name)+" | "+str(train_type)+" | "+str(train_zone)+" | "+str(platform)+" | "+str(source)+" | "+str(arrival)+" | "+str(destination)+" | "+str(departure)
           print(line_output)
           idx+=1

    def display_departures(self,current_time):
        # collect departures from all platforms
        all_departures=[]
        platform_keys=list(self.station.platforms.keys())
        k=0
        while k<len(platform_keys):
            p_no=platform_keys[k]
            p=self.station.platforms[p_no]
            p_departures=p.upcoming_departures(current_time)
            d=0
            while d<len(p_departures):
                all_departures.append(p_departures[d])
                d+=1
            k=k+1
        
        # display header
        header="\nDepartures after "+str(current_time)+":"
        print(header)
        col_headers="No. | Name | Type | Zone | PF | From | Arr | To | Dep"
        print(col_headers)
        separator="-"*80
        print(separator)
        
        total_departures=len(all_departures)
        if total_departures==0:
            print("No upcoming departures")
            return
        
        # display all departures
        i=0    
        while i<total_departures:
           e=all_departures[i]
           t_details=e.train.train_details()
           train_num=t_details[0]
           train_name=t_details[1]
           train_type=t_details[2]
           train_zone=t_details[3]
           platform=e.platform_no
           source=e.from_station
           arrival=e.arrival_time
           destination=e.to_station
           departure=e.departure_time
           line_output=str(train_num)+" | "+str(train_name)+" | "+str(train_type)+" | "+str(train_zone)+" | "+str(platform)+" | "+str(source)+" | "+str(arrival)+" | "+str(destination)+" | "+str(departure)
           print(line_output)
           i+=1
            
   


def main():
    # initialize station
    # stn_name is the station name we are managing
    stn_name="Durg"
    # s is the main Station object
    s=Station(stn_name)
    # master is Station_Master who manages scheduling
    master=Station_Master(s)
    # ui is Interface for displaying information
    ui=Interface(s)

    # print welcome message
    empty_line="\n"
    print(empty_line)
    print(empty_line)
    equals="="
    line=equals*50
    print(line)
    msg="Train Station Management System of "+stn_name
    print(msg)
    print(line)
    print(empty_line)

    # add platforms
    max_p=3
    platform_counter=1
    done=False
    while not done:
        s.add_platform(platform_counter)
        platform_counter=platform_counter+1
        if platform_counter>max_p:
            done=True

    # add initial trains
    adding=1
    while adding==1:
        q="\nDo you want to add a new train schedule? (yes/no): "
        response=input(q)
        response=response.strip()
        response=response.lower()
        yes_check="yes"
        if response==yes_check:
            adding=1
        else:
            adding=0
            break
            
        print("\nEnter Train Details:")
        t_number=input("Train Number: ")
        t_name=input("Train Name: ")
        t_category=input("Train Type (Express/Passenger/etc): ")
        z=input("Zone: ")
        pf_input=input("Platform Number (1-3): ")
        pf_number=int(pf_input)
        
        days_input=input("Running days (e.g., Mon,Tue,Wed): ")
        days_arr=days_input.split(',')
        
        a_input=input("Arrival Time (24hr format, e.g., 14): ")
        a_time=int(a_input)
        d_input=input("Departure Time (24hr format): ")
        d_time=int(d_input)
        
        origin=s.station_name
        dest_input=input("Destination Station: ")
        
        stop_q="Does train stop at this station? (yes/no): "
        stop_ans=input(stop_q)
        stop_ans=stop_ans.strip()
        stop_ans=stop_ans.lower()
        pass_flag=1
        if stop_ans=="yes":
            pass_flag=0
        is_passing=False
        if pass_flag==1:
            is_passing=True

        master.schedule_new_train(t_number,t_name,t_category,z,pf_number,days_arr,a_time,d_time,is_passing,origin,dest_input)
        succ="\nTrain schedule added successfully!"
        print(succ)

    # main menu
    continue_running=1
    while continue_running==1:
        newline="\n"
        print(newline)
        sep_char="="
        sep_line=sep_char*50
        print(sep_line)
        menu_title="MAIN MENU"
        print(menu_title)
        print(sep_line)
        opt1="1. View Arrivals in Next Hour"
        opt2="2. View Upcoming Departures"
        opt3="3. Re-assign Platform to a Train"
        opt4="4. Update Train Schedule"
        opt5="5. Mark Train as Passing Through"
        opt6="6. Exit"
        print(opt1)
        print(opt2)
        print(opt3)
        print(opt4)
        print(opt5)
        print(opt6)
        print(sep_line)

        prompt="\nEnter your choice (1-6): "
        user_choice=input(prompt)
        user_choice=user_choice.strip()

        one="1"
        if user_choice==one:
            t_prompt="Enter current time (24hr format): "
            t_str=input(t_prompt)
            t_int=int(t_str)
            ui.display_arrivals_next_hour(t_int)

        two="2"
        if user_choice==two:
            t_prompt="Enter current time (24hr format): "
            t_str=input(t_prompt)
            t_int=int(t_str)
            ui.display_departures(t_int)

        three="3"
        if user_choice==three:
            t_num_prompt="\nEnter Train Number to re-assign: "
            t_num=input(t_num_prompt)
            p_prompt="New Platform Number: "
            p_str=input(p_prompt)
            p_int=int(p_str)
            master.re_assign_platform(t_num,p_int)
            success="Platform re-assigned successfully!"
            print(success)
        
        four="4"
        if user_choice==four:
            t_num_prompt="\nEnter Train Number: "
            t_num=input(t_num_prompt)
            a_prompt="New Arrival Time (24hr): "
            a_str=input(a_prompt)
            a_int=int(a_str)
            d_prompt="New Departure Time (24hr): "
            d_str=input(d_prompt)
            d_int=int(d_str)
            master._update_train_schedule(t_num,a_int,d_int)
            success="Schedule updated successfully!"
            print(success)

        five="5"
        if user_choice==five:
            t_num_prompt="\nEnter Train Number: "
            t_num=input(t_num_prompt)
            p_time_prompt="Passing Time (24hr): "
            p_time_str=input(p_time_prompt)
            p_time_int=int(p_time_str)
            master.mark_train_passing_through(t_num,p_time_int)
            success="Train marked as passing through!"
            print(success)

        six="6"
        if user_choice==six:
            bye_msg="\nExiting system. Goodbye!"
            print(bye_msg)
            continue_running=0

        valid_choices=["1","2","3","4","5","6"]
        is_valid=False
        idx=0
        while idx<len(valid_choices):
            if user_choice==valid_choices[idx]:
                is_valid=True
                break
            idx=idx+1
        if is_valid==False:
            error_msg="\nInvalid choice! Please enter 1-6."
            print(error_msg)
    
if __name__ == "__main__":
    main()
    

