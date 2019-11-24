drop table if exists ns_load_vendor_bills;

create table ns_load_vendor_bills(
    "externalId" text primary key,
    "currencyInternalId" text,
    "memo" text not null,
    "classInternalId" text,
    "locationInternalId" text,
    "entityInternalId" text not null
);

drop table if exists ns_load_vendor_bills_expenses;

create table ns_load_vendor_bills_expenses(
    "vendorBillExternalId" text,
    "accountInternalId" text not null,
    "amount" numeric,
    "departmentInternalId" text,
    "classInternalId" text,
    "locationInternalId" text,
    "memo" text
);
