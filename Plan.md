# Raspberry Pi Barcode Scanner

## Roles
Adam
- logic

Mark
- database 

Nathan
- getting data from barcodes 

## Questions
Which database will we use?
- SQL -Mark

Data input
- Adam, how do you want to get data? I can do an iterator, function call, etc. -Nate
- Looking at it, an interator would be best -Nate
- interator is fine with me - Adam

Input rules
- 6 long numeric strings will be sent to processing
- The database will take data formatted as (s#, time in, time out, forced timeout)

### Iterator input
This is how the barcode data will be gotten:
```py
from barcode_reader import BarcodeReader

reader = BarcodeReader()
for snumber in reader.watch_for_barcodes():
    # snumber will be a str like '433246'
    # Handle it however you wish
```
