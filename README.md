# MBI-Export-API-Template

Official Magento BI Export API documentation here: https://devdocs.magento.com/mbi/docs/export-api.html

Before you can call data using the Export API, you must:

1. Set up an Export API key in MBI and whitelist the correct IP addresses.
2. Create a raw data export.

This script does the following:

1. Refresh the provided raw data export (this re-runs the raw data export with the same parameters to reflect updated data).
2. Download the newly refreshed raw data export as a CSV to an export directory. At this point, you can do something with the data.
3. Delete the downloaded zip file and CSV from the export directory.

**PLEASE NOTE:**

This app is not endorsed or supported by Adobe.

This repo is _not_ actively maintained, and no changes are anticipated.
