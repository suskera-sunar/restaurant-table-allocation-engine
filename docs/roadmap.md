Phase 1: Database Setup  
        • Define models in models.py: Table, TimeSlot, Reservation


        • Configure foreign keys (TimeSlot & Table FKs on Reservation)


        • Register models in Django Admin and seed data (~8 tables, fixed slots)

Phase 2: Core Algorithm
        • Write ai/search.py implementing the greedy best-first function


        • Filter tables by requested TimeSlot and capacity >= party_size


        • Implement heuristic scoring: $h(\text{table}) = \text{capacity} - \text{party\_size}$


        • Return candidate with minimum $h$ (or reject if no candidates exist)


Phase 3: Web Views & Flow
        • Create Guest reservation form (party size, slot, contact details)


        • Connect form submission directly to the greedy allocator


        • Build confirmation page and explicit "Allocation Rejected" error  view

Phase 4: Staff Dashboard
        • Implement Staff login/authentication view


        • Build allocation board filtered per time slot


        • Add actions to mark no-shows and free tables for new requests

Phase 5: Testing & Viva Prep
        • Seed an evening with 12 reservations to prove edge cases
        

        • Intentionally trigger rejection to verify capacity filtering
        

        • Document failure modes and defense strategy for greedy vs $A^*$