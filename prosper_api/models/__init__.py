from datetime import date, datetime
from decimal import Decimal
from typing import List, Literal, NamedTuple, Union

from prosper_api.models.enums import (
    BidResult,
    BidStatus,
    BorrowerState,
    EmploymentStatus,
    FICOScore,
    IncomeRange,
    InvestmentProduct,
    InvestmentType,
    ListingCategory,
    ListingStatus,
    LoanDefaultReason,
    LoanStatus,
    Occupation,
    OrderSource,
    OrderStatus,
    ProsperRating,
)


class AmountsByRating(NamedTuple):
    """Holds arbitrary float | Decimal amounts bucketed by Prosper rating."""

    NA: Union[float, Decimal]
    HR: Union[float, Decimal]
    E: Union[float, Decimal]
    D: Union[float, Decimal]
    C: Union[float, Decimal]
    B: Union[float, Decimal]
    A: Union[float, Decimal]
    AA: Union[float, Decimal]


class Account(NamedTuple):
    """Holds account-level information, such as current balances."""

    available_cash_balance: Union[float, Decimal]
    pending_investments_primary_market: Union[float, Decimal]
    pending_investments_secondary_market: Union[float, Decimal]
    pending_quick_invest_orders: Union[float, Decimal]
    total_principal_received_on_active_notes: Union[float, Decimal]
    total_amount_invested_on_active_notes: Union[float, Decimal]
    outstanding_principal_on_active_notes: Union[float, Decimal]
    total_account_value: Union[float, Decimal]
    pending_deposit: Union[float, Decimal]
    last_deposit_amount: Union[float, Decimal]
    last_deposit_date: Union[str, datetime]
    last_withdraw_amount: Union[float, Decimal]
    last_withdraw_date: Union[str, datetime]
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

    g102s_months_since_most_recent_inquiry: Union[float, Decimal]
    credit_report_date: Union[str, datetime]
    at02s_open_accounts: Union[float, Decimal]
    g041s_accounts_30_or_more_days_past_due_ever: Union[float, Decimal]
    g093s_number_of_public_records: Union[float, Decimal]
    g094s_number_of_public_record_bankruptcies: Union[float, Decimal]
    g095s_months_since_most_recent_public_record: Union[float, Decimal]
    g218b_number_of_delinquent_accounts: Union[float, Decimal]
    g980s_inquiries_in_the_last_6_months: Union[float, Decimal]
    re20s_age_of_oldest_revolving_account_in_months: Union[float, Decimal]
    s207s_months_since_most_recent_public_record_bankruptcy: Union[float, Decimal]
    re33s_balance_owed_on_all_revolving_accounts: Union[float, Decimal]
    at57s_amount_delinquent: Union[float, Decimal]
    g099s_public_records_last_24_months: Union[float, Decimal]
    at20s_oldest_trade_open_date: Union[float, Decimal]
    at03s_current_credit_lines: Union[float, Decimal]
    re101s_revolving_balance: Union[float, Decimal]
    bc34s_bankcard_utilization: Union[float, Decimal]
    at01s_credit_lines: Union[float, Decimal]
    fico_score: FICOScore


