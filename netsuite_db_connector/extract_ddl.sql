drop table if exists ns_extract_currencies;

create table ns_extract_currencies(
    "internalId" text primary key,
    "symbol" text,
    "isBaseCurrency" boolean,
    "exchangeRate" numeric
);

drop table if exists ns_extract_accounts;

create table ns_extract_accounts(
    "internalId" text primary key,
    "acctType" text,
    "acctNumber" int,
    "acctName" text
);

drop table if exists ns_extract_departments;

create table ns_extract_departments(
    "internalId" text primary key,
    "name" text
);

drop table if exists ns_extract_locations;

create table ns_extract_locations(
    "internalId" text primary key,
    "name" text
);

drop table if exists ns_extract_vendors;

create table ns_extract_vendors(
    "internalId" text primary key,
    "entityId" text
);

drop table if exists ns_extract_classifications;

-- Might want to add parent class as well if there is ambiguity
create table ns_extract_classifications(
    "internalId" text primary key,
    "name" text
);