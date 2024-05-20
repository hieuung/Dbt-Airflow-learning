with customers as (
    select 
        *
    from 
        {{ ref('stagging_eltool__customers') }}
)
select
    c.customer_id,
    c.postal_code,
    c.city,
    c.address,
    c.country,
    c.phone,
    c.contact_name,
    c.company_name
from customers as c