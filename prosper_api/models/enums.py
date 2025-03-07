from enum import Enum


class _DefaultEnum(Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class SortOrder(_DefaultEnum):
    """Sort orders."""

    ASCENDING = "asc"
    DESCENDING = "desc"


class SearchListingsSortBy(_DefaultEnum):
    """Listing sort bys."""

    AMOUNT_FUNDED = "amount_funded"
    AMOUNT_REMAINING = "amount_remaining"
    BORROWER_RATE = "borrower_rate"
    FICO_SCORE = "fico_score"
    INVESTMENT_TYPEID = "investment_typeid"
    LENDER_YIELD = "lender_yield"
    LISTING_AMOUNT = "listing_amount"
    LISTING_CATEGORY_ID = "listing_category_id"
    LISTING_CREATION_DATE = "listing_creation_date"
    LISTING_END_DATE = "listing_end_date"
    LISTING_NUMBER = "listing_number"
    LISTING_START_DATE = "listing_start_date"
    LISTING_STATUS = "listing_status"
    LISTING_TERM = "listing_term"
    PARTIAL_FUNDING_INDICATOR = "partial_funding_indicator"
    PERCENT_FUNDED = "percent_funded"
    PROSPER_RATING = "prosper_rating"
    PROSPER_SCORE = "prosper_score"
    VERIFICATION_STAGE = "verification_stage"


class ListNotesSortBy(_DefaultEnum):
    """Listing sort bys."""

    LOAN_NOTE_ID = "loan_note_id"
    NOTE_OWNERSHIP_AMOUNT = "note_ownership_amount"
    AMOUNT_BORROWED = "amount_borrowed"
    BORROWER_RATE = "borrower_rate"
    PROSPER_RATING = "prosper_rating"
    TERM = "term"
    AGE_IN_MONTHS = "age_in_months"
    ORIGINATION_DATE = "origination_date"
    NOTE_STATUS = "note_status"


class ListOrdersSortBy(_DefaultEnum):
    """Listing sort bys."""

    LISTING_TITLE = "listing_title"
    PROSPER_RATING = "prosper_rating"
    LISTING_AMOUNT = "listing_amount"
    LOAN_TERM_MONTHS = "loan_term_months"
    ESTIMATED_END_DATE = "estimated_end_date"


class ListLoansSortBy(_DefaultEnum):
    """Listing sort bys."""

    LOAN_NUMBER = "loan_number"
    BORROWER_RATE = "borrower_rate"
    PROSPER_RATING = "prosper_rating"
    ORIGINATION_DATE = "origination_date"


class ProsperRating(_DefaultEnum):
    """Prosper ratings."""

    NA = "N/A"
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


class InvestmentType(_DefaultEnum):
    """Investment type of the listing."""

    WHOLE = 0
    FRACTIONAL = 1


class InvestmentProduct(_DefaultEnum):
    """Investment product of the listing."""

    STANDARD = 0
    SERIES_1 = 1


class Occupation(_DefaultEnum):
    """Occupations."""

    ACCOUNTANT_CPA = "Accountant/CPA"
    ANALYST = "Analyst"
    ARCHITECT = "Architect"
    ATTORNEY = "Attorney"
    BIOLOGIST = "Biologist"
    BUS_DRIVER = "Bus Driver"
    CAR_DEALER = "Car Dealer"
    CHEMIST = "Chemist"
    CIVIL_SERVICE = "Civil Service"
    CLERGY = "Clergy"
    CLERICAL = "Clerical"
    COMPUTER_PROGRAMMER = "Computer Programmer"
    CONSTRUCTION = "Construction"
    DENTIST = "Dentist"
    DOCTOR = "Doctor"
    ENGINEER_CHEMICAL = "Engineer - Chemical"
    ENGINEER_ELECTRICAL = "Engineer - Electrical"
    ENGINEER_MECHANICAL = "Engineer - Mechanical"
    EXECUTIVE = "Executive"
    FIREMAN = "Fireman"
    FLIGHT_ATTENDANT = "Flight Attendant"
    FOOD_SERVICE = "Food Service"
    FOOD_SERVICE_MANAGEMENT = "Food Service Management"
    HOMEMAKER = "Homemaker"
    JUDGE = "Judge"
    LABORER = "Laborer"
    LANDSCAPING = "Landscaping"
    MEDICAL_TECHNICIAN = "Medical Technician"
    MILITARY_ENLISTED = "Military Enlisted"
    MILITARY_OFFICER = "Military Officer"
    NURSE_PLN = "Nurse (LPN)"
    NURSE_RN = "Nurse (RN)"
    NURSES_AIDE = "Nurse's Aide"
    PHARMACIST = "Pharmacist"
    PILOT = "Pilot - Private/Commercial"
    POLICE_CORRECTION_OFFICER = "Police Officer/Correction Officer"
    POSTAL_SERVICE = "Postal Service"
    PRINCIPAL = "Principal"
    PROFESSIONAL = "Professional"
    PROFESSOR = "Professor"
    PSYCHOLOGIST = "Psychologist"
    REALTOR = "Realtor"
    RELIGIOUS = "Religious"
    RETAIL_MANAGEMENT = "Retail Management"
    SALES_COMMISSION = "Sales - Commission"
    SALES_RETAIL = "Sales - Retail"
    SCIENTIST = "Scientist"
    ADMINISTRATIVE_ASSISTANT = "Administrative Assistant"
    SELF_EMPLOYED = "Self Employed"
    SKILLED_LABOR = "Skilled Labor"
    SOCIAL_WORKER = "Social Worker"
    STUDENT_COLLEGE_FRESHMAN = "Student - College Freshman"
    STUDENT_COLLEGE_SOPHOMORE = "Student - College Sophomore"
    STUDENT_COLLEGE_JUNIOR = "Student - College Junior"
    STUDENT_COLLEGE_SENIOR = "Student - College Senior"
    STUDENT_COLLEGE_GRADUATE_STUDENT = "Student - College Graduate Student"
    STUDENT_COMMUNITY_COLLEGE = "Student - Community College"
    STUDENT_TECHNICAL_SCHOOL = "Student - Technical School"
    TEACHER = "Teacher"
    TEACHERS_AIDE = "Teacher's Aide"
    TRADESMAN_CARPENTER = "Tradesman - Carpenter"
    TRADESMAN_ELECTRICIAN = "Tradesman - Electrician"
    TRADESMAN_MECHANIC = "Tradesman - Mechanic"
    TRADESMAN_PLUMBER = "Tradesman - Plumber"
    TRUCK_DRIVER = "Truck Driver"
    WAITER_WAITRESS = "Waiter/Waitress"
    OTHER = "Other"
    INVESTOR = "Investor"


class EmploymentStatus(_DefaultEnum):
    """Employment statuses."""

    EMPLOYED = "Employed"
    SELF_EMPLOYED = "Self-employed"
    RETIRED = "Retired"
    NOT_EMPLOYED = "Not employed"
    OTHER = "Other"


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


class LoanStatus(_DefaultEnum):
    """Status of loan."""

    ORIGINATION_DELAYED = 0
    CURRENT = 1
    CHARGED_OFF = 2
    DEFAULTED = 3
    COMPLETED = 4
    FINAL_PAYMENT_IN_PROGRESS = 5
    CANCELLED = 6


class LoanDefaultReason(_DefaultEnum):
    """Reason for loan default."""

    NOT_IN_DEFAULT = 0
    DELINQUENCY = 1
    BANKRUPTCY = 2
    DECEASED = 3
    REPURCHASED = 4
    PAID_IN_FULL = 5
    SETTLED_IN_FULL = 6
    SOLD = 7


class OrderStatus(_DefaultEnum):
    """Status of order."""

    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class OrderSource(_DefaultEnum):
    """Source of order."""

    API = "API"
    AI = "AI"
    MI = "MI"


class BidStatus(_DefaultEnum):
    """Status of bid."""

    PENDING = "PENDING"
    INVESTED = "INVESTED"
    EXPIRED = "EXPIRED"


class BidResult(_DefaultEnum):
    """Result of bid."""

    NONE = "NONE"
    AMOUNT_BID_TOO_HIGH = "AMOUNT_BID_TOO_HIGH"
    AMOUNT_BID_TOO_LOW = "AMOUNT_BID_TOO_LOW"
    BID_FAILED = "BID_FAILED"
    BID_SUCCEEDED = "BID_SUCCEEDED"
    CANNOT_BID_ON_FRACTIONAL_LOANS = "CANNOT_BID_ON_FRACTIONAL_LOANS"
    CANNOT_BID_ON_OWN_LISTING = "CANNOT_BID_ON_OWN_LISTING"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    INVESTMENT_ORDER_ALREADY_PROCESSED = "INVESTMENT_ORDER_ALREADY_PROCESSED"
    LENDER_NOT_ELIGIBLE_TO_BID = "LENDER_NOT_ELIGIBLE_TO_BID"
    LISTING_NOT_BIDDABLE = "LISTING_NOT_BIDDABLE"
    SUITABILITY_REQUIREMENTS_NOT_MET = "SUITABILITY_REQUIREMENTS_NOT_MET"
    PARTIAL_BID_SUCCEEDED = "PARTIAL_BID_SUCCEEDED"


class PaymentTransactionCode(_DefaultEnum):
    """Transaction code."""

    AUTOMATED_CLEARING_HOUSE = "ACH"
    BANK_DRAFT = "BD"
    COLLECTION_AGENCY = "CAP"
    DISPUTE = "DSP"
    INSUFFICIENT_FUNDS = "NSF"
    BANK_DRAFT_RETURN = "BDF"
    ACH_FAILURE = "ACHF"
    COLLECTION_AGENCY_PAYMENT_FAILURE = "CAPF"
    PRIOR_PAYMENT_REVERSAL = "SEQR"
    INTEREST_REVERSAL = "INTR"
    INTEREST_REVERSAL2 = "CRINT"
    CHECK_PAYMENT = "CK"
    CHECK_PAYMENT_REVERSAL = "CKF"
    LATE_FEE_ADJUSTMENT = "LFA"
    NSF_ADJUSTMENT = "NSFA"
    LATE_FEE_ADJUSTMENT_WITHOUT_CASH_DISBURSEMENT = "LFA2"
    NSF_ADJUSTMENT_WITHOUT_CASH_DISBURSEMENT = "NSFA2"
    PROMOTIONAL_PAYMENT = "PROMO"
    PROMOTIONAL_PAYMENT_REVERSAL = "PROMF"
    CUSTOMER_RELATIONS_CREDIT = "CRCRE"
    CUSTOMER_RELATIONS_CREDIT_REVERSAL = "CRCRF"
    SETTLED_IN_FULL_CREDIT = "SIFA"
    SETTLED_IN_FULL_CREDIT_REVERSAL = "SIFAR"
    FLAT_CANCEL_A_LOAN = "UNWND"
    ACH_FAILURE_WITH_NO_NSF = "ACHF2"
    CHECK_FAILURE_WITH_NO_NSF = "CKF2"
    CUSTOMER_RELATIONS_CREDIT_FAILURE_WITH_NO_NSF = "CRCF2"
    COLLECTION_AGENCY_PAYMENT_FAILURE_WITH_NO_NSF = "CAPF2"
    PROMOTIONAL_PAYMENT_REVERSAL_WITH_NO_NSF = "PRMF2"
    SETTLED_IN_FULL_REVERSAL_WITH_NO_NSF = "SIFR2"
    DEBT_SALE_TRANSACTION = "DBSA"
    DEBT_SALE_FAILURE = "DBSAF"
    CATCH_ALL_GENERIC_PAYMENT = "PMT"
    CATCH_ALL_GENERIC_PAYMENT_FAILURE = "PMTF"
    CATCH_ALL_GENERIC_PAYMENT_WITH_NO_NSF = "PMTF2"
    BANK_DRAFT_RETURN_WITH_NO_NSF = "BDF2"
    REFUND = "RFND"
    # Unknown types
    OGRE = "OGRE"
    OGRF2 = "OGRF2"


class PaymentStatus(_DefaultEnum):
    """Payment status."""

    PROCESSING = "Process"
    SUCCESS = "Success"
    FAILURE = "Fail"
    DISPUTE = "Dispute"


class PaymentCashflowType(_DefaultEnum):
    """Payment cashflow type."""

    PAYMENT = "Payment"
    ADJUSTMENT = "Adjustment"
    CHARGEBACK = "Chargeback"
    DEBT_SALE = "DebtSale"
    OTHER = "Other"
