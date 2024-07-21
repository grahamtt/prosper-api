from decimal import Decimal
from typing import List, Literal, Optional

from pydantic import BaseModel

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
    ListLoansSortBy,
    ListNotesSortBy,
    ListOrdersSortBy,
    LoanDefaultReason,
    LoanStatus,
    Occupation,
    OrderSource,
    OrderStatus,
    ProsperRating,
    SearchListingsSortBy,
    SortOrder,
)


class AmountsByRating(BaseModel):
    """Holds arbitrary float | Decimal amounts bucketed by Prosper rating."""

    NA: Decimal
    HR: Decimal
    E: Decimal
    D: Decimal
    C: Decimal
    B: Decimal
    A: Decimal
    AA: Decimal


class Account(BaseModel):
    """Holds account-level information, such as current balances."""

    available_cash_balance: Decimal
    pending_investments_primary_market: Decimal
    pending_investments_secondary_market: Decimal
    pending_quick_invest_orders: Decimal
    total_principal_received_on_active_notes: Decimal
    total_amount_invested_on_active_notes: Decimal
    outstanding_principal_on_active_notes: Decimal
    total_account_value: Decimal
    pending_deposit: Decimal
    last_deposit_amount: Decimal
    last_deposit_date: str
    last_withdraw_amount: Decimal
    last_withdraw_date: str
    external_user_id: str
    prosper_account_digest: str
    invested_notes: AmountsByRating
    pending_bids: AmountsByRating


class _ListResponse(BaseModel):
    result: List[BaseModel]
    result_count: int
    total_count: int


class CreditBureauValues(BaseModel):
    """Represents data sourced from TransUnion."""

    g102s_months_since_most_recent_inquiry: Decimal
    credit_report_date: str
    at02s_open_accounts: Decimal
    g041s_accounts_30_or_more_days_past_due_ever: Decimal
    g093s_number_of_public_records: Decimal
    g094s_number_of_public_record_bankruptcies: Decimal
    g095s_months_since_most_recent_public_record: Decimal
    g218b_number_of_delinquent_accounts: Decimal
    g980s_inquiries_in_the_last_6_months: Decimal
    re20s_age_of_oldest_revolving_account_in_months: Decimal
    s207s_months_since_most_recent_public_record_bankruptcy: Decimal
    re33s_balance_owed_on_all_revolving_accounts: Decimal
    at57s_amount_delinquent: Decimal
    g099s_public_records_last_24_months: Decimal
    at20s_oldest_trade_open_date: Decimal
    at03s_current_credit_lines: Decimal
    re101s_revolving_balance: Decimal
    bc34s_bankcard_utilization: Decimal
    at01s_credit_lines: Decimal
    fico_score: FICOScore


