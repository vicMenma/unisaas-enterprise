
# Matricule System (Production)

## Format
PREFIX-PROGRAM-LEVEL-SEQ

## Example
CU-BEE-100-0001

## Rules
- Unique per tenant
- Generated atomically
- Uses SELECT FOR UPDATE

## Storage
matricule_sequences table

## Failure Handling
- rollback transaction
- retry safe
