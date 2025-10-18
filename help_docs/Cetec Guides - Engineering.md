## Part maintenance
### How to create PRCS
- Parts -> Lists -> PRC Lists -> create prc
- Choose 3 letter prc -> create
- Set info -> update
### View Prcs
- Parts -> Lists -> Prc list -> submit
### How to create PRCparts
- Parts -> Lists -> Part Lists -> Create New
- Choose Prc & set part No & description
- Create
### How to edit parts
- From part -> edit - edit it -> update
### How to manage cross parts
- From part -> MAINT+ -> Crosses
- Enter vendors part no, part type, association -> update
### How to assign UOMs to PRCparts
- Parts -> Lists -> Part List -> Search for part -> submit
- Part Record -> Edit -> Select UOM -> Update.
- New UOMS can be added from ADMIN
### How to create non-inventory prc-parts
- Parts -> Lists -> Part List -> Create new
- Select PRC & part NO -> create
- Check non-inventory
## BOM Management
### How to create a BOM
- Parts -> Lists -> Part List -> Create New
- Select PRC & part no/ loc -> Select Bom? -> Create
- Enter info - update as many lines as needed
#### View BOM tree
- To Part Record -> BOM Overview
#### For revisions
- Revisions/labor plan/edit BOM
### How to create a multi level BOM
#### Sub Assembly
- Parts -> Lists -> Part List -> Create New
- Select PRC & part no/ loc -> Select Bom? -> Create
- Enter info - update as many lines as needed
#### Top Assembly
- Parts -> Lists -> Part List -> Create New
- Select PRC & part no/ loc -> Select Bom? -> Add revision >= 1 -> Create
- Add a component that is the sub assembly -> update
- Enter info - update as many lines as needed
- To Part Record -> Bom Data + -> Bom Overview
### How to attach documents to Revisions
- Global search for BOM -> Documents -> Browse 
- Choose to attach to a new revision -> upload
- Can move after the fact
### How to create a labor plan (Traveler)
- Search for part no.
- Revisions -> Labor Plan
- Set location -> Add
- Edit with pencil
- Add operation -> Set Overhead -> Set.
- Add work instructions
	- Pick reqd
- For label estimate use total labor estimate
### How to manage your production setup
- Admin - Config Settings -> config settings
- type work_start in name
	- set work_start_hour_MN - main warehouse
	- set work_start_hour
	- set work_end_hour etc 16 == 4pm
#### Setup work locations
- Admin -> Maintenance -> Data Maintenance
- Type ordline and search
- open ordlinestatus
#### Capacity calander
- Production -> Scheduling -> Set capacity
- Select day -> Edit -> Batch Update
- For range of dates use batch set capacity
## Revision Control
### How to manage BOM revisions (manual)
- Revisions -> Edit Revision Bom -> update or add
- To part record -> bom data + -> bom overview
#### Add new revision
- Create new rev with name
- Edit new rev bom, set if current
### How to manage BOM revisions (ECR)
- Production -> Orders -> ECO/ECR list
- Create ->  enter pcr parts no and type. -> create
- change revision from and to.
- can add rev from add rev

### CREATING AN ECO
- Navigate to PRODUCTION » ORDERS » ECO/ECR. Type in the part number for which you want to create the ECO, set the ECO type, and click Create.
## Order BOM
### How to create a Work Order
- Production -> Orders -> New Build for Stock or Hamburger -> work order entry/build to stock
- Enter part info -> commit order 
- After following steps
- Complete All
### How to edit Labor, material & revisions on a work order
- from order -> workorder view+ -> line
- Maint/Etc + -> BOM management
- Maint/Etc + -> Labor Plan management
	- Use replace order specific labor plan
- Maint/Etc + -> Change Rev
	- view or change revisions


[[Cetec Guides - Production]]

