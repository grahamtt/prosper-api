from datetime import date
from typing import List, Literal, NamedTuple

from prosper_api.models.enums import (
    BorrowerState,
    EmploymentStatus,
    FICOScore,
    IncomeRange,
    ListingCategory,
    ListingStatus,
    Occupation,
    ProsperRating,
)


class AmountsByRating(NamedTuple):
    """Holds arbitrary float amounts bucketed by Prosper rating."""

    NA: float
    HR: float
    E: float
    D: float
    C: float
    B: float
    A: float
    AA: float


class Account(NamedTuple):
    """Holds account-level information, such as current balances."""

    available_cash_balance: float
    pending_investments_primary_market: float
    pending_investments_secondary_market: float
    pending_quick_invest_orders: float
    total_principal_received_on_active_notes: float
    total_amount_invested_on_active_notes: float
    outstanding_principal_on_active_notes: float
    total_account_value: float
    pending_deposit: float
    last_deposit_amount: float
    last_deposit_date: str
    last_withdraw_amount: float
    last_withdraw_date: str
    external_user_id: str
    prosper_account_digest: str
    invested_notes: AmountsByRating
    pending_bids: AmountsByRating


class _ListResponse(NamedTuple):
    result: List[NamedTuple]
    result_count: int
    total_count: int


class CreditBureauValues(NamedTuple):
    """Represents data sourced from TransUnion."""

    g102s_months_since_most_recent_inquiry: float
    credit_report_date: str
    at02s_open_accounts: float
    g041s_accounts_30_or_more_days_past_due_ever: float
    g093s_number_of_public_records: float
    g094s_number_of_public_record_bankruptcies: float
    g095s_months_since_most_recent_public_record: float
    g218b_number_of_delinquent_accounts: float
    g980s_inquiries_in_the_last_6_months: float
    re20s_age_of_oldest_revolving_account_in_months: float
    s207s_months_since_most_recent_public_record_bankruptcy: float
    re33s_balance_owed_on_all_revolving_accounts: float
    at57s_amount_delinquent: float
    g099s_public_records_last_24_months: float
    at20s_oldest_trade_open_date: float
    at03s_current_credit_lines: float
    re101s_revolving_balance: float
    bc34s_bankcard_utilization: float
    at01s_credit_lines: float
    fico_score: str


class Listing(NamedTuple):
    """Represents a Prosper listing.

    Contains the information needed for an investor to make an informed decision about
    whether to invest in a potential loan.
    """

    listing_number: int
    prosper_rating: str
    listing_title: str
    listing_start_date: str
    listing_creation_date: str
    listing_status: int
    listing_status_reason: str
    invested: bool
    biddable: bool
    has_mortgage: bool
    credit_bureau_values_transunion_indexed: CreditBureauValues
    employment_status_description: str
    investment_type_description: str
    last_updated_date: str
    decision_bureau: str
    member_key: str
    borrower_state: str
    co_borrower_application: bool
    income_verifiable: bool
    occupation: str = None
    loan_number: int = None
    listing_end_date: str = None
    loan_origination_date: str = None
    months_employed: float = None
    investment_product_id: int = None
    listing_amount: float = None
    amount_funded: float = None
    amount_remaining: float = None
    percent_funded: float = None
    partial_funding_indicator: bool = None
    funding_threshold: float = None
    lender_yield: float = None
    borrower_rate: float = None
    borrower_apr: float = None
    listing_term: int = None
    listing_monthly_payment: float = None
    prosper_score: int = None
    listing_category_id: int = None
    income_range: int = None
    income_range_description: str = None
    stated_monthly_income: float = None
    dti_wprosper_loan: float = None
    lender_indicator: int = None
    channel_code: int = None
    amount_participation: float = None
    investment_typeid: int = None
    estimated_monthly_housing_expense: float = None
    historical_return: float = None
    historical_return_10th_pctl: float = None
    historical_return_90th_pctl: float = None
    prior_prosper_loans_active: int = None
    prior_prosper_loans: int = None
    prior_prosper_loan_earliest_pay_off: int = None
    prior_prosper_loans_principal_borrowed: float = None
    prior_prosper_loans_principal_outstanding: float = None
    prior_prosper_loans_balance_outstanding: float = None
    prior_prosper_loans_cycles_billed: int = None
    prior_prosper_loans_ontime_payments: int = None
    prior_prosper_loans_late_cycles: int = None
    prior_prosper_loans_late_payments_one_month_plus: int = None
    prior_prosper_loans31dpd: float = None
    max_prior_prosper_loan: float = None
    min_prior_prosper_loan: float = None
    verification_stage: str = None
    combined_dti_wprosper_loan: float = None
    combined_stated_monthly_income: float = None


