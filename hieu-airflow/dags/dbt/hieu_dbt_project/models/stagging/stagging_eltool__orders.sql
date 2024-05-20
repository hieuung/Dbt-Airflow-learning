with source as (
    select *
    from {{ source('raw_layer', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        employee_id,
        order_date,
        required_date,
        ship_city,
        ship_address,
        ship_region,
        ship_via,
        ship_country,
        ship_postal_code,
        ship_name,
        freight
    from source
)

select *
from renamed