class Listing(BaseModel):
    """Represents a Prosper listing.

    Contains the information needed for an investor to make an informed decision about
    whether to invest in a potential loan.
    """

    listing_number: int
    prosper_rating: ProsperRating
    listing_title: str
    listing_start_date: str
    listing_creation_date: str
    listing_status: ListingStatus
    listing_status_reason: str
    invested: bool
    biddable: bool
    has_mortgage: bool
    credit_bureau_values_transunion_indexed: CreditBureauValues
    employment_status_description: EmploymentStatus
    investment_type_description: str
    last_updated_date: str
    decision_bureau: str
    member_key: str
    borrower_state: BorrowerState
    co_borrower_application: bool
    income_verifiable: bool
    lender_yield: Decimal
    occupation: Optional[Occupation] = None
    loan_number: Optional[int] = None
    listing_end_date: Optional[str] = None
    loan_origination_date: Optional[str] = None
    months_employed: Optional[Decimal] = None
    investment_product_id: Optional[InvestmentProduct] = None
    listing_amount: Optional[Decimal] = None
    amount_funded: Optional[Decimal] = None
    amount_remaining: Optional[Decimal] = None
    percent_funded: Optional[Decimal] = None
    partial_funding_indicator: Optional[bool] = None
    funding_threshold: Optional[Decimal] = None
    borrower_rate: Optional[Decimal] = None
    borrower_apr: Optional[Decimal] = None
    listing_term: Optional[int] = None
    listing_monthly_payment: Optional[Decimal] = None
    prosper_score: Optional[int] = None
    listing_category_id: Optional[int] = None
    income_range: Optional[IncomeRange] = None
    income_range_description: Optional[str] = None
    stated_monthly_income: Optional[Decimal] = None
    dti_wprosper_loan: Optional[Decimal] = None
    lender_indicator: Optional[int] = None
    channel_code: Optional[int] = None
    amount_participation: Optional[Decimal] = None
    investment_typeid: Optional[InvestmentType] = None
    estimated_monthly_housing_expense: Optional[Decimal] = None
    historical_return: Optional[Decimal] = None
    historical_return_10th_pctl: Optional[Decimal] = None
    historical_return_90th_pctl: Optional[Decimal] = None
    prior_prosper_loans_active: Optional[int] = None
    prior_prosper_loans: Optional[int] = None
    prior_prosper_loan_earliest_pay_off: Optional[int] = None
    prior_prosper_loans_principal_borrowed: Optional[Decimal] = None
    prior_prosper_loans_principal_outstanding: Optional[Decimal] = None
    prior_prosper_loans_balance_outstanding: Optional[Decimal] = None
    prior_prosper_loans_cycles_billed: Optional[int] = None
    prior_prosper_loans_ontime_payments: Optional[int] = None
    prior_prosper_loans_late_cycles: Optional[int] = None
    prior_prosper_loans_late_payments_one_month_plus: Optional[int] = None
    prior_prosper_loans31dpd: Optional[Decimal] = None
    max_prior_prosper_loan: Optional[Decimal] = None
    min_prior_prosper_loan: Optional[Decimal] = None
    verification_stage: Optional[int] = None
    combined_dti_wprosper_loan: Optional[Decimal] = None
    combined_stated_monthly_income: Optional[Decimal] = None