class SearchListingsRequest(NamedTuple):
    """Request for searching listings."""

    sort_by: str = "lender_yield"
    sort_dir: str = "desc"
    offset: int = None
    limit: int = None
    biddable: bool = True
    invested: bool = None

    amount_funded_min: float = None
    amount_funded_max: float = None
    amount_remaining_min: float = None
    amount_remaining_max: float = None
    borrower_rate_min: float = None
    borrower_rate_max: float = None
    borrower_state: List[str | BorrowerState] = None
    dti_wprosper_loan_min: float = None
    dti_wprosper_loan_max: float = None
    employment_status_description: List[str | EmploymentStatus] = None
    estimated_monthly_housing_expense_min: float = None
    estimated_monthly_housing_expense_max: float = None
    fico_score: List[str | FICOScore] = None
    has_mortgage: bool = None
    income_range: List[int | IncomeRange] = None
    lender_yield_min: float = None
    lender_yield_max: float = None
    listing_amount_min: float = None
    listing_amount_max: float = None
    listing_category_id: List[int | ListingCategory] = None
    listing_creation_date_min: str | date = None
    listing_creation_date_max: str | date = None
    listing_end_date_min: str | date = None
    listing_end_date_max: str | date = None
    listing_monthly_payment_min: float = None
    listing_monthly_payment_max: float = None
    listing_start_date_min: str | date = None
    listing_start_date_max: str | date = None
    listing_status: List[int | ListingStatus] = None
    listing_term: Literal[24, 36, 48, 60] = None
    loan_origination_date_min: str | date = None
    loan_origination_date_max: str | date = None
    months_employed_min: int = None
    months_employed_max: int = None
    occupation: List[str | Occupation] = None
    partial_funding_indicator: bool = None
    percent_funded_min: float = None
    percent_funded_max: float = None
    prior_prosper_loans_min: int = None
    prior_prosper_loans_max: int = None
    prior_prosper_loans_active_min: int = None
    prior_prosper_loans_active_max: int = None
    prior_prosper_loans_balance_outstanding_min: float = None
    prior_prosper_loans_balance_outstanding_max: float = None
    prior_prosper_loans_cycles_billed_min: int = None
    prior_prosper_loans_cycles_billed_max: int = None
    prior_prosper_loans_late_cycles_min: int = None
    prior_prosper_loans_late_cycles_max: int = None
    prior_prosper_loans_late_payments_one_month_plus_min: int = None
    prior_prosper_loans_late_payments_one_month_plus_max: int = None
    prior_prosper_loans_ontime_payments_min: int = None
    prior_prosper_loans_ontime_payments_max: int = None
    prior_prosper_loans_principal_borrowed_min: float = None
    prior_prosper_loans_principal_borrowed_max: float = None
    prior_prosper_loans_principal_outstanding_min: float = None
    prior_prosper_loans_principal_outstanding_max: float = None
    prosper_rating: List[str | ProsperRating] = [
        ProsperRating.AA,
        ProsperRating.A,
        ProsperRating.B,
        ProsperRating.C,
        ProsperRating.D,
        ProsperRating.E,
        ProsperRating.HR,
    ]
    prosper_score_min: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] = None
    prosper_score_max: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] = None
    stated_monthly_income_min: float = None
    stated_monthly_income_max: float = None
    verification_stage_min: Literal[1, 2, 3] = None
    verification_stage_max: Literal[1, 2, 3] = None
    whole_loan_end_date_min: str | date = None
    whole_loan_end_date_max: str | date = None
    whole_loan_start_date_min: str | date = None
    whole_loan_start_date_max: str | date = None
    co_borrower_application: bool = None
    combined_dti_wprosper_loan_min: float = None
    combined_dti_wprosper_loan_max: float = None
    combined_stated_monthly_income_min: float = None
    combined_stated_monthly_income_max: float = None

    listing_number: List[int] = []


