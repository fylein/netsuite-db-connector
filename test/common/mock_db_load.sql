delete from ns_load_vendor_bills;
delete from ns_load_vendor_bill_expenses;

insert into ns_load_vendor_bills("externalId", "currencyInternalId", "memo", "classInternalId", "locationInternalId", "entityInternalId")
values ('1237', '1', 'Courtesy db connector', '1', '1', '46');

insert into ns_load_vendor_bill_expenses("vendorBillExternalId", "accountInternalId", "amount", "departmentInternalId", "classInternalId", "locationInternalId", "memo")
values ('1237', '16', 10.0, '1', '1', '1', 'Expense no. 1');

insert into ns_load_vendor_bill_expenses("vendorBillExternalId", "accountInternalId", "amount", "departmentInternalId", "classInternalId", "locationInternalId", "memo")
values ('1237', '17', 20.0, '1', '2', '2', 'Expense no. 2');
