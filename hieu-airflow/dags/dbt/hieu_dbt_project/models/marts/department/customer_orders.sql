with orders as (
    select *
    from {{ ref('fact_orders') }}
),

customers as (
    select *
    from {{ ref('dim_customers') }}
)

select
    o.*,
    c.postal_code,
    c.city,
    c.address,
    c.country,
    c.phone,
    c.contact_name,
    c.company_name
from orders as o
inner join customers as c on
    o.customer_id = c.customer_id