# Endpoint reference

All 203 endpoints of the DataPorium Data API, grouped by category. Each one is a method on the client with the name shown, for example `dp.company_info(symbol="AAPL")`.

This page is generated from the public OpenAPI file at <https://dataporium.tech/openapi.json>. For parameter details and example answers see the [API documentation](https://dataporium.tech/api-docs), or run `dp.describe("<method name>")` in Python.

## Categories

- [Stock Directory](#stock-directory) (1)
- [Company Information](#company-information) (10)
- [Quote](#quote) (2)
- [News](#news) (2)
- [Stock Performance](#stock-performance) (5)
- [Financial Statements](#financial-statements) (6)
- [Earnings & Events](#earnings--events) (4)
- [Shareholder Data](#shareholder-data) (5)
- [Insider Trades](#insider-trades) (3)
- [US Elections](#us-elections) (9)
- [Politician Trades](#politician-trades) (11)
- [Government Contracts](#government-contracts) (2)
- [Lobbying](#lobbying) (2)
- [Patents](#patents) (2)
- [Trademarks](#trademarks) (3)
- [Private Fundraising](#private-fundraising) (2)
- [Short Interest](#short-interest) (8)
- [Drug Approvals](#drug-approvals) (5)
- [Healthcare Providers](#healthcare-providers) (35)
- [Options Data](#options-data) (1)
- [Market Hours](#market-hours) (2)
- [Economics](#economics) (8)
- [Industry Metrics](#industry-metrics) (3)
- [Forex](#forex) (1)
- [Commodity](#commodity) (2)
- [Futures Positioning](#futures-positioning) (3)
- [Agriculture](#agriculture) (3)
- [Gas Prices](#gas-prices) (3)
- [Electricity Rates & Grid Prices](#electricity-rates--grid-prices) (7)
- [Local Economy](#local-economy) (4)
- [Layoffs](#layoffs) (9)
- [Colleges](#colleges) (3)
- [Industries](#industries) (2)
- [Banks](#banks) (4)
- [Consumer Complaints](#consumer-complaints) (3)
- [Recalls](#recalls) (4)
- [Transportation](#transportation) (5)
- [Facility Compliance & Emissions](#facility-compliance--emissions) (3)
- [Employer Salaries](#employer-salaries) (4)
- [Mortgage Lending](#mortgage-lending) (3)
- [Real Estate](#real-estate) (7)
- [Flood Claims & Disasters](#flood-claims--disasters) (2)

## Stock Directory

| Method | Path | What it returns |
|---|---|---|
| `symbols_list` | `/symbols-list` | Symbols by Exchange |

## Company Information

| Method | Path | What it returns |
|---|---|---|
| `company_info` | `/company-info` | Company Info |
| `business_segments` | `/business-segments` | Business Segments |
| `business_segments_quarterly` | `/business-segments/quarterly` | Business Segments (Quarterly) |
| `business_segments_views` | `/business-segments/views` | Business Segment Views |
| `business_segments_detail` | `/business-segments/detail` | Business Segment Details |
| `logo` | `/logo` | Company Logo |
| `ma_transactions_summary` | `/ma-transactions-summary` | Mergers & Investments |
| `sec_filings` | `/sec-filings` | SEC Filings |
| `presentations` | `/presentations` | Presentations |
| `industry` | `/industry` | Industry Classification |

## Quote

| Method | Path | What it returns |
|---|---|---|
| `stock_price_1d` | `/stock-price-1d` | Stock Price (1-Day) |
| `stock_price_5m` | `/stock-price-5m` | Stock Price (5-Minute) |

## News

| Method | Path | What it returns |
|---|---|---|
| `stock_news` | `/stock-news` | Stock News |
| `press_release` | `/press-release` | Press Releases |

## Stock Performance

| Method | Path | What it returns |
|---|---|---|
| `gain_loss` | `/gain-loss` | Stock Performance |
| `industry_performance` | `/industry-performance` | Industry Performance |
| `industry_performance_pe` | `/industry-performance-pe` | Industry P/E |
| `sector_performance` | `/sector-performance` | Sector Performance |
| `sector_performance_pe` | `/sector-performance-pe` | Sector P/E |

## Financial Statements

| Method | Path | What it returns |
|---|---|---|
| `income_statements` | `/income-statements` | Income Statement |
| `income_statements_summary` | `/income-statements-summary` | Income Summary |
| `balance_sheet_statements` | `/balance-sheet-statements` | Balance Sheet |
| `balance_sheet_statements_summary` | `/balance-sheet-statements-summary` | Balance Sheet Summary |
| `cash_flow_statements` | `/cash-flow-statements` | Cash Flow |
| `cash_flow_statements_summary` | `/cash-flow-statements-summary` | Cash Flow Summary |

## Earnings & Events

| Method | Path | What it returns |
|---|---|---|
| `earnings_transcripts` | `/earnings-transcripts` | Earnings Transcripts |
| `earnings_split_calendar` | `/earnings-split-calendar` | Earnings & Split Calendar |
| `ipo_calendar` | `/ipo-calendar` | IPO Calendar |
| `market_calendar` | `/market-calendar` | Market Calendar |

## Shareholder Data

| Method | Path | What it returns |
|---|---|---|
| `shareholders_by_type` | `/shareholders-by-type` | Shareholders by Type |
| `shareholders_geo` | `/shareholders-geo` | Geographic Shareholders |
| `shareholders_class` | `/shareholders-class` | Shareholders Class |
| `shareholders_quarterly` | `/shareholders-quarterly` | Quarterly Shareholders |
| `shareholders_quarterly_summary` | `/shareholders-quarterly-summary` | Quarterly Shareholders Summary |

## Insider Trades

| Method | Path | What it returns |
|---|---|---|
| `insider_transactions` | `/insider-transactions` | Insider List |
| `insider_holdings_summary` | `/insider-holdings-summary` | Insider Summary |
| `insider_transaction_history` | `/insider-transaction-history` | Insider Transactions |

## US Elections

| Method | Path | What it returns |
|---|---|---|
| `elections_races` | `/elections/races` | Election Races |
| `elections_results` | `/elections/results` | Election Results by Area |
| `elections_candidates` | `/elections/candidates` | Election Candidates |
| `elections_geography_level_code` | `/elections/geography/{level}/{code}` | Election Area Profile |
| `elections_area` | `/elections/area` | Election Area Summary |
| `elections_summary` | `/elections/summary` | Election Analysis |
| `elections_turnout` | `/elections/turnout` | Election Turnout |
| `elections_live_races` | `/elections/live/races` | Election Night Races |
| `elections_live_summary` | `/elections/live/summary` | Election Night Summary |

## Politician Trades

| Method | Path | What it returns |
|---|---|---|
| `politician_trades` | `/politician-trades` | Politician Trades |
| `politician_trades_summary` | `/politician-trades/summary` | Politician Trades Summary |
| `politician_trades_members` | `/politician-trades/members` | Politician Trades Members |
| `politician_trades_symbols` | `/politician-trades/symbols` | Politician Trades Symbols |
| `politician_trades_member_search` | `/politician-trades/member-search` | Politician Member Search |
| `politician_trades_net_worth` | `/politician-trades/net-worth` | Politician Net Worth |
| `politician_trades_net_worth_summary` | `/politician-trades/net-worth/summary` | Politician Net Worth Summary |
| `politician_trades_assets` | `/politician-trades/assets` | Politician Assets |
| `politician_trades_interests` | `/politician-trades/interests` | Politician Interests (Germany and Netherlands) |
| `politician_trades_interests_summary` | `/politician-trades/interests/summary` | Politician Interests Summary (Germany and Netherlands) |
| `politician_trades_holdings` | `/politician-trades/holdings` | Politician Holdings (Germany) |

## Government Contracts

| Method | Path | What it returns |
|---|---|---|
| `government_contracts` | `/government-contracts` | Government Contracts |
| `government_contracts_summary` | `/government-contracts/summary` | Government Contracts Summary |

## Lobbying

| Method | Path | What it returns |
|---|---|---|
| `lobbying` | `/lobbying` | Lobbying Reports |
| `lobbying_summary` | `/lobbying/summary` | Lobbying Summary |

## Patents

| Method | Path | What it returns |
|---|---|---|
| `patents` | `/patents` | Patents |
| `patents_summary` | `/patents/summary` | Patents Summary |

## Trademarks

| Method | Path | What it returns |
|---|---|---|
| `trademarks_filings` | `/trademarks/filings` | Trademark Filings |
| `trademarks_rankings` | `/trademarks/rankings` | Trademark Rankings |
| `trademarks_owners` | `/trademarks/owners` | Trademark Owners |

## Private Fundraising

| Method | Path | What it returns |
|---|---|---|
| `private_fundraising` | `/private-fundraising` | Private Fundraising |
| `private_fundraising_totals` | `/private-fundraising/totals` | Private Fundraising Totals |

## Short Interest

| Method | Path | What it returns |
|---|---|---|
| `short_interest` | `/short-interest` | Short Interest |
| `short_interest_ranking` | `/short-interest/ranking` | Most Shorted Stocks |
| `short_interest_summary` | `/short-interest/summary` | Short Interest Summary |
| `short_interest_dates` | `/short-interest/dates` | Short Interest Dates |
| `short_interest_filters` | `/short-interest/filters` | Short Interest Filters |
| `fails_to_deliver` | `/fails-to-deliver` | Fails to Deliver |
| `fails_to_deliver_ranking` | `/fails-to-deliver/ranking` | Fails to Deliver Ranking |
| `fails_to_deliver_periods` | `/fails-to-deliver/periods` | Fails to Deliver Periods |

## Drug Approvals

| Method | Path | What it returns |
|---|---|---|
| `drug_approvals` | `/drug-approvals` | Drug Approvals |
| `drug_approvals_summary` | `/drug-approvals/summary` | Drug Approvals Summary |
| `drug_approvals_companies` | `/drug-approvals/companies` | Drug Approvals by Company |
| `drug_approvals_countries` | `/drug-approvals/countries` | Drug Approval Countries |
| `drug_approvals_detail` | `/drug-approvals/detail` | Drug Approval Detail |

## Healthcare Providers

| Method | Path | What it returns |
|---|---|---|
| `healthcare_hospitals` | `/healthcare/hospitals` | Hospitals |
| `healthcare_hospitals_ccn` | `/healthcare/hospitals/{ccn}` | Hospital Detail |
| `healthcare_hospitals_summary` | `/healthcare/hospitals/summary` | Hospital Summary |
| `healthcare_health_systems` | `/healthcare/health-systems` | Health Systems |
| `healthcare_health_systems_system_id` | `/healthcare/health-systems/{system_id}` | Health System Detail |
| `healthcare_hospital_financials` | `/healthcare/hospital-financials` | Hospital Financials |
| `healthcare_hospital_quality` | `/healthcare/hospital-quality` | Hospital Quality |
| `healthcare_providers` | `/healthcare/providers` | Providers (NPI) |
| `healthcare_providers_npi` | `/healthcare/providers/{npi}` | Provider Detail |
| `healthcare_providers_summary` | `/healthcare/providers/summary` | Provider Counts |
| `healthcare_specialties` | `/healthcare/specialties` | Specialties |
| `healthcare_groups` | `/healthcare/groups` | Group Practices |
| `healthcare_procedures` | `/healthcare/procedures` | Medicare Procedures |
| `healthcare_procedures_codes` | `/healthcare/procedures/codes` | Procedure Codes |
| `healthcare_procedures_providers` | `/healthcare/procedures/providers` | Procedure Providers and Summary |
| `healthcare_lab_tests` | `/healthcare/lab-tests` | Lab Tests |
| `healthcare_hospital_procedures` | `/healthcare/hospital-procedures` | Hospital Stays and Outpatient Services |
| `healthcare_prescriptions` | `/healthcare/prescriptions` | Medicare Prescriptions |
| `healthcare_prescriptions_drugs` | `/healthcare/prescriptions/drugs` | Medicare Drugs |
| `healthcare_drug_spending` | `/healthcare/drug-spending` | Drug Spending |
| `healthcare_medicaid_drugs` | `/healthcare/medicaid-drugs` | Medicaid Drugs |
| `healthcare_payments` | `/healthcare/payments` | Payments to Doctors and Hospitals |
| `healthcare_payments_companies` | `/healthcare/payments/companies` | Paying Companies, Recipients and Summary |
| `healthcare_companies_ticker` | `/healthcare/companies/{ticker}` | Listed Company Medicare Summary |
| `healthcare_labs` | `/healthcare/labs` | Certified Labs |
| `healthcare_labs_summary` | `/healthcare/labs/summary` | Lab Counts and Lab Companies |
| `healthcare_lab_tests_segments` | `/healthcare/lab-tests/segments` | Medicare Lab Tests by Segment and Category |
| `healthcare_device_procedures` | `/healthcare/device-procedures` | Device Procedures |
| `healthcare_device_procedures_hospitals` | `/healthcare/device-procedures/hospitals` | Device Hospital Stays and Outpatient Services |
| `healthcare_device_procedures_icd` | `/healthcare/device-procedures/icd` | California Inpatient Procedures by ICD-10-PCS Code |
| `healthcare_medical_equipment` | `/healthcare/medical-equipment` | Medical Equipment and Supplies |
| `healthcare_devices_approvals` | `/healthcare/devices/approvals` | Device Approvals |
| `healthcare_devices_recalls` | `/healthcare/devices/recalls` | Device Recalls and Adverse Events |
| `healthcare_devices_companies` | `/healthcare/devices/companies` | Device Makers |
| `healthcare_drugs_adverse_events_drug` | `/healthcare/drugs/adverse-events/{drug}` | Drug Side-Effect Reports |

## Options Data

| Method | Path | What it returns |
|---|---|---|
| `options_callsputs` | `/options-callsputs` | Options Calls & Puts |

## Market Hours

| Method | Path | What it returns |
|---|---|---|
| `exchange_holiday` | `/exchange-holiday` | Exchange Holidays |
| `exchange_hours` | `/exchange-hours` | Exchange Hours |

## Economics

| Method | Path | What it returns |
|---|---|---|
| `economic_metrics` | `/economic-metrics` | Economic Metrics |
| `treasury_yields` | `/treasury-yields` | Treasury Yields |
| `treasury_yields_curve` | `/treasury-yields/curve` | Yield Curve |
| `fed_decisions` | `/fed-decisions` | Fed Rate Decisions |
| `inflation_categories` | `/inflation-categories` | Inflation by Category |
| `corporate_bond_yields` | `/corporate-bond-yields` | Corporate Bond Yields |
| `us_trade` | `/us-trade` | US Trade |
| `us_trade_summary` | `/us-trade/summary` | US Trade Summary |

## Industry Metrics

| Method | Path | What it returns |
|---|---|---|
| `industry_metrics` | `/industry-metrics` | Industry Metrics Over Time |
| `industry_metrics_series` | `/industry-metrics/series` | Industry Metric Series |
| `industry_metrics_latest` | `/industry-metrics/latest` | Industry Rankings (Latest Period) |

## Forex

| Method | Path | What it returns |
|---|---|---|
| `fx` | `/fx` | FX Conversion |

## Commodity

| Method | Path | What it returns |
|---|---|---|
| `commodity_price_1d` | `/commodity-price-1d` | Commodity Price (1-Day) |
| `commodity_price_5m` | `/commodity-price-5m` | Commodity Price (5-Minute) |

## Futures Positioning

| Method | Path | What it returns |
|---|---|---|
| `futures_positioning` | `/futures-positioning` | Futures Positioning History |
| `futures_positioning_markets_market` | `/futures-positioning/markets/{market}` | Futures Market Positioning (Latest Week) |
| `futures_positioning_latest` | `/futures-positioning/latest` | Most Net Long and Net Short Futures |

## Agriculture

| Method | Path | What it returns |
|---|---|---|
| `agriculture_commodities` | `/agriculture/commodities` | Agriculture Commodities |
| `agriculture_stats` | `/agriculture/stats` | Agriculture Statistics |
| `agriculture_prices` | `/agriculture/prices` | Agriculture Prices |

## Gas Prices

| Method | Path | What it returns |
|---|---|---|
| `gas_prices` | `/gas-prices` | Gas Prices |
| `gas_prices_local` | `/gas-prices/local` | Daily Local Gas Prices |
| `gas_prices_local_nearest` | `/gas-prices/local/nearest` | Nearest Local Gas Price |

## Electricity Rates & Grid Prices

| Method | Path | What it returns |
|---|---|---|
| `electricity_rates` | `/electricity-rates` | Electricity Rates by Utility |
| `electricity_rates_states` | `/electricity-rates/states` | Electricity Rates by State |
| `electricity_rates_utilities_utility_id` | `/electricity-rates/utilities/{utility_id}` | One Utility |
| `electricity_rates_county_county_fips` | `/electricity-rates/county/{county_fips}` | Electricity Prices of a County |
| `grid_prices_locations` | `/grid-prices/locations` | Grid Price Locations |
| `grid_prices` | `/grid-prices` | Grid Prices |
| `grid_prices_latest` | `/grid-prices/latest` | Latest Grid Prices |

## Local Economy

| Method | Path | What it returns |
|---|---|---|
| `local_jobs` | `/local-jobs` | Local Jobs (Unemployment) |
| `local_wages` | `/local-wages` | Local Wages (Jobs and Pay) |
| `building_permits` | `/building-permits` | Building Permits |
| `migration` | `/migration` | Migration (Moves In and Out) |

## Layoffs

| Method | Path | What it returns |
|---|---|---|
| `layoffs_events` | `/layoffs/events` | Layoff Events |
| `layoffs_summary` | `/layoffs/summary` | Layoffs Summary |
| `layoffs_companies` | `/layoffs/companies` | Companies by Layoffs |
| `layoffs_company_ticker` | `/layoffs/company/{ticker}` | Company Layoffs |
| `layoffs_state_state` | `/layoffs/state/{state}` | State Layoffs |
| `layoffs_industry_naics` | `/layoffs/industry/{naics}` | Industry Layoffs |
| `layoffs_overview` | `/layoffs/overview` | Layoffs Overview |
| `layoffs_official_jolts` | `/layoffs/official/jolts` | Official Layoffs (JOLTS) |
| `layoffs_official_claims` | `/layoffs/official/claims` | Unemployment Claims |

## Colleges

| Method | Path | What it returns |
|---|---|---|
| `colleges` | `/colleges` | Colleges |
| `colleges_summary` | `/colleges/summary` | College Summary |
| `colleges_programs` | `/colleges/programs` | College Programs and Majors |

## Industries

| Method | Path | What it returns |
|---|---|---|
| `industries` | `/industries` | Industry List |
| `industry_area_stats` | `/industry-area-stats` | Businesses, Employees and Payroll by Industry |

## Banks

| Method | Path | What it returns |
|---|---|---|
| `banks` | `/banks` | Banks and Credit Unions |
| `banks_screener` | `/banks/screener` | Bank Screener |
| `bank_branches` | `/bank-branches` | Bank Branches and Deposits |
| `bank_failures` | `/bank-failures` | Bank Failures |

## Consumer Complaints

| Method | Path | What it returns |
|---|---|---|
| `consumer_complaints_totals` | `/consumer-complaints/totals` | Complaints Over Time |
| `consumer_complaints_breakdown` | `/consumer-complaints/breakdown` | Complaints Breakdown |
| `consumer_complaints_companies` | `/consumer-complaints/companies` | Complaint Companies |

## Recalls

| Method | Path | What it returns |
|---|---|---|
| `recalls` | `/recalls` | Recalls |
| `recalls_totals` | `/recalls/totals` | Recall Totals |
| `vehicle_ratings` | `/vehicle-ratings` | Vehicle Safety Ratings |
| `vehicle_complaints` | `/vehicle-complaints` | Vehicle Owner Complaints |

## Transportation

| Method | Path | What it returns |
|---|---|---|
| `airlines` | `/airlines` | Airlines |
| `airports` | `/airports` | Airports and Air Routes |
| `trucking_carriers` | `/trucking/carriers` | Trucking Carriers |
| `trucking_stats` | `/trucking/stats` | Trucking by State and Month |
| `port_volumes` | `/port-volumes` | Port Container Volumes |

## Facility Compliance & Emissions

| Method | Path | What it returns |
|---|---|---|
| `compliance_facilities` | `/compliance/facilities` | Facilities |
| `compliance_companies` | `/compliance/companies` | Listed Companies |
| `emissions` | `/emissions` | Greenhouse Gas Emissions |

## Employer Salaries

| Method | Path | What it returns |
|---|---|---|
| `employer_salaries_totals` | `/employer-salaries/totals` | Salary Totals |
| `employer_salaries_employers` | `/employer-salaries/employers` | Employers |
| `employer_salaries_jobs` | `/employer-salaries/jobs` | Job Groups |
| `employer_salaries_areas` | `/employer-salaries/areas` | Areas |

## Mortgage Lending

| Method | Path | What it returns |
|---|---|---|
| `mortgage_lending_summary` | `/mortgage-lending/summary` | Mortgage Lending Summary |
| `mortgage_lending_areas` | `/mortgage-lending/areas` | Mortgage Lending by Area |
| `mortgage_lending_lenders` | `/mortgage-lending/lenders` | Mortgage Lenders |

## Real Estate

| Method | Path | What it returns |
|---|---|---|
| `properties` | `/properties` | Properties (Search and Detail) |
| `realestate_price_changes` | `/realestate-price-changes` | Price Changes and Relists |
| `realestate_for_sale` | `/realestate-for-sale` | Properties For Sale |
| `realestate_sold` | `/realestate-sold` | Properties Sold |
| `realestate_pending` | `/realestate-pending` | Pending Sales |
| `realestate_rent` | `/realestate-rent` | Rental Properties |
| `property_tax` | `/property-tax` | Property Tax |

## Flood Claims & Disasters

| Method | Path | What it returns |
|---|---|---|
| `flood_insurance` | `/flood-insurance` | Flood Insurance Claims |
| `disasters` | `/disasters` | Declared Disasters |
