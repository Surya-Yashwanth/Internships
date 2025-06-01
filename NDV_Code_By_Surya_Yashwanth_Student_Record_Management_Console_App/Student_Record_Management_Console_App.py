import json
import os

class Student:
    """
    Represents a single student record with ID, name, branch, year, and marks.
    """
    def __init__(self, Student_id, Name, Branch, Year, Marks):
        self.student_id = Student_id
        self.name = Name
        self.branch = Branch
        self.year = Year
        self.marks = Marks

    def to_dict(self):
        """
        Converts the Student object to a dictionary for JSON serialization.
        """
        return {
            "Student_id": self.student_id,
            "Name": self.name,
            "Branch": self.branch,
            "Year": self.year,
            "Marks": self.marks
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Student object from a dictionary.
        This is useful when loading data from JSON.
        """
        return cls(
            data["Student_id"],
            data["Name"],
            data["Branch"],
            data["Year"],
            data["Marks"]
        )

    def __str__(self):
        """
        Returns a string representation of the Student object.
        """
        return (f"ID: {self.student_id}, Name: {self.name}, Branch: {self.branch}, "
                f"Year: {self.year}, Marks: {self.marks}")


class StudentManager:
    """
    Manages the collection of student records, including loading, saving,
    adding, viewing, updating, and deleting.
    """
    def __init__(self, file_name="students.json"):
        self.file_name = file_name
        self.students = []
        self._load_data()

    def _load_data(self):
        """
        Loads student data from the JSON file into the 'students' list.
        If the file doesn't exist, it initializes an empty list.
        """
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as f:
                    data = json.load(f)
                    self.students = [Student.from_dict(d) for d in data]
                print(f"Data loaded successfully from '{self.file_name}'.")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from '{self.file_name}'. Starting with empty records.")
                self.students = []
            except Exception as e:
                print(f"An unexpected error occurred while loading data: {e}. Starting with empty records.")
                self.students = []
        else:
            print(f"No existing data file '{self.file_name}' found. Starting with empty records.")

    def _save_data(self):
        """
        Saves the current 'students' list to the JSON file.
        Each Student object is converted to a dictionary before saving.
        """
        try:
            with open(self.file_name, 'w') as f:
                json.dump([s.to_dict() for s in self.students], f, indent=4)
            print(f"Data saved successfully to '{self.file_name}'.")
        except Exception as e:
            print(f"Error saving data to '{self.file_name}': {e}")

    def _find_student(self, student_id):
        """
        Helper method to find a student by their ID.
        Returns the Student object if found, None otherwise.
        """
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def _get_string_input(self, prompt, allow_empty=False):
        """
        Helper method to get and validate string input from the user.
        """
        while True:
            value = input(prompt).strip()
            if value:
                return value
            elif allow_empty:
                return value
            else:
                print("Input cannot be empty. Please try again.")

    def _get_int_input(self, prompt, min_val=None, max_val=None, allow_empty=False):
        """
        Helper method to get and validate integer input from the user.
        """
        while True:
            value_str = input(prompt).strip()
            if not value_str and allow_empty:
                return None
            try:
                value = int(value_str)
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}.")
                elif max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}.")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a whole number.")

    def _get_float_input(self, prompt, min_val=None, max_val=None, allow_empty=False):
        """
        Helper method to get and validate float input from the user.
        """
        while True:
            value_str = input(prompt).strip()
            if not value_str and allow_empty:
                return None
            try:
                value = float(value_str)
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}.")
                elif max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}.")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a number.")

    def add_student(self):
        """
        Prompts the user for new student details and adds the record.
        Ensures student ID is unique.
        """
        print("\n--- Add New Student ---")
        while True:
            student_id = self._get_string_input("Enter Student ID: ")
            if self._find_student(student_id):
                print(f"Student with ID '{student_id}' already exists. Please use a unique ID.")
            else:
                break

        name = self._get_string_input("Enter Name: ")
        branch = self._get_string_input("Enter Branch: ")
        year = self._get_int_input("Enter Year (e.g., 1, 2, 3, 4): ", min_val=1)
        marks = self._get_float_input("Enter Marks (0-100): ", min_val=0, max_val=100)

        new_student = Student(student_id, name, branch, year, marks)
        self.students.append(new_student)
        self._save_data()
        print(f"Student '{name}' (ID: {student_id}) added successfully!")

    def view_students(self):
        """
        Displays all student records in a formatted tabular layout.
        """
        print("\n--- All Student Records ---")
        if not self.students:
            print("No student records found.")
            return

        headers = ["ID", "Name", "Branch", "Year", "Marks"]
        
        # Calculate maximum width for each column dynamically, including headers
        col_widths = {
            "ID": max(len(s.student_id) for s in self.students) if self.students else 0,
            "Name": max(len(s.name) for s in self.students) if self.students else 0,
            "Branch": max(len(s.branch) for s in self.students) if self.students else 0,
            "Year": max(len(str(s.year)) for s in self.students) if self.students else 0,
            "Marks": max(len(str(s.marks)) for s in self.students) if self.students else 0
        }

        # Ensure header width is respected if content is shorter
        col_widths["ID"] = max(col_widths["ID"], len("ID"))
        col_widths["Name"] = max(col_widths["Name"], len("Name"))
        col_widths["Branch"] = max(col_widths["Branch"], len("Branch"))
        col_widths["Year"] = max(col_widths["Year"], len("Year"))
        col_widths["Marks"] = max(col_widths["Marks"], len("Marks"))
        
        # Add some padding
        padding = 2
        for key in col_widths:
            col_widths[key] += padding

        # Print header
        header_line_format = (
            f"{{:<{col_widths['ID']}}}"
            f"{{:<{col_widths['Name']}}}"
            f"{{:<{col_widths['Branch']}}}"
            f"{{:<{col_widths['Year']}}}"
            f"{{:<{col_widths['Marks']}}}"
        )
        print(header_line_format.format("ID", "Name", "Branch", "Year", "Marks"))
        print("-" * sum(col_widths.values()))

        # Print each student record
        for student in self.students:
            print(
                header_line_format.format(
                    student.student_id,
                    student.name,
                    student.branch,
                    str(student.year),
                    str(student.marks)
                )
            )
        print("-" * sum(col_widths.values()))


    def update_student(self):
        """
        Prompts for a student ID, finds the student, and allows updating
        their name, branch, year, and marks.
        """
        print("\n--- Update Student Record ---")
        student_id = self._get_string_input("Enter Student ID to update: ")
        student = self._find_student(student_id)

        if student:
            print(f"Found student: {student}")
            print("Enter new details (leave blank to keep current value):")

            new_name = self._get_string_input(f"Enter new Name ({student.name}): ", allow_empty=True)
            if new_name:
                student.name = new_name

            new_branch = self._get_string_input(f"Enter new Branch ({student.branch}): ", allow_empty=True)
            if new_branch:
                student.branch = new_branch

            new_year = self._get_int_input(f"Enter new Year ({student.year}): ", min_val=1, allow_empty=True)
            if new_year is not None:
                student.year = new_year

            new_marks = self._get_float_input(f"Enter new Marks ({student.marks}): ", min_val=0, max_val=100, allow_empty=True)
            if new_marks is not None:
                student.marks = new_marks

            self._save_data()
            print(f"Student with ID '{student_id}' updated successfully!")
        else:
            print(f"Student with ID '{student_id}' not found.")

    def delete_student(self):
        """
        Prompts for a student ID and deletes the corresponding record.
        Includes a confirmation step.
        """
        print("\n--- Delete Student Record ---")
        student_id = self._get_string_input("Enter Student ID to delete: ")
        
        student_to_delete = self._find_student(student_id)

        if student_to_delete:
            print(f"Found student: {student_to_delete}")
            confirm = input(f"Are you sure you want to delete student with ID '{student_id}'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                self.students = [s for s in self.students if s.student_id != student_id]
                self._save_data()
                print(f"Student with ID '{student_id}' deleted successfully!")
            else:
                print(f"Deletion cancelled for student with ID '{student_id}'.")
        else:
            print(f"Student with ID '{student_id}' not found.")

def display_menu():
    """
    Displays the main menu options to the user.
    """
    print("\n--- Student Record Management System ---")
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Update Student Record")
    print("4. Delete Student Record")
    print("5. Exit")
    print("----------------------------------------")

def main():
    """
    Main function to run the student record management application.
    """
    manager = StudentManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            manager.add_student()
        elif choice == '2':
            manager.view_students()
        elif choice == '3':
            manager.update_student()
        elif choice == '4':
            manager.delete_student()
        elif choice == '5':
            print("Exiting Student Record Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
