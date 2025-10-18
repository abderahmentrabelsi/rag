## Vouchers

### How to enter a voucher

- Accounting -> AP -> Add Voucher
- Enter details:
    - Vendor invoice number
    - Search for vendor
    - Enter total invoice amount in vendor requested field
- Scroll down -> search for POs to pay
- Click Add All to include all receipt lines
- Click Add Break
- Choose Additional Splits for Freight, tax, etc.
    - Enter amount for each split
    - Adjust as needed
- Scroll up -> click Submit
- Note: Options for dates:
    - Receive date: manual or auto-populate
    - Pay by date: auto-populates from vendor terms (checkbox to edit manually)
    - Invoice date: can manually change if different from received date

### How to pay a bill and print a check

- Accounting -> AP -> Add Voucher
- Enter:
    - Vendor invoice hash
    - Vendor name
    - Vendor requested amount
- Scroll down -> click Add Break
- Specify break details:
    - Account to map invoice
    - Value for that account
- Scroll down -> click New Payment
- Select vouchers to pay
- Specify payment account
- Click Mark as Paid
- Click System Check link to view/print
- Click PDF

## AP Payments

### How to Create, Approve, and Pay Vouchers

- AP -> Add Voucher
- Enter:
    - Vendor's invoice
    - Vendor name
    - Vendor requested amount (invoice total)
- Scroll down -> Search the PO you're paying
- Click Add to pay specific PO receipt
- Scroll up -> click Add Break for other splits
- Add all details -> click Submit
- Assign for approval:
    - Use workflow tool
    - Select employee (e.g., John Smith)
    - Click Needs Review
- For approver (John Smith):
    - Navigate to Voucher List
    - Select Needs Review -> Submit
    - Find voucher -> click Voucher ID
    - Click Approve to assign back
- For payment processor (Susan Smith):
    - Create new payment ID
    - Include vouchers to pay
    - Include/apply any debit memos
    - Select payment method (e.g., Wire)
    - Click Mark as Paid

### How to Run the Voucher List and Batch Pay Vouchers

- Accounting -> AP -> Voucher List
- Set filters:
    - State filter: Approved
    - Date range for payment due date
- Click Submit
- Click Batch checkbox in header row
- Click Batch Pay Selected
- Select:
    - GL account for payment
    - Payment type
- Click Pay Selected Vouchers

### How to Create Debit Memo and Apply it to a Vendor Payment

- Accounting -> AP -> Debit Memo List
- Click Create Debit Memo
- Enter vendor information -> click Create
- Enter:
    - Total amount
    - Description
- Select account to credit value
- Click Update
- Apply to payment:
    - AP -> AP Payment List -> Submit
    - Select AP Payment ID
    - Include voucher to pay
    - Include debit memo to apply
    - Scroll down -> click Update
    - Click Mark as Paid
- Verify: Click Debit Memo ID to confirm it's closed/applied

### How to Process a Vendor Prepayment

- Set up GL mapping:
    - Admin -> Config Settings
    - GL Transaction Mappings
    - Vendor Unapplied Cash
    - Select account to debit (typically prepaid inventory)
    - Click Set
- Create prepayment:
    - Search for PO in Global Search
    - Click Prepay on left-hand side
    - Enter Vendor Prepayment Amount
    - Select payment method
    - Click Prepay
- View prepayment details:
    - Click Prepayments Plus
    - Click specific prepayment to view details
    - Click Ledger to see transaction implications
- Create voucher for final invoice:
    - Enter standard voucher information
    - Attach PO receipt per normal process
    - Click Submit
- Apply prepayment to final payment:
    - Click New Payment at bottom of voucher
    - In Vendor Unapplied Cash section:
        - Check Include checkbox
        - Enter amount in Apply text box
    - Scroll down -> click Voucher ID being paid
    - Scroll up -> click Update
    - Click Mark as Paid
- Review ledger impact:
    - Click Ledger in left-side menu
- Transaction flow:
    - Unapplied Cash AP payment: debits Prepaid Inventory, credits Cash AP
    - Receipt: impacts inventory and accrued AP
    - Voucher: impacts accrued and AP accounts
    - AP Payment: credits Prepaid Inventory account
- View vendor unapplied cash report:
    - Accounting -> AP -> Vendor Unapplied Cash List
    - Set filters as needed
    - Click Submit
    - Status of closed means prepayment applied

## Check Runs & Bank Reconcile

### How to Perform a Check Run

- Accounting -> AP -> Check Register
- Choose System Check as payment type
- Click Submit
- Click Print checkbox in header row
- Click Batch Print

### How to Perform a Bank Reconcile

- Accounting -> Audit -> Account Reconcile
- Click New Reconcile
- Select Account
- Enter statement date
- Click Account
- Enter ending balance from bank statement
- Click Create
- Enter beginning balance
- Select items that apply to this statement:
    - AP pasyments and checks
    - Deposits
- Scroll up -> click Update
- Verify totals produce difference of zero dollars
- Click Update to finalize

[[Cetec Guides - Index]]