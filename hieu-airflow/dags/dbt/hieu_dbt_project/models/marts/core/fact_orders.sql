with orders as (
    select *
    from {{ ref('stagging_eltool__orders') }}
)

select * from orders