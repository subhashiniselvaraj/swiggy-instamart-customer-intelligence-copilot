# Dataset and analytical choices

## Source
UCI Machine Learning Repository: Online Retail
https://archive.ics.uci.edu/dataset/352/online+retail

## Main fields
- `InvoiceNo`: transaction/invoice identifier; values beginning with `C` denote cancellations/credit notes.
- `StockCode`: product code.
- `Description`: product description.
- `Quantity`: quantity in the line item.
- `InvoiceDate`: invoice timestamp.
- `UnitPrice`: unit price.
- `CustomerID`: customer identifier; some records lack it.
- `Country`: customer country.
- `Sales`: derived as `Quantity * UnitPrice`.

## Cleaning choices
The primary customer/sales analysis removes duplicate rows, missing customer or transaction essentials, cancellation invoices, and non-positive quantities/prices. These choices are appropriate for a simple sales analysis but do not represent every possible accounting use. Document the impact using the generated summary.

## Supervised target
Part 2 predicts whether a customer seen in the pre-cutoff feature period also purchases during the final 90-day period. Features are aggregated strictly before the cutoff. Customers without pre-cutoff activity are not included in the feature table. This is a defined educational prediction task; its evaluation should not be interpreted as a production guarantee.

## Limitations
This dataset contains retail transaction records, not Instamart's internal data, support tickets, official refund policies, demographics, or ground-truth satisfaction labels. The LLM demo uses aggregate/synthetic summaries and must not be presented as a real refund agent.