class Listing(NamedTuple):
    """Represents a Prosper listing.

    Contains the information needed for an investor to make an informed decision about
    whether to invest in a potential loan.
    """

    listing_number: int
    prosper_rating: ProsperRating
    listing_title: str
    listing_start_date: Union[str, datetime]
    listing_creation_date: Union[str, datetime]
    listing_status: ListingStatus
    listing_status_reason: str
    invested: bool
    biddable: bool
    has_mortgage: bool
    credit_bureau_values_transunion_indexed: CreditBureauValues
    employment_status_description: EmploymentStatus
    investment_type_description: str
    last_updated_date: Union[str, datetime]
    decision_bureau: str
    member_key: str
    borrower_state: BorrowerState
    co_borrower_application: bool
    income_verifiable: bool
    occupation: Occupation = None
    loan_number: int = None
    listing_end_date: Union[str, datetime] = None
    loan_origination_date: Union[str, datetime] = None
    months_employed: Union[float, Decimal] = None
    investment_product_id: InvestmentProduct = None
    listing_amount: Union[float, Decimal] = None
    amount_funded: Union[float, Decimal] = None
    amount_remaining: Union[float, Decimal] = None
    percent_funded: Union[float, Decimal] = None
    partial_funding_indicator: bool = None
    funding_threshold: Union[float, Decimal] = None
    lender_yield: Union[float, Decimal] = None
    borrower_rate: Union[float, Decimal] = None
    borrower_apr: Union[float, Decimal] = None
    listing_term: int = None
    listing_monthly_payment: Union[float, Decimal] = None
    prosper_score: int = None
    listing_category_id: int = None
    income_range: IncomeRange = None
    income_range_description: str = None
    stated_monthly_income: Union[float, Decimal] = None
    dti_wprosper_loan: Union[float, Decimal] = None
    lender_indicator: int = None
    channel_code: int = None
    amount_participation: Union[float, Decimal] = None
    investment_typeid: InvestmentType = None
    estimated_monthly_housing_expense: Union[float, Decimal] = None
    historical_return: Union[float, Decimal] = None
    historical_return_10th_pctl: Union[float, Decimal] = None
    historical_return_90th_pctl: Union[float, Decimal] = None
    prior_prosper_loans_active: int = None
    prior_prosper_loans: int = None
    prior_prosper_loan_earliest_pay_off: int = None
    prior_prosper_loans_principal_borrowed: Union[float, Decimal] = None
    prior_prosper_loans_principal_outstanding: Union[float, Decimal] = None
    prior_prosper_loans_balance_outstanding: Union[float, Decimal] = None
    prior_prosper_loans_cycles_billed: int = None
    prior_prosper_loans_ontime_payments: int = None
    prior_prosper_loans_late_cycles: int = None
    prior_prosper_loans_late_payments_one_month_plus: int = None
    prior_prosper_loans31dpd: Union[float, Decimal] = None
    max_prior_prosper_loan: Union[float, Decimal] = None
    min_prior_prosper_loan: Union[float, Decimal] = None
    verification_stage: str = None
    combined_dti_wprosper_loan: Union[float, Decimal] = None
    combined_stated_monthly_income: Union[float, Decimal] = None


