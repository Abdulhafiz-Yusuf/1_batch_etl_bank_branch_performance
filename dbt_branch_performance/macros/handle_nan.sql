{% macro handle_nan(column_name, default_value=0) %}
    COALESCE(
        NULLIF({{ column_name }}::text, 'NaN')::numeric,
        {{ default_value }}
    )
{% endmacro %}