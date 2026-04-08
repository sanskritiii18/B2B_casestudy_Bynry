# B2B Case Study Solution

This repository contains my solution for the B2B Inventory Management Case Study. The solution is organized into separate folders corresponding to each part of the problem statement.

Each part includes the implementation code, while the detailed explanation of the approach, reasoning, and analysis is provided in the accompanying Word document.

The repository is structured to clearly separate the analysis, design, and implementation steps for each part of the case study.

## Repository Structure
.
├── part_1
│   └── main.py
│
├── part_2
│   ├── Tables.txt
│   └── schema.sql
│
├── part_3
│   └── main.py
│
└── README.md
##
# Part 1 – Code Analysis and Debugging

For Part 1, the workflow analysis, debugging approach, and explanation of the issues in the provided code are described in detail in the Word document.

The corrected and improved implementation can be found here:

part_1/main.py

This section discusses issues such as:

Input validation
Transaction safety
SKU uniqueness checks
Error handling
Separation of business logic from API routes
Rate limiting
Authentication and authorization


# Part 2 – Database Design

For Part 2, the database schema design is explained in the Word document.

The repository includes:

part_2/Tables.txt

This file describes the table structures.

part_2/schema.sql

This file contains the SQL DDL implementation of the database schema.

The schema supports:

Multiple companies
Multiple warehouses per company
Inventory tracking
Supplier-product relationships
Product bundles
Inventory history tracking


# Part 3 – API Implementation

For Part 3, the implementation of the low-stock alert endpoint is provided.

Endpoint:

GET /api/companies/{company_id}/alerts/low-stock

The implementation can be found here:

part_3/main.py

This endpoint:

Identifies products below their stock threshold
Considers recent sales activity
Supports multiple warehouses per company
Includes supplier information for reordering

The design assumptions and detailed reasoning for this implementation are described in the Word document.


# Additional Documentation

A Word document containing the full explanation of:

approach
workflow analysis
debugging reasoning
design decisions

has also been shared via Google Drive.

The same document has been provided in the submission email along with the GitHub repository link.
