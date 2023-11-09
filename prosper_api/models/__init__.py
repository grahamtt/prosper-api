from datetime import date
from decimal import Decimal
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
    """Holds arbitrary float | Decimal amounts bucketed by Prosper rating."""

    NA: float | Decimal
    HR: float | Decimal
    E: float | Decimal
    D: float | Decimal
    C: float | Decimal
    B: float | Decimal
    A: float | Decimal
    AA: float | Decimal


class Account(NamedTuple):
    """Holds account-level information, such as current balances."""

    available_cash_balance: float | Decimal
    pending_investments_primary_market: float | Decimal
    pending_investments_secondary_market: float | Decimal
    pending_quick_invest_orders: float | Decimal
    total_principal_received_on_active_notes: float | Decimal
    total_amount_invested_on_active_notes: float | Decimal
    outstanding_principal_on_active_notes: float | Decimal
    total_account_value: float | Decimal
    pending_deposit: float | Decimal
    last_deposit_amount: float | Decimal
    last_deposit_date: str
    last_withdraw_amount: float | Decimal
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

    g102s_months_since_most_recent_inquiry: float | Decimal
    credit_report_date: str
    at02s_open_accounts: float | Decimal
    g041s_accounts_30_or_more_days_past_due_ever: float | Decimal
    g093s_number_of_public_records: float | Decimal
    g094s_number_of_public_record_bankruptcies: float | Decimal
    g095s_months_since_most_recent_public_record: float | Decimal
    g218b_number_of_delinquent_accounts: float | Decimal
    g980s_inquiries_in_the_last_6_months: float | Decimal
    re20s_age_of_oldest_revolving_account_in_months: float | Decimal
    s207s_months_since_most_recent_public_record_bankruptcy: float | Decimal
    re33s_balance_owed_on_all_revolving_accounts: float | Decimal
    at57s_amount_delinquent: float | Decimal
    g099s_public_records_last_24_months: float | Decimal
    at20s_oldest_trade_open_date: float | Decimal
    at03s_current_credit_lines: float | Decimal
    re101s_revolving_balance: float | Decimal
    bc34s_bankcard_utilization: float | Decimal
    at01s_credit_lines: float | Decimal
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
    months_employed: float | Decimal = None
    investment_product_id: int = None
    listing_amount: float | Decimal = None
    amount_funded: float | Decimal = None
    amount_remaining: float | Decimal = None
    percent_funded: float | Decimal = None
    partial_funding_indicator: bool = None
    funding_threshold: float | Decimal = None
    lender_yield: float | Decimal = None
    borrower_rate: float | Decimal = None
    borrower_apr: float | Decimal = None
    listing_term: int = None
    listing_monthly_payment: float | Decimal = None
    prosper_score: int = None
    listing_category_id: int = None
    income_range: int = None
    income_range_description: str = None
    stated_monthly_income: float | Decimal = None
    dti_wprosper_loan: float | Decimal = None
    lender_indicator: int = None
    channel_code: int = None
    amount_participation: float | Decimal = None
    investment_typeid: int = None
    estimated_monthly_housing_expense: float | Decimal = None
    historical_return: float | Decimal = None
    historical_return_10th_pctl: float | Decimal = None
    historical_return_90th_pctl: float | Decimal = None
    prior_prosper_loans_active: int = None
    prior_prosper_loans: int = None
    prior_prosper_loan_earliest_pay_off: int = None
    prior_prosper_loans_principal_borrowed: float | Decimal = None
    prior_prosper_loans_principal_outstanding: float | Decimal = None
    prior_prosper_loans_balance_outstanding: float | Decimal = None
    prior_prosper_loans_cycles_billed: int = None
    prior_prosper_loans_ontime_payments: int = None
    prior_prosper_loans_late_cycles: int = None
    prior_prosper_loans_late_payments_one_month_plus: int = None
    prior_prosper_loans31dpd: float | Decimal = None
    max_prior_prosper_loan: float | Decimal = None
    min_prior_prosper_loan: float | Decimal = None
    verification_stage: str = None
    combined_dti_wprosper_loan: float | Decimal = None
    combined_stated_monthly_income: float | Decimal = None