class SearchListingsResponse(_ListResponse):
    """The listings matching the given search parameters."""

    result: List[Listing]


class Note(NamedTuple):
    """Represents the Prosper note.

    The note holds information about the borrowers obligation to the individual lenders.

    See Also:
        https://developers.prosper.com/docs/investor/notes-api/
    """

    principal_balance_pro_rata_share: float
    service_fees_paid_pro_rata_share: float
    principal_paid_pro_rata_share: float
    interest_paid_pro_rata_share: float
    prosper_fees_paid_pro_rata_share: float
    late_fees_paid_pro_rata_share: float
    collection_fees_paid_pro_rata_share: float
    debt_sale_proceeds_received_pro_rata_share: float
    platform_proceeds_net_received: float
    next_payment_due_amount_pro_rata_share: float
    note_ownership_amount: float
    note_sale_gross_amount_received: float
    note_sale_fees_paid: float
    loan_note_id: str
    listing_number: int
    note_status: int
    note_status_description: str
    is_sold: bool
    is_sold_folio: bool
    loan_number: int
    amount_borrowed: float
    borrower_rate: float
    lender_yield: float
    prosper_rating: str
    term: int
    age_in_months: int
    accrued_interest: float
    payment_received: float
    loan_settlement_status: str
    loan_extension_status: str
    loan_extension_term: int
    is_in_bankruptcy: bool
    co_borrower_application: bool
    origination_date: str
    days_past_due: int
    next_payment_due_date: str
    ownership_start_date: str
    ownership_end_date: str = None
    note_default_reason: str = None
    note_default_reason_description: str = None


class ListNotesRequest(NamedTuple):
    """Request for searching notes."""

    sort_by: str = "prosper_rating"
    sort_dir: str = "desc"
    offset: int = None
    limit: int = None


class ListNotesResponse(_ListResponse):
    """The notes matching the given search parameters."""

    result: List[Note]


class BidRequest(NamedTuple):
    """Represents an individual bid on a listing.

    An order may contain multiple bids on multiple listings.
    """

    listing_id: int
    bid_status: str
    bid_amount: float
    bid_amount_placed: float = None
    bid_result: str = None


class Order(NamedTuple):
    """Represents an order placed on one or more listings."""

    order_id: str
    order_date: str
    bid_requests: List[BidRequest]
    order_status: str
    source: str
    order_amount: float = None
    order_amount_placed: float = None
    order_amount_invested: float = None


class ListOrdersRequest(NamedTuple):
    """Request for listing orders."""

    sort_by: str = "prosper_rating"
    sort_dir: str = "desc"
    offset: int = None
    limit: int = None


class ListOrdersResponse(_ListResponse):
    """The orders that match the given search params."""

    result: List[Order]


class Loan(NamedTuple):
    """Represents the totality of a loan the lender participates in."""

    loan_number: int
    amount_borrowed: float
    borrower_rate: float
    prosper_rating: str
    term: int
    age_in_months: int
    origination_date: str
    days_past_due: int
    principal_balance: float
    service_fees_paid: float
    principal_paid: float
    interest_paid: float
    prosper_fees_paid: float
    late_fees_paid: float
    collection_fees_paid: float
    debt_sale_proceeds_received: float
    loan_status: int
    loan_status_description: str
    loan_default_reason: int
    next_payment_due_date: str
    next_payment_due_amount: float
    loan_default_reason_description: str = None


class ListLoansRequest(NamedTuple):
    """Request for searching loans."""

    sort_by: str = "prosper_rating"
    sort_dir: str = "desc"
    offset: int = None
    limit: int = None


class ListLoansResponse(_ListResponse):
    """The loans that match the given parameters."""

    result: List[Loan]
