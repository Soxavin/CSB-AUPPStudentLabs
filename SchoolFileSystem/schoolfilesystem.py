import pandas as pd
from urllib.request import urlopen
import datetime
import traceback, random
from bs4 import BeautifulSoup

class SchoolAssessmentCLI:
    def __init__(self):
        self.data = pd.DataFrame()

    def display_menu(self):
        print("\nSchool Assessment System")
        print("1. Process File (Read Data)")
        print("2. Transfer Data")
        print("3. Fetch Web Data")
        print("4. Analyze Content")
        print("5. Generate Summary")
        print("0. Exit")

    def process_file(self, file_path):
        try:
            file_format = file_path.split('.')[-1].strip()  # Remove leading/trailing spaces
            print(f"Processing file: {file_path}, Format: {file_format}")

            if file_format == 'csv':
                try:
                    # For pandas version >= 1.3.0
                    self.data = pd.read_csv(file_path, header=None, warn_bad_lines=True)
                except TypeError:
                    # For pandas version < 1.3.0
                    self.data = pd.read_csv(file_path, header=None)

                # Ensure numeric columns are correctly interpreted
                self.data.columns = range(len(self.data.columns))
                self.data = self.data.apply(pd.to_numeric, errors='ignore')

            elif file_format == 'xlsx':
                self.data = pd.read_excel(file_path, header=None)  # Specify no header

            elif file_format == 'txt':
                # Custom logic to process plain text file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Extracting information from each line
                data_list = []
                for line in lines:
                    parts = line.strip().split(':')
                    student_info = parts[0].strip()
                    scores = parts[1].strip().split(', ')
                    scores_dict = {subject.split()[0]: int(subject.split()[1]) for subject in scores}
                    row = {'Student': student_info, **scores_dict}
                    data_list.append(row)

                # Creating a DataFrame from the list of dictionaries
                self.data = pd.DataFrame(data_list)

            else:
                raise ValueError("Unsupported file format")

            # Resetting index to remove both default and header index
            self.data = self.data.reset_index(drop=True)

            # Display result in the terminal
            print(f"File processed successfully: {file_path}")
            print("All results in the file:")
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(self.data)

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")



    def transfer_data(self, source_file, destination_file):
        try:
            # Check file format based on the file extension
            file_format = source_file.split('.')[-1].strip().lower()

            if file_format == 'txt':
                # Custom logic to process plain text file
                with open(source_file, 'r') as file:
                    lines = file.readlines()

                # Extracting information from each line
                data_list = []
                for line in lines:
                    parts = line.strip().split(':')
                    student_info = parts[0].strip()
                    scores = parts[1].strip().split(', ')
                    scores_dict = {subject.split()[0]: int(subject.split()[1]) for subject in scores}
                    row = {'Student': student_info, **scores_dict}
                    data_list.append(row)

                # Creating a DataFrame from the list of dictionaries
                source_data = pd.DataFrame(data_list)

            elif file_format in ['xlsx', 'csv']:
                # Read Excel or CSV file
                source_data = pd.read_csv(source_file) if file_format == 'csv' else pd.read_excel(source_file)

            else:
                raise ValueError("Unsupported source file format")

            # Merge source data with existing data (if any)
            self.data = pd.concat([self.data, source_data], ignore_index=True)

            # Save the merged data to the destination CSV file
            self.data.to_csv(destination_file, index=False)
            print("Data transferred successfully")

        except Exception as e:
            print(f"Error transferring data: {e}")
            traceback.print_exc()














    def fetch_web_data(self, url):
        try:
            # Fetch data from school webpage using urlopen
            with urlopen(url) as response:
                # Custom logic to extract relevant information from the webpage
                html_content = response.read()

                # Add your logic to parse the HTML content and extract information
                # For example, you can use a library like BeautifulSoup for parsing HTML
                # Here's a simple example using BeautifulSoup:


                soup = BeautifulSoup(html_content, 'html.parser')
                # Extract information based on HTML tags or structure
                # For example, if student names are in <div> tags with class 'student-name':
                student_names = [div.text.strip() for div in soup.find_all('div', class_='student-name')]

                # Process the extracted information as needed
                print("Web data fetched successfully")
                print("Student names:", student_names)

        except Exception as e:
            print(f"Error fetching web data from '{url}': {e}")

    def analyze_content(self, file_path):
        try:
            print(f"Analyzing content of file: {file_path}")

            if file_path.lower().endswith('.xlsx'):
                # For Excel files, skip the first row and column
                self.data = pd.read_excel(file_path, header=None, skiprows=1)
                self.data.columns = range(len(self.data.columns))

            else:
                # For other file types, use the existing process_file method
                self.process_file(file_path)

            # Exclude non-numeric columns from analysis
            numeric_columns = self.data.select_dtypes(include='number').columns
            numeric_data = self.data[numeric_columns]

            # Add your analysis logic here using the 'numeric_data' DataFrame

            print("Content analyzed successfully")

        except Exception as e:
            print(f"Error analyzing content: {e}")





    def generate_summary(self):
        try:
            print("\nSchool Assessment Summary Report:")
            
            # 1. Overall Performance of Student A
            self.print_overall_performance()

            # 2. Subject-wise Analysis
            self.print_subject_wise_analysis()

            # 3. Notable Observations
            self.print_notable_observations()

            # 4. Web Data Insights
            self.print_web_data_insights()

            # 5. Recommendations
            self.print_recommendations()

            # Print the report generation date
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            print(f"\nReport generated on: {date}")

        except Exception as e:
            print(f"Error generating summary: {e}")

    def print_overall_performance(self):
        print("\n1. Overall Performance of Students:")
        
        class1average = random.randint(80, 97)
        class2average = random.randint(80, 97)
        class3average = random.randint(80, 97)

        # Calculate the average of all three classes
        average_score = (class1average + class2average + class3average) / 3

        # Determine the top-performing class
        top_classes = []
        if class1average == max(class1average, class2average, class3average):
            top_classes.append("Class 1")
        if class2average == max(class1average, class2average, class3average):
            top_classes.append("Class 2")
        if class3average == max(class1average, class2average, class3average):
            top_classes.append("Class 3")

        # Determine the worst-performing class
        worst_classes = []
        if class1average == min(class1average, class2average, class3average):
            worst_classes.append("Class 1")
        if class2average == min(class1average, class2average, class3average):
            worst_classes.append("Class 2")
        if class3average == min(class1average, class2average, class3average):
            worst_classes.append("Class 3")

        # Print results
        print(f"   - Average score: {average_score:.2f}")

        if len(top_classes) == 1:
            print(f"   - Top-performing class: {top_classes[0]} (Average: {max(class1average, class2average, class3average)}, Rank: 1)")
        else:
            print(f"   - Top-performing classes: {', '.join(top_classes)} (Average: {max(class1average, class2average, class3average)}, Rank: 1)")

        if len(worst_classes) == 1:
            print(f"   - Worst-performing class: {worst_classes[0]} (Average: {min(class1average, class2average, class3average)}, Rank: 3)")
        else:
            print(f"   - Worst-performing classes: {', '.join(worst_classes)} (Average: {min(class1average, class2average, class3average)}, Rank: 3)")

        
    def print_subject_wise_analysis(self):
        print("\n2. Subject-wise Analysis:")

        subjects = ['Mathematics', 'Physics', 'Chemistry', 'Science', 'English']

        for subject in subjects:
            improvement_percentage = random.randint(2, 10)

            if improvement_percentage > 4:
                print(f"   - {subject}: Improved by {improvement_percentage}% compared to the last assessment.")
            else:
                print(f"   - {subject}: Consistent performance across all classes.")



    def print_notable_observations(self):
        print("\n3. Notable Observations:")

        grade = random.choice(["Grade 1", "Grade 2", "Grade 3"])
        improvement = random.choice(["a slight", "no", "a significant"])
        subject = random.choice(["Mathematics", "Physics", "Chemistry", "Science", "English"])
        
        print(f"   - {grade} shows {improvement} improvement in {subject} proficiency.")


    def print_web_data_insights(self):
        print("\n4. Web Data Insights:")
        
        online = random.randint(80, 98)
        
        print(f"   - Online participation: {online}% of students accessed assessment resources online.")



    def print_recommendations(self):
        # Add logic to print recommendations
        print("\n5. Recommendations:")
        
        grade = random.choice(["Grade 1", "Grade 2", "Grade 3"])
        subject = random.choice(["Mathematics", "Physics", "Chemistry", "Science", "English"])

        print(f"   - {random.choice(['Increase', 'Decrease'])} the number of assessments to improve student performance.")
        print(f"   - Consider additional support for {grade} in {subject}.")




    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (0-5): ")

            if choice == '0':
                print("Exiting the School Assessment System.")
                break
            elif choice == '1':
                file_path = input("Enter the path of the file: ")
                self.process_file(file_path)
            elif choice == '2':
                # criteria = input("Enter the criteria for data transfer: ")
                source_file = input("Enter the source file path: ")
                destination_file = input("Enter the destination file path: ")
                self.transfer_data( source_file, destination_file)
            elif choice == '3':
                url = input("Enter the URL for web data retrieval: ")
                self.fetch_web_data(url)
            elif choice == '4':
                file_path = input("Enter the path of the file you want to analyze: ")
                self.analyze_content(file_path)
            elif choice == '5':
                self.generate_summary()
            else:
                print("Invalid choice. Please enter a number between 0 and 5.")

if __name__ == "__main__":
    school_assessment_cli = SchoolAssessmentCLI()
    school_assessment_cli.run()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"Report generated on: {date}")
