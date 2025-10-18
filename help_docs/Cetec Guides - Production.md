## Workorder Release/Print

### Order Release - How to Print a Licence Plate and Pick List

- Warehouse -> Release to Pick
- Choose either:
    - Release Orders (All)
    - Sales Orders Only
    - Build Orders Only
- Filter report or click Submit to view all
- For license plate (Line Plate Traveler):
    - Find order -> click Plate
    - View and print license plate
- For pick list:
    - Find order -> click Docs
    - Click Part Pick List to open document
    - This screen also provides access to license plate
- Alternative access:
    - From any work order screen -> left-side menu -> Documents

### How to batch release and assign work orders

- Open Cetec ERP -> Warehouse -> Release to Pick -> Release Build Orders
- Transcode field defaults to Build
- Filter search criteria or click Submit to view all
- Select orders for release:
    - Find desired orders
    - Click Move checkbox next to each
- For batch printing:
    - Click Batch Print
    - Cetec generates line plates for selected orders
- To assign users:
    - Assign individually or enter name in field at top of column for all
    - Choose next build stage from dropdown
    - Click Move Orders
- System advances orders and saves user assignments
- Confirmation message appears at top of screen

### How to find released orders by location

- Production -> Orders -> Production Order List
- Choose desired location
- For multiple locations:
    - Hold Control (Ctrl) key while clicking each location
- Add additional filters if needed or click Submit
- Cetec displays list of released orders for selected location(s)
## Picking

### How to pick and Dekit parts on Orders

- Search for order using Global Search:
    - Enter order number or PO number
    - Click result
- Click Line 1 -> Work Order View -> Pick Parts
- Pick options:
    - Enter quantity for each part individually
    - Or scroll to bottom -> Pick All Lines to select entire inventory list
- Click Update to confirm
- To D-kit (unpick) parts:
    - Click D-kit Parts
    - Enter return quantity (full or partial) on each line
    - Click Update to return those parts
    - Alternative: Click Kit Line 1 link at top to D-kit all picked parts in full

### Picking - How to overpick a workorder

- Go to Pick Parts screen
- View Quantity Need listed
- Manually enter higher pick quantity as instructed
- Click Update
- When warning pop-up appears:
    - Click OK
    - Click orange Update button again to confirm
- Actual pick quantity will update and display on screen

### How to perform a part request

- From Work Order screen -> click Parts
- Locate needed part -> click Request More
- In pop-up window:
    - Enter quantity needed
    - Check box if request is due to scrap
    - Select a reason
    - Add relevant comments
    - Click Send to submit
- To fulfill the request:
    - Go to Part Request List
    - Click on relevant request number
    - Review comments and quantity requested
    - Find appropriate bin
    - Enter pick quantity
    - Choose appropriate Part Request Status
    - Click Update to save
- On Pick Parts screen:
    - Picked quantity for that part will be highlighted in orange
    - Orange indicates quantity exceeds original quantity needed
## Job Tracking

### How to run the production order list

- Production -> Orders -> Production Order List
- Default: displays all open build orders (internal and external)
- Click Submit to view results
- For specific searches:
    - Click More Options for additional search parameters
    - For specific work locations: select location(s) by holding Control (Ctrl) key while clicking
    - Sort chronologically by clicking Work Start Date column header
- Production Status field helps find:
    - Late orders
    - Orders with critical shortages
    - Other key statuses
- For detailed production data:
    - Check Show Production Management box before clicking Submit
    - Adds columns showing: on target, short per allocation, missing parts
- To view specific work order: click on order number from list

### How to move work orders to work locations in the routing steps

- Find order using Global Search
- Type order number -> click line number
- View work order/job details
- Scroll to Move Location dropdown menu
- Select next stage in production
- Click Move to Next to update status
- To review location change history: click History tab
- To review multiple orders:
    - Production -> Orders -> Production Order List
    - Select desired location(s)
    - Click Submit to view relevant jobs

### How to log time on a work order

- Search for order number using Global Search
- Click line item to open Work Order/Job view
- Click Start Work
- System shows pop-up notification that time begins logging immediately
- Time log segment starts
- Optionally enter number of pieces finished
- Click Stop Work to end time log
- Alternative: Click Start Work again to continue logging time if needed

### Workorder management - Complete required work instructions

- Access required instructions:
    - Click View
    - Or navigate to Instructions tab
- Required instructions are highlighted:
    - Red box around input field
    - Word "Required" appears in red
- Add your response to the field
- Click Done
- System returns to main work order screen
- Number of missing required work instructions updates (typically to zero if all completed)
## Workorder Management

### Delete work History

