## Receiving Inspections

### How to create receiving inspections

- Navigate to receiving screen:
    - Click appropriate links
- On receiving screen, locate Inspection section
- To create inspection document:
    - Enter quantity accepted
    - Enter quantity rejected
    - Optionally enter inspection notes
    - Click Receive
- System creates:
    - Inspection document
    - NCR (Non-Conformance Report) if quantity rejected
- View inspection document:
    - Click link to navigate to inspection document
    - Edit as needed
    - Note automatic links to PO, part record, and receipt document
- View NCR:
    - Click NCR link from inspection document
    - Note default information:
        - Link to inspection document
        - Pre-filled part number, rejected quantity, and PO number

## In process Inspections

### How to create in process inspections

- Navigate to work order:
    - Production -> Orders -> Production Order List
    - Click Submit
    - Click into appropriate work order
- From Work Order screen:
    - Select Inspections from left-hand menu
- Fill required fields (outlined in red):
    - Enter quantity being inspected
    - Select Inspection Type:
        - In Process (before assembly complete)
        - Final (after assembly complete)
    - Enter quantity accepted
    - Indicate inspection pass number
    - Enter quantity rejected
    - Enter date code
    - Enter assembler's name
    - Add optional information
- Click Submit
- Enter inspection details:
    - Either assign failure codes individually
    - Or use dropdown at top to apply same failure code to all parts
    - Complete remaining fields
    - Click Update
- System automatically generates NCR for every rejected part
- Return to Inspection screen to view/edit submitted reports

### How to add custom inspection types

- Admin Maintenance -> Data Maintenance
- Locate Inspection Type data type
- Click Add Record
- Enter description
- Click Submit
- Refresh inspection screen to see new type

## NCRs & CARs

### How to create NCRs

- Access NCR types table:
    - Method 1: Maintenance -> Data Maintenance -> search for "NCR" -> Submit -> NCR Type
    - Method 2: Production -> Quality -> NCR List -> click link to data maintenance in header
- Manage NCR types:
    - Delete existing types: check delete box -> Submit
    - Add new types: Add Record -> enter information -> Submit
- On NCR screen:
    - View associated documents
    - Add new documents
    - View/add notes
    - Track progress: click History
- When creating NCR (Creation workflow stage):
    - Set NCR type
    - Enter title
    - Specify part, quantity, and vendor
    - Attach images
    - Log additional details
    - Enter Containment actions (required)
    - Check critical box if issue is critical
    - Click Update to save
- NCR document options:
    - Download as ZIP/PDF
    - Print
    - Delete
- Configure workflow assignees:
    - Workflow Menu -> edit link
    - Scroll to relevant state
    - Select users (hold Control while clicking)
    - Assign roles
    - Click Submit -> refresh NCR screen
- Move NCR to Review stage:
    - Use Workflow menu (top right)
    - Select assignee
    - Click Send to Review
- In Review state:
    - Select Disposition
    - Enter Review Comments
    - Click Update
    - Advance to next stage (Escalation or MRB)

### How to create CARs

- Create CAR:
    - Method 1: Production -> Quality -> CAR List -> Create
    - Method 2: From existing NCR in MRB or Management state
- From NCR:
    - Scroll to CAR section
    - Choose CAR type
    - Click Update
- On CAR Edit screen:
    - Access Documents, Notes, History from left menu
    - Fill basic information: CAR Type, Source, Involved Parties
    - Click Update
- Add Root Cause Analysis (only in State 1/Creation):
    - Click Add Additional Issue
    - Fill in why issue happened
    - Click Update
    - Add Sub-Causes if needed: click link -> complete field -> Add
- Document Why the Issue Escaped:
    - Add Sub-Reasons if necessary
    - Select Root Cause from dropdown
    - Include comments
    - Click Add Root Cause
- Customize root cause options:
    - Click Edit to access CAR Root Cause Type table
- Manage NCR linkage:
    - View associated NCRs at bottom
    - Link more if needed -> Update
- Move CAR to Review State:
    - Select reviewer
    - Click To Review
- In Review State:
    - Evaluate report
    - Determine Corrective/Preventive Action
    - Scroll to Actions Taken section
    - Choose action type from dropdown
    - Assign to internal user, vendor, or customer
    - Select appropriate contact
    - Choose Action Date
    - Enter Description
    - Click Add Action
- Complete actions:
    - Add Completion Date
    - Click Update
- Customize Actions Taken view:
    - Check/uncheck boxes at top of section
- Remove an action:
    - Select Drop next to it
    - Click Update
- Move CAR to Validation state
## Inspection & Reporting
### How to run inspection Reports
- Production -> Quality -> Inspection failures -> filter -> submit & export

[[Cetec Guides - Scheduling]]