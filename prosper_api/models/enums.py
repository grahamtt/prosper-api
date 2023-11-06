from enum import Enum


class _DefaultEnum(Enum):
    def __str__(self):
        return self._value_


class ProsperRating(_DefaultEnum):
    """Prosper ratings."""

    NR = "NR"
    HR = "HR"
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    AA = "AA"


class IncomeRange(_DefaultEnum):
    """Income ranges."""

    NOT_DISPLAYED = 0
    ZERO_DOLLARS = 1
    BETWEEN_1_AND_24999_DOLLARS = 2
    BETWEEN_25000_AND_49999_DOLLARS = 3
    BETWEEN_50000_AND_74999_DOLLARS = 4
    BETWEEN_75000_AND_99999_DOLLARS = 5
    MORE_THAN_100000_DOLLARS = 6
    NOT_EMPLOYED = 7


class ListingCategory(_DefaultEnum):
    """Listing categories."""

    DEBT_CONSOLIDATION = 1
    HOME_IMPROVEMENT = 2
    BUSINESS = 3
    PERSONAL_LOAN = 4
    STUDENT_USE = 5
    AUTO_MOTORCYCLE_RV_BOAT = 6
    OTHER = 7
    BABY_AND_ADOPTION = 8
    BOAT = 9
    COSMETIC_PROCEDURES = 10
    ENGAGEMENT_RING_FINANCING = 11
    GREEN_LOANS = 12
    HOUSEHOLD_EXPENSES = 13
    LARGE_PURCHASE = 14
    MEDICAL_DENTAL = 15
    MOTORCYCLE = 16
    RV = 17
    TAXES = 18
    VACATION = 19
    WEDDING_LOANS = 20
    SPECIAL_OCCASION = 21


class ListingStatus(_DefaultEnum):
    """Listing statuses."""

    ACTIVE = 2
    WITHDRAWN = 3
    EXPIRED = 4
    COMPLETED = 5
    CANCELLED = 6
    PENDING_REVIEW = 7


class Occupation(_DefaultEnum):
    """Occupations."""

    ACCOUNTANT_CPA = "Accountant / CPA"
    ANALYST = "Analyst"
    ARCHITECT = "Architect"
    ATTORNEY = "Attorney"
    BIOLOGIST = "Biologist"
    BUS = "Bus"
    DRIVER = "Driver"
    CAR = "Car"
    DEALER = "Dealer"
    CHEMIST = "Chemist"
    CIVIL = "Civil"
    SERVICE = "Service"
    CLERGY = "Clergy"
    CLERICAL = "Clerical"
    COMPUTER = "Computer"
    PROGRAMMER = "Programmer"
    CONSTRUCTION = "Construction"
    DENTIST = "Dentist"
    DOCTOR = "Doctor"
    ENGINEER_CHEMICAL = "Engineer – Chemical"
    ENGINEER_ELECTRICAL = "Engineer – Electrical"
    ENGINEER_MECHANICAL = "Engineer – Mechanical"
    EXECUTIVE = "Executive"
    FIREMAN = "Fireman"
    FLIGHT = "Flight"
    ATTENDANT = "Attendant"
    FOOD_SERVICE = "Food Service"
    FOOD_SERVICE_MANAGEMENT = "Food Service Management"
    HOMEMAKER = "Homemaker"
    JUDGE = "Judge"
    LABORER = "Laborer"
    LANDSCAPING = "Landscaping"
    MEDICAL = "Medical"
    TECHNICIAN = "Technician"
    MILITARY_ENLISTED = "Military Enlisted"
    MILITARY_OFFICER = "Military Officer"
    NURSE_PLN = "Nurse (LPN)"
    NURSE_RN = "Nurse (RN)"
    NURSES_AIDE = "Nurse’s Aide"
    PHARMACIST = "Pharmacist"
    PILOT = "Pilot Private / Commercial"
    POLICE_CORRECTION_OFFICER = "Police Officer / Correction Officer"
    POSTAL_SERVICE = "Postal Service"
    PRINCIPAL = "Principal"
    PROFESSIONAL = "Professional"
    PROFESSOR = "Professor"
    PSYCHOLOGIST = "Psychologist"
    REALTOR = "Realtor"
    RELIGIOUS = "Religious"
    RETAIL = "Retail"
    MANAGEMENT = "Management"
    SALES = "Sales"
    COMMISSION = "Commission"
    SALES_RETAIL = "Sales Retail"
    SCIENTIST = "Scientist"
    ADMINISTRATIVE = "Administrative"
    ASSISTANT = "Assistant"
    SKILLED = "Skilled"
    LABOR = "Labor"
    SOCIAL = "Social"
    WORKER = "Worker"
    STUDENT_COLLEGE_FRESHMAN = "Student – College Freshman"
    STUDENT_COLLEGE_SOPHOMORE = "Student – College Sophomore"
    STUDENT_COLLEGE_JUNIOR = "Student – College Junior"
    STUDENT_COLLEGE_SENIOR = "Student – College Senior"
    STUDENT_COLLEGE_GRADUATE_STUDENT = "Student – College Graduate Student"
    STUDENT_COMMUNITY_COLLEGE = "Student – Community College"
    STUDENT_TECHNICAL_SCHOOL = "Student – Technical School"
    TEACHER = "Teacher"
    TEACHERS_AIDE = "Teacher’s Aide"
    TRADESMAN_CARPENTER = "Tradesman – Carpenter"
    TRADESMAN_ELECTRICIAN = "Tradesman – Electrician"
    TRADESMAN_MECHANIC = "Tradesman – Mechanic"
    TRADESMAN_PLUMBER = "Tradesman – Plumber"
    TRUCK_DRIVER = "Truck Driver"
    WAITER_WAITRESS = "Waiter / Waitress"
    OTHER = "Other"
    INVESTOR = "Investor"


