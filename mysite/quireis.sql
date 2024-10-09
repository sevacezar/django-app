SELECT
    "shopapp_product"."id",
    "shopapp_product"."name",
    "shopapp_product"."description",
    "shopapp_product"."price",
    "shopapp_product"."discount",
    "shopapp_product"."created_at",
    "shopapp_product"."archived",
    "shopapp_product"."created_by_id",
    "shopapp_product"."preview"
FROM
    "shopapp_product"
WHERE
    NOT "shopapp_product"."archived"
ORDER BY
    "shopapp_product"."name" ASC;


SELECT
    "shopapp_product"."id",
    "shopapp_product"."name",
    "shopapp_product"."description",
    "shopapp_product"."price",
    "shopapp_product"."discount",
    "shopapp_product"."created_at",
    "shopapp_product"."archived",
    "shopapp_product"."created_by_id",
    "shopapp_product"."preview"
FROM
    "shopapp_product"
WHERE
    "shopapp_product"."id" = 3
LIMIT
    21;


SELECT
    "shopapp_productimage"."id",
    "shopapp_productimage"."product_id",
    "shopapp_productimage"."image",
    "shopapp_productimage"."descriprion"
FROM
    "shopapp_productimage"
WHERE
    "shopapp_productimage"."product_id" IN (3);









SELECT
    "shopapp_order"."id",
    "shopapp_order"."delivary_address",
    "shopapp_order"."promocode",
    "shopapp_order"."created_at",
    "shopapp_order"."user_id",
    "shopapp_order"."receipt",
    (CAST(SUM("shopapp_product"."price") AS NUMERIC)) AS "total",
    COUNT("shopapp_order_products"."product_id") AS "products_count"
FROM
    "shopapp_order"
    LEFT OUTER JOIN "shopapp_order_products" ON (
        "shopapp_order"."id" = "shopapp_order_products"."order_id"
    )
    LEFT OUTER JOIN "shopapp_product" ON (
        "shopapp_order_products"."product_id" = "shopapp_product"."id"
    )
GROUP BY
    "shopapp_order"."id",
    "shopapp_order"."delivary_address",
    "shopapp_order"."promocode",
    "shopapp_order"."created_at",
    "shopapp_order"."user_id",
    "shopapp_order"."receipt";

args =();

alias = default








SELECT
    "django_session"."session_key",
    "django_session"."session_data",
    "django_session"."expire_date"
FROM
    "django_session"
WHERE
    (
        "django_session"."expire_date" > '2024-10-03 09:02:40.236478'
        AND "django_session"."session_key" = '2l8bscmm54whw5ul9i234g9avw7he1my'
    )
LIMIT
    21;

SELECT
    "auth_user"."id",
    "auth_user"."password",
    "auth_user"."last_login",
    "auth_user"."is_superuser",
    "auth_user"."username",
    "auth_user"."first_name",
    "auth_user"."last_name",
    "auth_user"."email",
    "auth_user"."is_staff",
    "auth_user"."is_active",
    "auth_user"."date_joined"
FROM
    "auth_user"
WHERE
    "auth_user"."id" = 1
LIMIT
    21;

SELECT
    "shopapp_order"."id",
    "shopapp_order"."delivary_address",
    "shopapp_order"."promocode",
    "shopapp_order"."created_at",
    "shopapp_order"."user_id",
    "shopapp_order"."receipt",
    "auth_user"."id",
    "auth_user"."password",
    "auth_user"."last_login",
    "auth_user"."is_superuser",
    "auth_user"."username",
    "auth_user"."first_name",
    "auth_user"."last_name",
    "auth_user"."email",
    "auth_user"."is_staff",
    "auth_user"."is_active",
    "auth_user"."date_joined"
FROM
    "shopapp_order"
    INNER JOIN "auth_user" ON ("shopapp_order"."user_id" = "auth_user"."id");

SELECT
    ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id",
    "shopapp_product"."id",
    "shopapp_product"."name",
    "shopapp_product"."description",
    "shopapp_product"."price",
    "shopapp_product"."discount",
    "shopapp_product"."created_at",
    "shopapp_product"."archived",
    "shopapp_product"."created_by_id",
    "shopapp_product"."preview"
FROM
    "shopapp_product"
    INNER JOIN "shopapp_order_products" ON (
        "shopapp_product"."id" = "shopapp_order_products"."product_id"
    )
WHERE
    "shopapp_order_products"."order_id" IN (1, 2, 3, 4)
ORDER BY
    "shopapp_product"."name" ASC;






SELECT
    "shopapp_order"."id",
    "shopapp_order"."delivary_address",
    "shopapp_order"."promocode",
    "shopapp_order"."created_at",
    "shopapp_order"."user_id",
    "shopapp_order"."receipt",
    (
        CAST(
            COALESCE(
                (CAST(SUM("shopapp_product"."price") AS NUMERIC)),
                (CAST('0' AS NUMERIC))
            ) AS NUMERIC
        )
    ) AS "total",
    COUNT("shopapp_order_products"."product_id") AS "products_count"
FROM
    "shopapp_order"
    LEFT OUTER JOIN "shopapp_order_products" ON (
        "shopapp_order"."id" = "shopapp_order_products"."order_id"
    )
    LEFT OUTER JOIN "shopapp_product" ON (
        "shopapp_order_products"."product_id" = "shopapp_product"."id"
    )
GROUP BY
    "shopapp_order"."id",
    "shopapp_order"."delivary_address",
    "shopapp_order"."promocode",
    "shopapp_order"."created_at",
    "shopapp_order"."user_id",
    "shopapp_order"."receipt";