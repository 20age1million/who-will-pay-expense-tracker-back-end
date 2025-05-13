import json
import os

class opData:
    def __init__(self, filename="default"):     # filename is optional ,so can change the data file using
        base_dir = os.path.dirname(os.path.abspath(__file__))   # get path of current file
        self.filepath = os.path.join(base_dir, "data", f"{filename}.json")  # join files to get json's path

    def getDisplayData(self):
        '''return {alice : [amount of payment, number of payment], bob : [a, n], ...}'''
        print(f"✅{self.filepath} has been visited")
        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        result = {}
        for person in data:
            result[person["name"]] = [0,0]
            for record in person["records"]:
                (result[person["name"]])[0] += round(float(record["amount"]), 2)
                (result[person["name"]])[1] += 1
        return result
    
    def getNextPayment(self):
        '''return {alice : weight, bob : weight, ...}'''
        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        records = {}
        for person in data:
            records[person["name"]] = 0
            for record in person["records"]:
                records[person["name"]] += record["amount"]
        # so far records = {Alice : amount, Bob : amount, ...}

        zero_records = []
        # records persons who has not pay before
        for people in records.keys():
            if records[people] == 0:
                zero_records.append(people) 
        # if this is the first time use, everyone has equal posibility
        if len(zero_records) == len(records):
            for item in records.keys():
                records[item] = 1
        # if everyones has record, use algorithm to calculate weight
        elif len(zero_records) == 0:
            lowest_payment = ["Nobody",float('inf')]
            for name in records.keys():
                if records[name] < lowest_payment[1]:
                    lowest_payment = [name, records[name]]
            weight_records = {}
            for name in list(records.keys()):
                diff = records[name] - lowest_payment[1]
                weight = round(100 - diff, 4) if (100 - diff) > 0 else 0
                if weight != 0:
                    weight_records[name] = weight
            #prevent senerio that everyone paid exactly the same amount of money
            if len(weight_records) == 0:
                for name in records.keys():
                    records[name] = 1
            else:
                records = weight_records
        # if someone paid, but others not, people who has not paid has equal weight,
        # and people who has paid will not pay this time
        else:
            records = {}
            for item in zero_records:
                records[item] = 1
        
        return records
    
    def writeNewPayment(self, name:str, amount:float, time:str):
        with open(self.filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        # prepare new record
        record = {"amount": amount,     
                  "time": time}
        for person in data:
            if person["name"] == name:
                person["records"].append(record)
                break
        # if didnot find the person, create new one
        else:
            data.append({"name": name, "records": []})
            data[-1]["records"].append(record)

        # dump new file
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)
        
# test
#if __name__ == "__main__":
    #res = opData()
    #print(res.getDisplayData())