- Click on History tab
- Scroll to Work History section
- Find incorrectly entered hour of work
- Click Delete
- When pop-up appears asking "Are you sure you want to delete this work history?"
- Click OK

### Outsourcing PO's

- Set up order production location for outsourcing:
    - Admin -> Maintenance -> Data Maintenance
    - Search for Ordline Status Data Maintenance Table -> Submit
    - Click Ordline Status
    - Click Add Record
    - Enter description for vendor location
    - Check As Outsourcing checkbox
    - Fill in other information -> Submit
- Add location to BOM revision labor plan:
    - From part record -> left-side menu -> Revisions
    - Find revision -> click Labor Plan
    - Select outsourcing location in field left of orange Add button
    - Click Add
    - Add expected lead time -> Update
    - Position correctly: hover over number on left, click and drag to proper place
- Update quote and create order:
    - Refresh quote page
    - Click Commit to Order -> Commit Order
    - Go to Work Order View in left-side menu
    - Move work order to outsourcing location -> Move to Next
- Set up vendor and outsource PRC part:
    - Create outsourcing vendor:
        - Purchasing -> Vendors -> Vendor List
        - Create New -> enter vendor name -> Create
    - Create outsource PRC:
        - Parts -> Lists -> PRC List -> Create PRC
        - Enter PRC code -> Create
        - Add description -> Update
    - Create part for outsource PO:
        - Lists -> Part List -> Create New
        - Choose PRC code, enter part number, select location, add description
        - Click Create
- Create outsource PO:
    - Click Outsource PO
    - Enter vendor and part details
    - Fill relevant information
    - Click Create Outsource PO
- Access outsource PO documents:
    - From order overview -> Outsource POs Plus
    - Click into your outsource PO
    - Options:
        - Packing Slip for vendor
        - PDF Export for PO PDF

### Serial Assemblies

- Issuing Serials to Top-Level Parts:
    - From Work Order screen -> click Serials
    - Enter number of serials to assign (up to maximum in parentheses)
    - Check box to reset serial sequence if needed
    - Click Submit
    - Scroll down to view created serials
- Picking Serialized Parts to a Work Order:
    - Work Order screen -> Pick Parts in left-side menu
    - For serialized parts:
        - To find serial numbers: click part record -> scroll to correct warehouse
        - View part bin data -> find bin -> click Pieces link
        - On pick screen: enter serial numbers
        - Use Update or Tab key to move through entries
        - Green highlight indicates quantity met, blue means more needed
    - For picking from multiple bins:
        - Look up serial numbers from part record
        - Enter on pick screen
        - Pick from additional bins if needed to fulfill quantity
- Associating Component Serials with Top-Level Assemblies:
    - Return to Serial screen -> scroll to Component Piece to Top-Level Serial Association
    - Check BOM revision (Parts tab) for quantity per assembly
    - Enter top-level serial number for each component's serial number
    - Assign correct number of component serials based on BOM
    - Click Submit to confirm
- Viewing Serial Numbers on Reports:
    - After invoicing: Invoices -> Serial List
    - View top-level serial numbers with associated component serial numbers

### How to split a Line

- Production -> Orders -> Production Order List
- Search for work order to split
- Left side menu -> Maint Etc Plus -> Split Line
- Check box to split work done with quantity if needed
- Enter quantity for new line
- Click Split
- When menu appears for quantity adjustment, click Scale to Pick
- Success message confirms split
- Result: two lines on work order with divided quantities
## Complete Orders

### How to receive an internal build order

- Ensure all lines are fully picked:
    - Green-highlighted Quantity Picked indicates full quantity available
- Complete and receive the order:
    - Either click 5 in blue header -> Complete
    - Or select Complete Receive from left side menu
- Set finish quantity:
    - Manually enter finish quantity
    - Or click Complete All to automatically fill quantity
- Review component parts to be relieved from inventory
- Click Complete Receive Product to finalize
- Success message appears at top of screen
- System automatically navigates to PO Receipt
- From there, navigate to invoice if needed

### How to ship an external sales order

- Ensure lines for shipping are fully picked:
    - Green-highlighted Quantity Picked indicates full quantity available
- Complete the work order:
    - Click 5 in blue header -> Invoice Ship
    - Or click Invoice Ship link in left-side menu
- Set ship quantity:
    - Manually enter ship quantity
    - Or click Fully Ship to automatically fill quantity
- Review parts to be relieved from inventory
- Click Update to save ship quantity
- Print options available from this screen:
    - Packing slip
    - Packing labels
- Complete order: Click Create Invoice
- Success message appears at top of screen

[[Cetec Guides - Quality]]