class SearchListingsRequest(NamedTuple):
    """Request for searching listings."""

    sort_by: str = "lender_yield"
    sort_dir: str = "desc"
    offset: int = None
    limit: int = None
    biddable: bool = True
    invested: bool = None

    amount_funded_min: float | Decimal = None
    amount_funded_max: float | Decimal = None
    amount_remaining_min: float | Decimal = None
    amount_remaining_max: float | Decimal = None
    borrower_rate_min: float | Decimal = None
    borrower_rate_max: float | Decimal = None
    borrower_state: List[str | BorrowerState] = None
    dti_wprosper_loan_min: float | Decimal = None
    dti_wprosper_loan_max: float | Decimal = None
    employment_status_description: List[str | EmploymentStatus] = None
    estimated_monthly_housing_expense_min: float | Decimal = None
    estimated_monthly_housing_expense_max: float | Decimal = None
    fico_score: List[str | FICOScore] = None
    has_mortgage: bool = None
    income_range: List[int | IncomeRange] = None
    lender_yield_min: float | Decimal = None
    lender_yield_max: float | Decimal = None
    listing_amount_min: float | Decimal = None
    listing_amount_max: float | Decimal = None
    listing_category_id: List[int | ListingCategory] = None
    listing_creation_date_min: str | date = None
    listing_creation_date_max: str | date = None
    listing_end_date_min: str | date = None
    listing_end_date_max: str | date = None
    listing_monthly_payment_min: float | Decimal = None
    listing_monthly_payment_max: float | Decimal = None
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
    percent_funded_min: float | Decimal = None
    percent_funded_max: float | Decimal = None
    prior_prosper_loans_min: int = None
    prior_prosper_loans_max: int = None
    prior_prosper_loans_active_min: int = None
    prior_prosper_loans_active_max: int = None
    prior_prosper_loans_balance_outstanding_min: float | Decimal = None
    prior_prosper_loans_balance_outstanding_max: float | Decimal = None
    prior_prosper_loans_cycles_billed_min: int = None
    prior_prosper_loans_cycles_billed_max: int = None
    prior_prosper_loans_late_cycles_min: int = None
    prior_prosper_loans_late_cycles_max: int = None
    prior_prosper_loans_late_payments_one_month_plus_min: int = None
    prior_prosper_loans_late_payments_one_month_plus_max: int = None
    prior_prosper_loans_ontime_payments_min: int = None
    prior_prosper_loans_ontime_payments_max: int = None
    prior_prosper_loans_principal_borrowed_min: float | Decimal = None
    prior_prosper_loans_principal_borrowed_max: float | Decimal = None
    prior_prosper_loans_principal_outstanding_min: float | Decimal = None
    prior_prosper_loans_principal_outstanding_max: float | Decimal = None
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
    stated_monthly_income_min: float | Decimal = None
    stated_monthly_income_max: float | Decimal = None
    verification_stage_min: Literal[1, 2, 3] = None
    verification_stage_max: Literal[1, 2, 3] = None
    whole_loan_end_date_min: str | date = None
    whole_loan_end_date_max: str | date = None
    whole_loan_start_date_min: str | date = None
    whole_loan_start_date_max: str | date = None
    co_borrower_application: bool = None
    combined_dti_wprosper_loan_min: float | Decimal = None
    combined_dti_wprosper_loan_max: float | Decimal = None
    combined_stated_monthly_income_min: float | Decimal = None
    combined_stated_monthly_income_max: float | Decimal = None

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

    principal_balance_pro_rata_share: float | Decimal
    service_fees_paid_pro_rata_share: float | Decimal
    principal_paid_pro_rata_share: float | Decimal
    interest_paid_pro_rata_share: float | Decimal
    prosper_fees_paid_pro_rata_share: float | Decimal
    late_fees_paid_pro_rata_share: float | Decimal
    collection_fees_paid_pro_rata_share: float | Decimal
    debt_sale_proceeds_received_pro_rata_share: float | Decimal
    platform_proceeds_net_received: float | Decimal
    next_payment_due_amount_pro_rata_share: float | Decimal
    note_ownership_amount: float | Decimal
    note_sale_gross_amount_received: float | Decimal
    note_sale_fees_paid: float | Decimal
    loan_note_id: str
    listing_number: int
    note_status: int
    note_status_description: str
    is_sold: bool
    is_sold_folio: bool
    loan_number: int
    amount_borrowed: float | Decimal
    borrower_rate: float | Decimal
    lender_yield: float | Decimal
    prosper_rating: str
    term: int
    age_in_months: int
    accrued_interest: float | Decimal
    payment_received: float | Decimal
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
    bid_amount: float | Decimal
    bid_amount_placed: float | Decimal = None
    bid_result: str = None


class Order(NamedTuple):
    """Represents an order placed on one or more listings."""

    order_id: str
    order_date: str
    bid_requests: List[BidRequest]
    order_status: str
    source: str
    order_amount: float | Decimal = None
    order_amount_placed: float | Decimal = None
    order_amount_invested: float | Decimal = None


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
    amount_borrowed: float | Decimal
    borrower_rate: float | Decimal
    prosper_rating: str
    term: int
    age_in_months: int
    origination_date: str
    days_past_due: int
    principal_balance: float | Decimal
    service_fees_paid: float | Decimal
    principal_paid: float | Decimal
    interest_paid: float | Decimal
    prosper_fees_paid: float | Decimal
    late_fees_paid: float | Decimal
    collection_fees_paid: float | Decimal
    debt_sale_proceeds_received: float | Decimal
    loan_status: int
    loan_status_description: str
    loan_default_reason: int
    next_payment_due_date: str
    next_payment_due_amount: float | Decimal
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
