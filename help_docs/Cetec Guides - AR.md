## Customer Maintenance

### How to update customer credit limit and terms

- Search for customer in global search
- Click Edit to open customer details
- Update credit limit and terms code
- Click Update to save changes
- Add documentation note:
    - Navigate to customer notes section
    - Click Add Note
    - Detail changes clearly
    - Check sticky checkbox
    - Click OK
- Return to main customer page:
    - Click View
    - Note sticky message at top of page

### How to send an A/R Statement

- Open Cetec ERP -> Accounting -> AR -> AR Summary
- Click Submit
- Select customer for statement
- Click Email PDF
- Enter recipient's email address
- Type email body
- Click Send
- Alternative: Set up automatic statements
    - Select Notifications on customer record
    - Choose Customer Statement Email as notifier type
    - Enter recipient's email
    - Click Create New Notification

## Invoicing

### How to edit and resend an invoice

- AR -> AR List Receivables
- Search for customer by name -> Submit
- Locate invoice number (e.g., 50.1 to 1)
- Click on invoice -> Edit
- Update customer PO number and freet field
- Click Update to save changes
- To resend:
    - Click PDF -> Email PDF
    - Type email body
    - Enter recipient's email in To field
    - Click Send

### How to Create a Bill only invoice

- Sales -> Invoices -> Invoice List
- Choose Create Bill Only Invoice
- Search for customer -> Create
- Scroll down -> click Line_1_Ship_D
- Enter key in Per Part field
- Input resale amount
- Click Update to save
- To review: Click View
- To send: Click PDF

## Processing payments and deposits

### How to process a Prepayment

- Search for order -> click Prepay
- Select customer's payment method
- Enter reference number
- Scroll down -> click Prepay
- Note order is now prepaid
- For quote prepayment:
    - Click Prepay in left-hand navigation of quote
    - Input values as with order prepayment

### How to take payment from a customer

- Accounting -> AR -> AR List Receivables
- Click Pay on customer's invoice
- Select payment method
- Enter payment value
- Enter customer's payment reference
- Note: Oldest invoice automatically applied
    - Can manually select another invoice
    - Can select multiple invoices for single payment
- Click Update to save changes
- Click Payment Complete to finalize

### How to process an overpayment from a customer

- Accounting -> AR -> AR List -> Submit
- Click Pay on invoice
- Enter payment method, value, and reference
- System creates unapplied cash for excess payment
- Click Update to confirm details
- Click Payment Complete to finalize
- To review unapplied cash:
    - AR -> Unapplied Cash List
    - Search for customer -> Submit
    - Click unapplied cash ID for details
    - Note message about overpayment origin

### How to create a credit memo and apply to a customer invoice

- Accounting -> AR -> Credit Memo List -> Create
- Hover over search field to find customer -> click Create
- Enter total credit amount in Resale field
- Include customer's PO number if applicable
- Click Update
- Optional: Change account to be debited
    - Scroll through list
    - Select preferred account
- Apply memo to payment:
    - Click customer name -> AR Statement
    - Click Take Payment
    - Enter payment method, value, reference number
    - Scroll down -> check Include checkbox for credit memo
    - Note combined applied amount
    - Click Update
    - Scroll down -> click Payment Complete

### How to create a deposit

- Accounting -> AR -> Deposit List -> Submit
- Click deposit ID (typically corresponds to day/week of collections)
- View all AR payments in deposit
- Ensure deposit value matches total AR payments
- Note: All AR payments must be finalized before deposit can be finalized
- If needed, change account for deposit
- Click Update to confirm
- Click Deposit to finalize
- Optional: Click Ledger to review corresponding ledger activity

## A/R Reporting

### How to Run A/R aging and detail reports

- Accounting -> AR -> AR Summary -> Submit
- In AR Summary report:
    - Choose value of aging window (total or per customer)
    - Click link to drill into AR details
    - View breakdown of total within aging window
- Adjust date ranges and customer selection as needed

### How to Review and print A/R by Customer

- Accounting -> AR -> AR by Customer -> Submit
- View details by customer:
    - Invoices
    - Unapplied cash
    - Credit memos
    - Aging buckets
- For printable version:
    - Click PDF
    - Download directly to device

[[Cetec Guides - AP]]