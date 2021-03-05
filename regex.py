import re
ssnlist = ['123456789','12345678','123-45-6789']
#ssn format: xxxxxxxxx or xxx-xx-xxxx
print('ssn validation: ')
for i in ssnlist:
    print(bool(re.match(r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$', i)))
#credit card number
#Amex: 15 digits, format: 3(4 or 7)xx xxxxxx xxxxx
    amex = '^3[47][0-9]{13}$'
#Visa: 13 or 16 digits, begin with 4
    visa = '^4[0-9]{12}(?:[0-9]{3})?$'
#Mastercard: begins with 5, 16 digits
    mastercard = '^(5[1-5][0-9]{14}|2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12}))$'
creditcardlist = ['344678542165211','4654524875945111','5123456789123456']
print('Credit card validation: ')
for k in creditcardlist:
    print(bool(re.match(amex, k))) #amex True-False-False
for k in creditcardlist:
    print(bool(re.match(visa, k)))#visa False-True-False
for k in creditcardlist:
    print(bool(re.match(mastercard, k))) #master card False-False-True
