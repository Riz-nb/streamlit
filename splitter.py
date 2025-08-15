from PyPDF2 import PdfReader, PdfWriter
import os

def split_academic_calendar(input_path, output_dir):
    sections = {
        # "Sessional_Dates": (5, 6),
        # "General_Information": (7, 8),
        # "Admission": (9, 14),
        # "Fees": (15, 18),
        # "University_Regulations_and_Programs": (19, 37),  # Includes regulations and program overview
        # "Williams_School_of_Business":(41, 54),
        # "School_of_Education":(55, 68),
        # # Split Faculty and Divisional Programs into 3 logical sections
        # "Faculty_and_Divisional_Programs_Humanities": (69, 144),
        # "Faculty_and_Divisional_Programs_Sciences": (145, 186),
        # "Faculty_and_Divisional_Programs_SocialSciences": (187, 230),
        # "Graduate_Studies": (231, 252),
        # "Services_Scholarships_Administration_Index": (253, 302)  # adjust ranges as needed

        "Sessional_Dates": (5, 6),
        "General_Information": (7, 8),
        "Admission": (9, 14),
        "Fees": (15, 18),


        "University_Regulations": (19, 36),
        "Programs_and_Courses": (37, 40),
        "Continuing_Education": (38, 38),
        "Writing_Centre": (39, 40),
        "Williams_School_of_Business": (41, 44),
        "School_of_Education": (45, 68),

        # Division of Humanities
        "Division_of_Humanities_Overview": (69, 69),
        "Division_of_Humanities_Art_History": (70, 72),
        "Division_of_Humanities_Arts_Administration": (73, 75),
        "Division_of_Humanities_Classical_Studies": (76, 82),
        "Division_of_Humanities_Drama": (83, 83),
        "Division_of_Humanities_English": (84, 92),
        "Division_of_Humanities_English_Language_Studies": (93, 96),
        "Division_of_Humanities_Etudes_francaises_et_quebecoises": (97, 100),
        "Division_of_Humanities_EWP": (101, 105),
        "Division_of_Humanities_Fine_Arts": (106, 110),
        "Division_of_Humanities_History": (111, 116),
        "Division_of_Humanities_College_of_Liberal_Arts": (117, 120),
        "Division_of_Humanities_Modern_Languages_Literatures_and_Cultures": (121, 121),
        "Division_of_Humanities_Modern_Languages_German": (122, 124),
        "Division_of_Humanities_Modern_Languages_Hispanic_Studies": (125, 127),
        "Division_of_Humanities_Modern_Languages_Italian": (128, 128),
        "Division_of_Humanities_Modern_Languages_Japanese": (129, 130),
        "Division_of_Humanities_Music": (131, 134),
        "Division_of_Humanities_Philosophy": (135, 137),
        "Division_of_Humanities_Pre_Law": (138, 139),
        "Division_of_Humanities_Religion": (140, 144),

        # Division of Natural Sciences and Mathematics
        "Division_of_Natural_Sciences_and_Mathematics_Overview": (145, 146),
        "Division_of_Natural_Sciences_and_Mathematics_Biochemistry": (147, 151),
        "Division_of_Natural_Sciences_and_Mathematics_Biological_Sciences": (152, 158),
        "Division_of_Natural_Sciences_and_Mathematics_Chemistry": (159, 164),
        "Division_of_Natural_Sciences_and_Mathematics_Computer_Science": (165, 170),
        "Division_of_Natural_Sciences_and_Mathematics_Mathematics": (171, 177),
        "Division_of_Natural_Sciences_and_Mathematics_Physics_and_Astronomy": (178, 183),
        "Division_of_Natural_Sciences_and_Mathematics_Pre_Medicine_Double_Major": (184, 186),

        # Division of Social Sciences
        "Division_of_Social_Sciences_Overview": (187, 187),
        "Division_of_Social_Sciences_Economics": (188, 193),
        "Division_of_Social_Sciences_Environment_and_Geography": (194, 200),
        "Division_of_Social_Sciences_Political_Science": (201, 206),
        "Division_of_Social_Sciences_Psychology": (207, 210),
        "Division_of_Social_Sciences_Sociology": (211, 215),
        "Division_of_Social_Sciences_Sports_Studies": (216, 218),

        # Graduate Studies
        "Graduate_Studies_Overview": (219, 234),
        "Graduate_Certificate_in_Business": (235, 235),
        "Graduate_Studies_MEd_and_MA_in_Education": (236, 237),
        "Graduate_Certificate_in_Teaching_Intensive_English": (238, 238),
        "Graduate_Certificate_in_Brewing_Science": (239, 239),
        "Graduate_Micro_Program_in_Climate_Change": (240, 240),
        "Graduate_Certificate_in_Knowledge_Mobilization": (241, 241),
        "Masters_in_Computer_Science": (242, 252),

        # Services and Facilities
        "Services_and_Facilities_Overview": (253, 254),
        "Student_Services": (255, 256),
        "Other_Services_and_Facilities": (257, 262),

        # Other
        "Scholarships_Awards_Bursaries_Loans_Prizes": (263, 286),
        "Administration_and_Librarians": (287, 292),
        "Index": (293, 299)
    }

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    reader = PdfReader(input_path)

    for name, (start_page, end_page) in sections.items():
        writer = PdfWriter()
        for page_index in range(start_page, end_page + 1):
            if page_index < len(reader.pages):
                writer.add_page(reader.pages[page_index])
        output_path = os.path.join(output_dir, f"{name}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"✅ Saved: {output_path}")
