from collections import namedtuple

Account = namedtuple(
    "Account",
    [
        "available_cash_balance",
        "pending_investments_primary_market",
        "pending_investments_secondary_market",
        "pending_quick_invest_orders",
        "total_principal_received_on_active_notes",
        "total_amount_invested_on_active_notes",
        "outstanding_principal_on_active_notes",
        "total_account_value",
        "pending_deposit",
        "last_deposit_amount",
        "last_deposit_date",
        "last_withdraw_amount",
        "last_withdraw_date",
        "external_user_id",
        "prosper_account_digest",
        "invested_notes",
        "pending_bids",
    ],
)

AmountsByRating = namedtuple(
    "AmountsByRating", ["NA", "HR", "E", "D", "C", "B", "A", "AA"]
)
