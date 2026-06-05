# Payment Methods

## Supported Payment Method

### Cash on Delivery

- **Method**: `cash_on_delivery` in the frontend checkout
- **Backend value**: `cod`
- **Status**: Enabled

## Flow

1. Buyer completes checkout details.
2. Buyer selects Cash on Delivery.
3. Stock is reduced when the order is placed.
4. Order is saved locally for buyer tracking.
5. Buyer pays when the order arrives.

## Notes

- Digital wallet payment has been removed from this system.
- The checkout page should only show Cash on Delivery.
- No frontend redirect payment routes are active.
- No backend digital payment initiate or verify endpoints are active.
