## Customer Maintenance
### Create a customer and add contacts & addresses
- Sales -> Customers -> Customer List -> Create New (Customer) -> Create
- Edit/Add Info -> Ok
- View -> Add Address -> Enter info -> Update
- Add Contact -> Ok
### Create Note in customer record
- Search for customer in global search
- Click Notes -> Add Note (sticky) -> Ok
- View -> Orders -> Click an Order
- Sticky notes are viewable from orders quotes and invoices
## Quote Creation
### Create a new quote
- #### Create Header
- Sales -> Quotes -> New Quote -> Pencil Icon
- Enter name, customer, PO, ship settings -> Ok
- #### Create quote lines
- Add line
- Enter part no. & cust part no 
- Enter dates, lead time, quantity, pricing
- Set trans code - Ok.
### Change Quote Transcode
- In a quote -> edit line
	- Stock - shipped from inventory without assembly
	- Build - (Work order)
	- Build-for-stock work orders are different from standard work orders in that build for stock orders are charged against an inter-company customer to accurately track and reconcile inventory cost. Thus, fulfilling a build-for-stock order means that the inventory quantity of assembly components decreases, the assembled product is then ‘bought’ from yourself, baking in any labor costs associated with the build, and For a build-for-stock order, you'll need to set up an inter-company "customer."
	- Customer -> Customer List -> Create New (Internal Customer) -> Create
	- Edit -> Inter-Company Account - Yes
	- Charge - orders with no impact on inventory - repairs, installation etc.
### Clone, Delete, & View Part Info from Quote Line
- Edit / View - Pencil Icon
- Delete - X Icon
- Clone - White square with blue arrows
### How to edit the BOM worksheet
- Sales -> Quotes -> Quote List -> Line Item ID -> Paper Icon
- Edit quantity or costs
- Click edit to add markup and margin -> Ok and transfer to quote

## Quote Management
### How to Send a Quote
- From quote -> send+
	- Quick (downloads default pdf)
	- PDF/EMAIL
		- has settings
		- can email or download
### How to run a Quote Report
- Sales -> My Quotes -> Open/Pending/Closed
- Use Filters
### How to Clone and Close Quotes
- Sales -> Quotes -> Quote List -> Submit
- Select quote number -> Quoting Tools+
	- Clone this quote
	- Close this quote
		- Resolution type -> Reconcile lines & close quote
- #### View quote data corresponding to closed quote
	- Quotes -> Quote Stats
### How to use WorkFlows
- Global search for order, po, ncr, etc
- Click Pending Approval 
### How to create an order
- Global search for quote number
- Commit to Order/Commit Order
## Order Management##
### How to find a specific order
- Orders -> Order List -> Enter Filters -> Submit **or**
#### From customer
- Customers -> customer list
- Search customer -> select -> Orders
#### From parts
- Parts -> Lists -> Search by part -> Submit -> Part no. -> Sales+ -> Orders.
### How to edit an order
- From order -> edit -> submit
### How to send order acknowledgement to customer
- From order no. -> Pdf with filters -> Email PDF
### How to run the order list to see backlog
- Sales -> Orders -> Order List -> Submit
- Closed orders are in sales -> invoices -> invoice list
- Filter with +/- columns
### How do I fulfill an order
-  Search for order
- Click 3 in the header -> Set qty/fully ship then update
- Set 4 pick qty and update -> invoice ship order
- Create invoice -> Packing slip -> print
### How to log an RMA
- Sales -> Invoices -> Invoice List -> Submit
- Click Invoice -> Create RMA
- Set type, reason code, status code, comments -> ok.
- Set return qty and defect code -> update
- Set receiving po -> create receiving po
- From RMA -> Click Invoice
- From Order -> Click RMAS + -> RMA
### View Labor Plan
- From part -> revisions -> labor plan


[[Cetec Guides - Inventory]]