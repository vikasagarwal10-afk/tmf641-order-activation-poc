# TMF641 Order Management POC — Working Demo

## Test Results

### Idempotency Test ✅
Same request twice → Same orderId (no duplicate orders)

### SLA Prediction ✅
- 5G Gaming Slice: 10 seconds predicted
- Home Broadband: 30 seconds predicted

### Order Tracking ✅
GET /orders returns all created orders

## Live Demo Commands
```bash
# Create order
curl -X POST http://localhost:8000/order -H "Content-Type: application/json" -H "x-request-id: test-001" -H "x-subscriber-id: sub-123" -d '{"orderItem": [{"productId": "5g_slicing_gaming", "action": "add"}]}'

# Get order
curl http://localhost:8000/order/b287004a-598c-4d48-bc64-12cbd57bed0b
Architecture Decision Record (ADR)
Why Idempotency?
Without it, network retries or agent double-clicks create duplicate orders → double billing → customer churn.

Why SLA Prediction?
Customers abandon orders if activation takes too long. Predicting SLA before order sets correct expectations.