class EmploymentStatus(_DefaultEnum):
    """Employment statuses."""

    EMPLOYED = "Employed"
    SELF_EMPLOYED = "Self-employed"
    RETIRED = "Retired"


class FICOScore(_DefaultEnum):
    """FICO scores."""

    LESS_THAN_600 = "<600"
    BETWEEN_600_AND_619 = "600-619"
    BETWEEN_620_AND_639 = "620-639"
    BETWEEN_640_AND_659 = "640-659"
    BETWEEN_660_AND_679 = "660-679"
    BETWEEN_680_AND_699 = "680-699"
    BETWEEN_700_AND_719 = "700-719"
    BETWEEN_720_AND_739 = "720-739"
    BETWEEN_740_AND_759 = "740-759"
    BETWEEN_760_AND_779 = "760-779"
    BETWEEN_780_AND_799 = "780-799"
    BETWEEN_800_AND_819 = "800-819"
    BETWEEN_820_AND_850 = "820-850"


class BorrowerState(_DefaultEnum):
    """Borrower state abbreviations."""

    ALASKA = "AK"
    ALABAMA = "AL"
    ARKANSAS = "AR"
    ARIZONA = "AZ"
    CALIFORNIA = "CA"
    COLORADO = "CO"
    CONNECTICUT = "CT"
    DISTRICT_OF_COLUMBIA = "DC"
    DELAWARE = "DE"
    FLORIDA = "FL"
    GEORGIA = "GA"
    HAWAII = "HI"
    IOWA = "IA"
    IDAHO = "ID"
    ILLINOIS = "IL"
    INDIANA = "IN"
    KANSAS = "KS"
    KENTUCKY = "KY"
    LOUISIANA = "LA"
    MASSACHUSETTS = "MA"
    MARYLAND = "MD"
    MAINE = "ME"
    MICHIGAN = "MI"
    MINNESOTA = "MN"
    MISSOURI = "MO"
    MISSISSIPPI = "MS"
    MONTANA = "MT"
    NORTH_CAROLINA = "NC"
    NORTH_DAKOTA = "ND"
    NEBRASKA = "NE"
    NEW_HAMPSHIRE = "NH"
    NEW_JERSEY = "NJ"
    NEW_MEXICO = "NM"
    NEVADA = "NV"
    NEW_YORK = "NY"
    OHIO = "OH"
    OKLAHOMA = "OK"
    OREGON = "OR"
    PENNSYLVANIA = "PA"
    RHODE_ISLAND = "RI"
    SOUTH_CAROLINA = "SC"
    SOUTH_DAKOTA = "SD"
    TENNESSEE = "TN"
    TEXAS = "TX"
    UTAH = "UT"
    VIRGINIA = "VA"
    VERMONT = "VT"
    WASHINGTON = "WA"
    WISCONSIN = "WI"
    WEST_VIRGINIA = "WV"
    WYOMING = "WY"