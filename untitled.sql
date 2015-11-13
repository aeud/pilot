SELECT
    a.date Date,
    a.country Country,
    sum(b.gross) Gross_Revenue_Cumul
FROM ( 
    SELECT
        timestamp(date(o.createdAt)) date,
        case
          when o.address.country = 'Singapore' then o.address.country
          when o.address.country = 'Malaysia' then o.address.country
          when o.address.country = 'Australia' then o.address.country
          when o.address.country = 'India' then o.address.country
          when o.address.country = 'Indonesia' then o.address.country
          when o.address.country = 'Thailand' then o.address.country
          else 'Others'
        end country,
        round(sum(o.totals.grossRevenue)) gross
    FROM
        [dwh.orders] o
    WHERE
        o.isValid AND date(o.createdAt) >= DATE(STRFTIME_UTC_USEC(CURRENT_DATE(), '%Y-%m-01')) AND date(o.createdAt) < date(CURRENT_DATE())
    GROUP BY
        date, country
) a LEFT JOIN (
  SELECT
      timestamp(date(o.createdAt)) date,
      case
        when o.address.country = 'Singapore' then o.address.country
        when o.address.country = 'Malaysia' then o.address.country
        when o.address.country = 'Australia' then o.address.country
        when o.address.country = 'India' then o.address.country
        when o.address.country = 'Indonesia' then o.address.country
        when o.address.country = 'Thailand' then o.address.country
        else 'Others'
      end country,
      round(sum(o.totals.grossRevenue)) gross
  FROM
      [dwh.orders] o
  WHERE
      o.isValid AND date(o.createdAt) >= DATE(STRFTIME_UTC_USEC(CURRENT_DATE(), '%Y-%m-01')) AND date(o.createdAt) < date(CURRENT_DATE())
  GROUP BY
      date, country
) b ON a.country = b.country
WHERE
    b.date <= a.date
GROUP BY
    Date, Country
ORDER BY
    Date, Country