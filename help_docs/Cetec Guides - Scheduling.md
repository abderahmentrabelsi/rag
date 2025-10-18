## Stock vs Build Concepts

### Overview: Build-to-Stock vs. Sales Order

- Two order types in Cetec:
    - Build to Stock (internal orders)
    - End Customer Sales Orders (external orders)
- Create Build to Stock order:
    - Hamburger menu -> Work Order Entry -> Build to Stock
    - Choose internal customer (company is both vendor and customer)
    - Header identifies work order type
- Create End Customer Sales Order:
    - Hamburger menu -> Work Order Entry -> Custom
    - Select from full customer list
    - Enter external customer's PO number
- Build to Stock process:
    - When committed, creates both order and internal PO
    - Location code (e.g., "MN") at beginning of order number
    - Final step: Complete and Receive order
- End Customer Sales process:
    - Final step: Invoice Ship (found in left-side menu)

### How to Create a Build-to-Stock Order from MRP

- Navigate to: Purchasing -> MRP -> MRP Build
- Run MRP refresh by clicking refresh button
- Review shortages in MRP report
- Check part waterfalls for up-to-date supply/demand data:
    - Select "Waterfall Only" in Expand All Part Info field
    - Click Submit
- Create work orders:
    - Select all parts or specific parts
    - Click Build
    - Choose to create new work order or add to existing
    - Select internal account as vendor
    - Click Add Create Quote Order Worksheet

### How to Create a Custom Order

- Method 1:
    - Hamburger menu -> Work Order Entry -> Custom
    - Choose customer -> Go
    - Edit header info with pencil icon
    - Fill part information -> Add
    - Ensure transcode is "Build" (check for BOM worksheet icon)
- Method 2:
    - Sales -> Quotes -> New Quote
    - Edit header (add customer, PO number, ship-to address, shipping method)
    - Add part information
    - Ensure transcode is "Build"
    - Enter date information (doc date important for MRP)

## Multi-Level BOM Management

### BOM Overview

- Access BOM report: Parts -> Lists -> BOM List -> Submit
- BOM overview screen shows:
    - Tree view of BOM at top
    - Multi-level structure identification
    - Component navigation
- Labor plan access: Left-side menu -> Revisions
- BOM Labor Plan details:
    - Locations and operations
    - Time estimates (setup and recurring)
    - Labor rate and overhead rate
    - Cost calculations

### Create Work Orders with Subassemblies

- When committing quote to order:
    - Choose "Yes" to include subassemblies
    - System creates orders for top-level assembly and each subassembly
    - Creates internal POs alongside subassembly orders
- Navigation between orders:
    - Left-side menu links to suborders
    - Work Order View Plus -> Line 1 -> Parts tab shows subassembly line

### Create Work Orders without Subassemblies

- When committing quote to order:
    - Choose "No" to exclude subassemblies
    - System creates order only for top-level assembly
    - Subassembly appears as single line in Parts tab

### Create Work Orders with Phantom Assemblies

- When committing quote to order:
    - Choose "With Top" option
    - Creates single work order for top-level and subassemblies
    - Parts tab shows all components from all levels

### Subassembly Default Settings

- Configure in part record:
    - Part -> Maintenance Plus -> Build Defaults
- Options:
    - Skip Build: No subassembly order created
    - With Top: Combines with top-level order
    - Always Build: Creates separate related order
- Settings can be manually adjusted during order commitment

## Order Management & Material Overview

### How to Review Material Shortages

- Production -> Orders -> Order Material Report
- View shortages and availability details
- For more detail, click View
- Create orders from shortage reports:
    - Overview -> Create PO Quote
    - Overview -> Create WOE (work order)

### How to Manage Lead Times & ROP

- Access MRP report: Purchasing -> MRP -> MRP All
- Part details show:
    - Lead Time (e.g., 4 weeks)
    - Quantity on Hand (QOH)
    - Reorder Point (ROP)
    - Required Quantity calculation
- Configure ROP comparison:
    - Admin -> Config Settings -> Config Settings
    - Search for ROP_underscore_AGAINST
- Set part's ROP and Lead Time:
    - Go to part record
    - Scroll to warehouse section
    - Click Pencil icon to edit
    - Enter ROP and Lead Time values
    - Click Update

### How to Perform a Stock Check & What If Scenario

- Parts -> Part List -> Lists -> Part List
- Select assembly BOM
- BOM Data Plus -> BOM Overview
- Shows:
    - BOM tree structure
    - Quantity on Hand for each part
    - Quantity per top-level assembly
- Build Estimate: BOM Data Plus -> Build Estimate
    - Shows parts and subassemblies in inventory
    - Provides build estimates

## Scheduling

### How to Create a Labor Plan (Traveler)

- Locate BOM using global search
- Navigate: Part screen -> Revisions -> Labor Plan
- Add work location:
    - Select from dropdown
    - Click Add
- Add operation:
    - Click Pencil icon
    - Choose operation
    - Click Add
- Configure operation:
    - Set as setup step if applicable
    - Click Set to confirm
    - Add more operations as needed
- Add work instructions:
    - Check parts picking box if needed
    - Enable signature requirement if needed
    - Click Update to save
- Manage locations and operations:
    - Add new locations as needed
    - Set operation repetitions
    - Remove locations/operations as needed
- Time estimates include:
    - One-time setup time
    - Recurring time (multiplied by quantity)
- Set total labor estimate:
    - Enter value in minutes
    - Select Use Total Labor Estimate
    - Click Update

### How to Schedule Jobs (Forward and Backward)

- Create Build for Stock order:
    - Production -> Orders -> New Build for Stock
    - Enter part number and entity
    - Set ship date and completed date
    - Click Add
- Commit order:
    - Click Commit to Order
    - Click Commit Order
    - Work Start Date auto-calculates
- View schedule details:
    - Work Order View -> Gantt Chart
    - Click Schedule for time segment breakdown
- Adjust scheduling:
    - Change ship date or work start date manually
	    - Reschedule forward or backward as needed

[[Cetec Guides - AR]]