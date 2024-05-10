# Summary of Deposits

Summary of Deposits (SOD) lists every branch and the deposits booked at that
branch for FDIC insured institutions. See [12 CFR 304.3(c)](
https://www.ecfr.gov/current/title-12/part-304/section-304.3#p-304.3(c)). Each
institution reports on 30 June of each year.

SOD is widely used in economic research. Eg Bouwman and Malmendier _Am Econ Rev_
105 (2015) pp 321–25. It is also used in the preliminary screens for bank merger
competitive reviews. Department of Justice
_[Bank merger competitive review](https://www.justice.gov/sites/default/files/atr/legacy/2007/08/14/6472.pdf)_
(2005).

## Variables

The FDIC merges SOD with RIS (Research Information System), which contains
information from call reports. Many of these variables are not especially
important. This section covers only the most important variables.

The following variables identify the branch.

* `YEAR` is the reporting year
* `CERT` identifies the institution on its FDIC certificate number
* `BRNUM` is a serial count of the branch in that year; this is valid only
  within the same `CERT`-`YEAR`
* `UNINUMBR` is a supposedly consistent identifier assigned to a branch location
  which does not change even if the branch is sold
* `NAMEFULL` is the bank's name of the branch
* `ADRESSBR` is the branch address
* `CITYBR` is the branch city
* `STALPBR` is the branch state
* `ZIPBR` is the branch ZIP code

The following variables describe the branch.

* `DEPSUMBR` is the deposits the bank reports at that branch; **do not confuse
  this with `DEPDOM`, which is the bank's total deposits!**
* `STCNTYBR` is the FIPS code in which the branch is located
* `BRSERTYP` is the branch service type; the [2023 instructions](
  https://www.fdic.gov/resources/bankers/call-reports/summary-of-deposits/2023-sod-instructions.pdf)
  show the following service levels on pp 34–35 with a fuller explanation:

| `BRSERTYP` | Service         | Short description             | Included? |
|------------|-----------------|-------------------------------|-----------|
| 11         | Full service    | Brick and mortar office       | Deposits  |
| 12         | Full service    | Retail office                 | Deposits  |
| 13         | Full service    | Home banking                  | Deposits  |
| 22         | Limited service | Military facility             |           |
| 23         | Limited service | Drive‐through/facility office |           |
| 29         | Limited service | Mobile/seasonal office        |           |
| 21         | Limited service | Administrative office         |           |
| 30         | Limited service | Trust office                  |           |
| 24         | Limited service | Loan production office        | No        |
| 25         | Limited service | Consumer Credit office        | No        |
| 26         | Limited service | Contractual office            | No        |
| 27         | Limited service | Messenger office              | No        |
| 28         | Limited service | Retail office (ATM?)          | No        |

* `BKMO` identifies if the branch is the bank's main office

The FDIC has already geocoded many of these branches and provide two
variables: `SIMS_LATITUDE` and `SIMS_LONGITUDE`. The quality of that
geocode is not always entirely acceptable. Especially in earlier data,
coordinates are approximate: assigned to the centre of counties, states, or
sometimes to `0, 0`, [Null Island](https://www.youtube.com/watch?v=bjvIpI-1w84),
in the Atlantic off the African coast. There are also variables identifying
the `CSA` (Combined Statistical Area) and `MSA` (Metropolitan Statistical Area)
of the branch.

There is no known interlink between branches in SOD and branches in the Federal
Reserve's _National Information Center_.

## `DEPSUMBR`

There is no guarantee that `DEPSUMBR` is at all accurate. This implied in the
SOD instructions (2023 instructions, p 3): "Institutions should assign deposits
to each office in a manner consistent with their existing internal
record‐keeping practices". Banks need not book a customer's deposits at a branch
at all proximate to the customer's location provided it is consistent with their
own records.

Nor is it clear how certain classes of customers ought to be treated. Many
corporate and brokered deposits are booked at the main office or at virtual
branches (branches with no or little real world analogue) which are used mainly
to separate those corporate or brokered deposits from the main deposit
franchise. In 1995, for example, around 75 per cent of banks booked a majority
of deposits at their main office (`BKMO`).

Along with the expansion of online banking – noted at
[89 FR 6607](https://www.federalregister.gov/d/2023-25797/p-499) – which
removes the need for branches in deposit collection entirely, `DEPSUMBR`
accuracy may be in further decline.

# Author

Kevin Wong

The views expressed (if there is any such expression at all) herein do not
necessarily represent the views of the Federal Deposit Insurance Corporation,
Office of the Comptroller of the Currency, the Department of the Treasury, or
the United States.