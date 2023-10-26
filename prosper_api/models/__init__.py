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
    occupation: str
    investment_type_description: str
    last_updated_date: str
    decision_bureau: str
    member_key: str
    borrower_state: str
    co_borrower_application: bool
    income_verifiable: bool
    loan_number: int = None
    listing_end_date: str = None
    loan_origination_date: str = None
    months_employed: float = 0.0
    investment_product_id: int = 0
    listing_amount: float = 0.0
    amount_funded: float = 0.0
    amount_remaining: float = 0.0
    percent_funded: float = 0.0
    partial_funding_indicator: bool = False
    funding_threshold: float = 0.0
    lender_yield: float = 0.0
    borrower_rate: float = 0.0
    borrower_apr: float = 0.0
    listing_term: int = 0
    listing_monthly_payment: float = 0.0
    prosper_score: int = 0
    listing_category_id: int = 0
    income_range: int = 0
    income_range_description: str = ""
    stated_monthly_income: float = 0.0
    dti_wprosper_loan: float = 0.0
    lender_indicator: int = 0
    channel_code: int = 0
    amount_participation: float = 0.0
    investment_typeid: int = 0
    estimated_monthly_housing_expense: float = 0.0
    historical_return: float = 0.0
    historical_return_10th_pctl: float = 0.0
    historical_return_90th_pctl: float = 0.0
    prior_prosper_loans_active: int = 0
    prior_prosper_loans: int = 0
    prior_prosper_loan_earliest_pay_off: int = 0
    prior_prosper_loans_principal_borrowed: float = 0.0
    prior_prosper_loans_principal_outstanding: float = 0.0
    prior_prosper_loans_balance_outstanding: float = 0.0
    prior_prosper_loans_cycles_billed: int = 0
    prior_prosper_loans_ontime_payments: int = 0
    prior_prosper_loans_late_cycles: int = 0
    prior_prosper_loans_late_payments_one_month_plus: int = 0
    max_prior_prosper_loan: float = 0.0
    min_prior_prosper_loan: float = 0.0
    verification_stage: str = None


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


class Order(NamedTuple):
    order_id: str
    bid_requests: List[dict]
    order_amount: float
    order_amount_placed: float
    order_amount_invested: float
    order_status: str
    source: str
    order_date: str


class ListOrdersResponse(ListResponse):
    result: List[Order]