class SearchListingsRequest(BaseModel):
    """Request for searching listings."""

    sort_by: SearchListingsSortBy = SearchListingsSortBy.LENDER_YIELD
    sort_dir: SortOrder = SortOrder.DESCENDING
    offset: Optional[int] = None
    limit: Optional[int] = None
    biddable: bool = True
    invested: Optional[bool] = None

    amount_funded_min: Optional[Decimal] = None
    amount_funded_max: Optional[Decimal] = None
    amount_remaining_min: Optional[Decimal] = None
    amount_remaining_max: Optional[Decimal] = None
    borrower_rate_min: Optional[Decimal] = None
    borrower_rate_max: Optional[Decimal] = None
    borrower_state: Optional[List[BorrowerState]] = None
    dti_wprosper_loan_min: Optional[Decimal] = None
    dti_wprosper_loan_max: Optional[Decimal] = None
    employment_status_description: Optional[List[EmploymentStatus]] = None
    estimated_monthly_housing_expense_min: Optional[Decimal] = None
    estimated_monthly_housing_expense_max: Optional[Decimal] = None
    fico_score: Optional[List[FICOScore]] = None
    has_mortgage: Optional[bool] = None
    income_range: Optional[List[IncomeRange]] = None
    lender_yield_min: Optional[Decimal] = None
    lender_yield_max: Optional[Decimal] = None
    listing_amount_min: Optional[Decimal] = None
    listing_amount_max: Optional[Decimal] = None
    listing_category_id: Optional[List[ListingCategory]] = None
    listing_creation_date_min: Optional[str] = None
    listing_creation_date_max: Optional[str] = None
    listing_end_date_min: Optional[str] = None
    listing_end_date_max: Optional[str] = None
    listing_monthly_payment_min: Optional[Decimal] = None
    listing_monthly_payment_max: Optional[Decimal] = None
    listing_start_date_min: Optional[str] = None
    listing_start_date_max: Optional[str] = None
    listing_status: Optional[List[ListingStatus]] = None
    listing_term: Optional[List[Literal[24, 36, 48, 60]]] = None
    loan_origination_date_min: Optional[str] = None
    loan_origination_date_max: Optional[str] = None
    months_employed_min: Optional[int] = None
    months_employed_max: Optional[int] = None
    occupation: Optional[List[Occupation]] = None
    partial_funding_indicator: Optional[bool] = None
    percent_funded_min: Optional[Decimal] = None
    percent_funded_max: Optional[Decimal] = None
    prior_prosper_loans_min: Optional[int] = None
    prior_prosper_loans_max: Optional[int] = None
    prior_prosper_loans_active_min: Optional[int] = None
    prior_prosper_loans_active_max: Optional[int] = None
    prior_prosper_loans_balance_outstanding_min: Optional[Decimal] = None
    prior_prosper_loans_balance_outstanding_max: Optional[Decimal] = None
    prior_prosper_loans_cycles_billed_min: Optional[int] = None
    prior_prosper_loans_cycles_billed_max: Optional[int] = None
    prior_prosper_loans_late_cycles_min: Optional[int] = None
    prior_prosper_loans_late_cycles_max: Optional[int] = None
    prior_prosper_loans_late_payments_one_month_plus_min: Optional[int] = None
    prior_prosper_loans_late_payments_one_month_plus_max: Optional[int] = None
    prior_prosper_loans_ontime_payments_min: Optional[int] = None
    prior_prosper_loans_ontime_payments_max: Optional[int] = None
    prior_prosper_loans_principal_borrowed_min: Optional[Decimal] = None
    prior_prosper_loans_principal_borrowed_max: Optional[Decimal] = None
    prior_prosper_loans_principal_outstanding_min: Optional[Decimal] = None
    prior_prosper_loans_principal_outstanding_max: Optional[Decimal] = None
    prosper_rating: List[ProsperRating] = [
        ProsperRating.AA,
        ProsperRating.A,
        ProsperRating.B,
        ProsperRating.C,
        ProsperRating.D,
        ProsperRating.E,
        ProsperRating.HR,
    ]
    prosper_score_min: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]] = None
    prosper_score_max: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]] = None
    stated_monthly_income_min: Optional[Decimal] = None
    stated_monthly_income_max: Optional[Decimal] = None
    verification_stage_min: Optional[Literal[1, 2, 3]] = None
    verification_stage_max: Optional[Literal[1, 2, 3]] = None
    whole_loan_end_date_min: Optional[str] = None
    whole_loan_end_date_max: Optional[str] = None
    whole_loan_start_date_min: Optional[str] = None
    whole_loan_start_date_max: Optional[str] = None
    co_borrower_application: Optional[bool] = None
    combined_dti_wprosper_loan_min: Optional[Decimal] = None
    combined_dti_wprosper_loan_max: Optional[Decimal] = None
    combined_stated_monthly_income_min: Optional[Decimal] = None
    combined_stated_monthly_income_max: Optional[Decimal] = None

    listing_number: Optional[List[int]] = None


class SearchListingsResponse(_ListResponse):
    """The listings matching the given search parameters."""

    result: List[Listing]