class SearchListingsRequest(NamedTuple):
    """Request for searching listings."""

    sort_by: str = "lender_yield"
    sort_dir: str = "desc"
    offset: int = None
    limit: int = None
    biddable: bool = True
    invested: bool = None

    amount_funded_min: Union[float, Decimal] = None
    amount_funded_max: Union[float, Decimal] = None
    amount_remaining_min: Union[float, Decimal] = None
    amount_remaining_max: Union[float, Decimal] = None
    borrower_rate_min: Union[float, Decimal] = None
    borrower_rate_max: Union[float, Decimal] = None
    borrower_state: List[Union[str, BorrowerState]] = None
    dti_wprosper_loan_min: Union[float, Decimal] = None
    dti_wprosper_loan_max: Union[float, Decimal] = None
    employment_status_description: List[Union[str, EmploymentStatus]] = None
    estimated_monthly_housing_expense_min: Union[float, Decimal] = None
    estimated_monthly_housing_expense_max: Union[float, Decimal] = None
    fico_score: List[Union[str, FICOScore]] = None
    has_mortgage: bool = None
    income_range: List[Union[int, IncomeRange]] = None
    lender_yield_min: Union[float, Decimal] = None
    lender_yield_max: Union[float, Decimal] = None
    listing_amount_min: Union[float, Decimal] = None
    listing_amount_max: Union[float, Decimal] = None
    listing_category_id: List[Union[int, ListingCategory]] = None
    listing_creation_date_min: Union[str, date] = None
    listing_creation_date_max: Union[str, date] = None
    listing_end_date_min: Union[str, date] = None
    listing_end_date_max: Union[str, date] = None
    listing_monthly_payment_min: Union[float, Decimal] = None
    listing_monthly_payment_max: Union[float, Decimal] = None
    listing_start_date_min: Union[str, date] = None
    listing_start_date_max: Union[str, date] = None
    listing_status: List[Union[int, ListingStatus]] = None
    listing_term: List[Literal[24, 36, 48, 60]] = None
    loan_origination_date_min: Union[str, date] = None
    loan_origination_date_max: Union[str, date] = None
    months_employed_min: int = None
    months_employed_max: int = None
    occupation: List[Union[str, Occupation]] = None
    partial_funding_indicator: bool = None
    percent_funded_min: Union[float, Decimal] = None
    percent_funded_max: Union[float, Decimal] = None
    prior_prosper_loans_min: int = None
    prior_prosper_loans_max: int = None
    prior_prosper_loans_active_min: int = None
    prior_prosper_loans_active_max: int = None
    prior_prosper_loans_balance_outstanding_min: Union[float, Decimal] = None
    prior_prosper_loans_balance_outstanding_max: Union[float, Decimal] = None
    prior_prosper_loans_cycles_billed_min: int = None
    prior_prosper_loans_cycles_billed_max: int = None
    prior_prosper_loans_late_cycles_min: int = None
    prior_prosper_loans_late_cycles_max: int = None
    prior_prosper_loans_late_payments_one_month_plus_min: int = None
    prior_prosper_loans_late_payments_one_month_plus_max: int = None
    prior_prosper_loans_ontime_payments_min: int = None
    prior_prosper_loans_ontime_payments_max: int = None
    prior_prosper_loans_principal_borrowed_min: Union[float, Decimal] = None
    prior_prosper_loans_principal_borrowed_max: Union[float, Decimal] = None
    prior_prosper_loans_principal_outstanding_min: Union[float, Decimal] = None
    prior_prosper_loans_principal_outstanding_max: Union[float, Decimal] = None
    prosper_rating: List[Union[str, ProsperRating]] = [
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
    stated_monthly_income_min: Union[float, Decimal] = None
    stated_monthly_income_max: Union[float, Decimal] = None
    verification_stage_min: Literal[1, 2, 3] = None
    verification_stage_max: Literal[1, 2, 3] = None
    whole_loan_end_date_min: Union[str, date] = None
    whole_loan_end_date_max: Union[str, date] = None
    whole_loan_start_date_min: Union[str, date] = None
    whole_loan_start_date_max: Union[str, date] = None
    co_borrower_application: bool = None
    combined_dti_wprosper_loan_min: Union[float, Decimal] = None
    combined_dti_wprosper_loan_max: Union[float, Decimal] = None
    combined_stated_monthly_income_min: Union[float, Decimal] = None
    combined_stated_monthly_income_max: Union[float, Decimal] = None

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

    principal_balance_pro_rata_share: Union[float, Decimal]
    service_fees_paid_pro_rata_share: Union[float, Decimal]
    principal_paid_pro_rata_share: Union[float, Decimal]
    interest_paid_pro_rata_share: Union[float, Decimal]
    prosper_fees_paid_pro_rata_share: Union[float, Decimal]
    late_fees_paid_pro_rata_share: Union[float, Decimal]
    collection_fees_paid_pro_rata_share: Union[float, Decimal]
    debt_sale_proceeds_received_pro_rata_share: Union[float, Decimal]
    platform_proceeds_net_received: Union[float, Decimal]
    next_payment_due_amount_pro_rata_share: Union[float, Decimal]
    note_ownership_amount: Union[float, Decimal]
    note_sale_gross_amount_received: Union[float, Decimal]
    note_sale_fees_paid: Union[float, Decimal]
    loan_note_id: str
    listing_number: int
    note_status: LoanStatus
    note_status_description: str
    is_sold: bool
    is_sold_folio: bool
    loan_number: int
    amount_borrowed: Union[float, Decimal]
    borrower_rate: Union[float, Decimal]
    lender_yield: Union[float, Decimal]
    prosper_rating: ProsperRating
    term: int
    age_in_months: int
    accrued_interest: Union[float, Decimal]
    payment_received: Union[float, Decimal]
    loan_settlement_status: str
    loan_extension_status: str
    loan_extension_term: int
    is_in_bankruptcy: bool
    co_borrower_application: bool
    origination_date: Union[str, date]
    days_past_due: int
    next_payment_due_date: Union[str, date]
    ownership_start_date: Union[str, date]
    ownership_end_date: Union[str, date] = None
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
    bid_status: BidStatus
    bid_amount: Union[float, Decimal]
    bid_amount_placed: Union[float, Decimal] = None
    bid_result: BidResult = None


class Order(NamedTuple):
    """Represents an order placed on one or more listings."""

    order_id: str
    order_date: Union[str, datetime]
    bid_requests: List[BidRequest]
    order_status: OrderStatus
    source: OrderSource
    order_amount: Union[float, Decimal] = None
    order_amount_placed: Union[float, Decimal] = None
    order_amount_invested: Union[float, Decimal] = None


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
    amount_borrowed: Union[float, Decimal]
    borrower_rate: Union[float, Decimal]
    prosper_rating: ProsperRating
    term: int
    age_in_months: int
    origination_date: Union[str, date]
    days_past_due: int
    principal_balance: Union[float, Decimal]
    service_fees_paid: Union[float, Decimal]
    principal_paid: Union[float, Decimal]
    interest_paid: Union[float, Decimal]
    prosper_fees_paid: Union[float, Decimal]
    late_fees_paid: Union[float, Decimal]
    collection_fees_paid: Union[float, Decimal]
    debt_sale_proceeds_received: Union[float, Decimal]
    loan_status: LoanStatus
    loan_status_description: str
    loan_default_reason: LoanDefaultReason
    next_payment_due_date: Union[str, date]
    next_payment_due_amount: Union[float, Decimal]
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
