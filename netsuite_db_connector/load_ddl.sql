drop table if exists ns_load_vendor_bills;

create table ns_load_vendor_bills(
    "externalId" text primary key,
    "internalId" text,
    "currencyInternalId" text not null,
    "memo" text not null,
    "departmentInternalId" text,
    "classInternalId" text,
    "locationInternalId" text,
    "entityInternalId" text not null
);

drop table if exists ns_load_vendor_bill_expenses;

create table ns_load_vendor_bill_expenses(
    "vendorBillExternalId" text,
    "accountInternalId" text not null,
    "amount" numeric,
    "departmentInternalId" text,
    "classInternalId" text,
    "locationInternalId" text,
    "memo" text
);