class Note(BaseModel):
    """Represents the Prosper note.

    The note holds information about the borrowers obligation to the individual lenders.

    See Also:
        https://developers.prosper.com/docs/investor/notes-api/
    """

    principal_balance_pro_rata_share: Decimal
    service_fees_paid_pro_rata_share: Decimal
    principal_paid_pro_rata_share: Decimal
    interest_paid_pro_rata_share: Decimal
    prosper_fees_paid_pro_rata_share: Decimal
    late_fees_paid_pro_rata_share: Decimal
    collection_fees_paid_pro_rata_share: Decimal
    debt_sale_proceeds_received_pro_rata_share: Decimal
    platform_proceeds_net_received: Decimal
    next_payment_due_amount_pro_rata_share: Decimal
    note_ownership_amount: Decimal
    note_sale_gross_amount_received: Decimal
    note_sale_fees_paid: Decimal
    loan_note_id: str
    listing_number: int
    note_status: LoanStatus
    note_status_description: str
    is_sold: bool
    is_sold_folio: bool
    loan_number: int
    amount_borrowed: Decimal
    borrower_rate: Decimal
    lender_yield: Decimal
    prosper_rating: ProsperRating
    term: int
    age_in_months: int
    accrued_interest: Decimal
    payment_received: Decimal
    loan_settlement_status: str
    loan_extension_status: str
    loan_extension_term: int
    is_in_bankruptcy: bool
    co_borrower_application: bool
    origination_date: str
    days_past_due: int
    next_payment_due_date: str
    ownership_start_date: str
    ownership_end_date: Optional[str] = None
    note_default_reason: Optional[LoanDefaultReason] = None
    note_default_reason_description: Optional[str] = None
    servicing_collection_agency_queue: Optional[str] = None


class ListNotesRequest(BaseModel):
    """Request for searching notes."""

    sort_by: ListNotesSortBy = ListNotesSortBy.PROSPER_RATING
    sort_dir: SortOrder = SortOrder.DESCENDING
    offset: Optional[int] = None
    limit: Optional[int] = None


class ListNotesResponse(_ListResponse):
    """The notes matching the given search parameters."""

    result: List[Note]


class BidRequest(BaseModel):
    """Represents an individual bid on a listing.

    An order may contain multiple bids on multiple listings.
    """

    listing_id: int
    bid_status: BidStatus
    bid_amount: Decimal
    bid_amount_placed: Optional[Decimal] = None
    bid_result: Optional[BidResult] = None


class Order(BaseModel):
    """Represents an order placed on one or more listings."""

    order_id: str
    order_date: str
    bid_requests: List[BidRequest]
    order_status: OrderStatus
    source: OrderSource
    order_amount: Optional[Decimal] = None
    order_amount_placed: Optional[Decimal] = None
    order_amount_invested: Optional[Decimal] = None


class ListOrdersRequest(BaseModel):
    """Request for listing orders."""

    sort_by: ListOrdersSortBy = ListOrdersSortBy.PROSPER_RATING
    sort_dir: SortOrder = SortOrder.DESCENDING
    offset: Optional[int] = None
    limit: Optional[int] = None


class ListOrdersResponse(_ListResponse):
    """The orders that match the given search params."""

    result: List[Order]


class Loan(BaseModel):
    """Represents the totality of a loan the lender participates in."""

    loan_number: int
    amount_borrowed: Decimal
    borrower_rate: Decimal
    prosper_rating: ProsperRating
    term: int
    age_in_months: int
    origination_date: str
    days_past_due: int
    principal_balance: Decimal
    service_fees_paid: Decimal
    principal_paid: Decimal
    interest_paid: Decimal
    prosper_fees_paid: Decimal
    late_fees_paid: Decimal
    collection_fees_paid: Decimal
    debt_sale_proceeds_received: Decimal
    loan_status: LoanStatus
    loan_status_description: str
    loan_default_reason: LoanDefaultReason
    next_payment_due_date: str
    next_payment_due_amount: Decimal
    loan_default_reason_description: Optional[str] = None


class ListLoansRequest(BaseModel):
    """Request for searching loans."""

    sort_by: ListLoansSortBy = ListLoansSortBy.PROSPER_RATING
    sort_dir: SortOrder = SortOrder.DESCENDING
    offset: Optional[int] = None
    limit: Optional[int] = None


class ListLoansResponse(_ListResponse):
    """The loans that match the given parameters."""

    result: List[Loan]
