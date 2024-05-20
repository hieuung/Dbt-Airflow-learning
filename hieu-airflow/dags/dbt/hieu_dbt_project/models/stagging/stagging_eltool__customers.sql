with source as (
    select *
    from {{ source('raw_layer', 'customers') }}
),

renamed as (
    select
        customer_id,
        postal_code,
        city,
        address,
        country,
        phone,
        contact_name,
        company_name
    from source
)

select *
from renamed