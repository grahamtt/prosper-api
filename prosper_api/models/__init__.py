from typing import List, NamedTuple


class AmountsByRating(NamedTuple):
    NA: float
    HR: float
    E: float
    D: float
    C: float
    B: float
    A: float
    AA: float


class Account(NamedTuple):
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


class ListResponse(NamedTuple):
    result: List[NamedTuple]
    result_count: int
    total_count: int


class Listing(NamedTuple):
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
    credit_bureau_values_transunion_indexed: dict
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
    max_prior_prosper_loan: float = None
    min_prior_prosper_loan: float = None
    verification_stage: str = None
    combined_dti_wprosper_loan: float = None
    combined_stated_monthly_income: float = None


class SearchListingsResponse(ListResponse):
    result: List[Listing]


class Note(NamedTuple):
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


class ListNotesResponse(ListResponse):
    result: List[Note]


class BidRequest(NamedTuple):
    listing_id: int
    bid_status: str
    bid_amount: float
    bid_amount_placed: float = None
    bid_result: str = None


class Order(NamedTuple):
    order_id: str
    order_date: str
    bid_requests: List[BidRequest]
    order_status: str
    source: str
    order_amount: float = None
    order_amount_placed: float = None
    order_amount_invested: float = None


def build_order(order_dict):
    order_dict["bid_requests"] = [BidRequest(**b) for b in order_dict["bid_requests"]]
    return Order(**order_dict)


class ListOrdersResponse(ListResponse):
    result: List[Order]
