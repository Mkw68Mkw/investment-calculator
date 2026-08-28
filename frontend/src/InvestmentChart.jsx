import { useMemo } from 'react'
import { defineChart, lineY } from '@tanstack/charts'
import { scaleLinear } from '@tanstack/charts/scales/linear'
import { colorLegend } from '@tanstack/charts/legend'
import { crosshair } from '@tanstack/charts/crosshair'
import { tooltip } from '@tanstack/charts/tooltip'
import { Chart } from '@tanstack/charts/react'

const PORTFOLIO_VALUE = 'Portfolio Value'
const INVESTED_CAPITAL = 'Invested Capital'
const RENDITE = 'Rendite'

const chfCompact = new Intl.NumberFormat('de-CH', {
  style: 'currency',
  currency: 'CHF',
  notation: 'compact',
  maximumFractionDigits: 1,
})

const chfFull = new Intl.NumberFormat('de-CH', {
  style: 'currency',
  currency: 'CHF',
  maximumFractionDigits: 0,
})

function cssVar(name, fallback) {
  if (typeof window === 'undefined') return fallback
  const value = getComputedStyle(document.documentElement)
    .getPropertyValue(name)
    .trim()
  return value || fallback
}

const monthToYear = (month) => Math.round(month / 12)
const rendite = (row) => row.value - row.invested

function yearTickValues(maxMonth) {
  const years = Math.round(maxMonth / 12)
  const step = [1, 2, 5, 10, 20, 25, 50, 100].find((s) => years / s <= 8) ?? 100
  const values = []
  for (let year = 0; year <= years; year += step) {
    values.push(year * 12)
  }
  return values
}

function InvestmentChart({ data }) {
  const definition = useMemo(() => {
    const valueColor = cssVar('--accent', '#2f6fed')
    const investedColor = cssVar('--text-muted', '#5c6b7a')
    const renditeColor = cssVar('--gain', '#f59e0b')
    const lastMonth = data.length > 0 ? data[data.length - 1].month : 0

    return defineChart({
      marks: [
        lineY(data, {
          x: 'month',
          y: 'invested',
          key: 'month',
          color: () => INVESTED_CAPITAL,
          strokeWidth: 1.75,
          strokeDasharray: '6 4',
        }),

        lineY(data, {
          x: 'month',
          y: 'value',
          key: 'month',
          color: () => PORTFOLIO_VALUE,
          strokeWidth: 3,
        }),

        crosshair({
          x: { label: { format: (month) => `Jahr ${monthToYear(month)}` } },
          y: false,
          strokeDasharray: '4 4',
        }),
      ],

      scales: {
        x: {
          scale: scaleLinear,
          axis: {
            label: 'Jahre',
            ticks: {
              values: yearTickValues(lastMonth),
              format: (month) => String(monthToYear(month)),
            },
          },
        },

        y: {
          scale: scaleLinear,
          nice: true,
          grid: true,
          axis: {
            ticks: {
              format: (value) => chfCompact.format(value),
            },
          },
        },
      },

      color: {
        domain: [PORTFOLIO_VALUE, INVESTED_CAPITAL],
        range: [valueColor, investedColor],
        legend: colorLegend({ placement: 'bottom' }),
      },

      focus: 'group-x',
      maxFocusDistance: Number.POSITIVE_INFINITY,

      tooltip: {
        use: tooltip,
        sort: 'color-domain',
        // Place the box in the emptier vertical half: if the focused point
        // sits low, anchor at the top edge; if it sits high, anchor at the
        // bottom edge. The placement fallback then flips into the free space.
        anchor: (points, { focus, plot }) => {
          const point = focus.primary ?? points[0]
          if (!point) return null
          const midY = plot.y + plot.height / 2
          const y = point.y > midY ? plot.y : plot.y + plot.height
          return { x: point.x, y }
        },
        placement: ['top', 'bottom'],
        offset: 12,
        content: (points) => {
          const first = points[0]
          const rows = points.map((point) => ({
            label: point.groupLabel,
            value: chfFull.format(point.yValue),
            color: point.color,
          }))

          if (first) {
            rows.push({
              label: RENDITE,
              value: chfFull.format(rendite(first.datum)),
              color: renditeColor,
            })
          }

          return {
            title: `Jahr ${monthToYear(first?.xValue ?? 0)}`,
            rows,
          }
        },
      },
    })
  }, [data])

  return (
    <Chart
      definition={definition}
      height={380}
      ariaLabel="Entwicklung des Portfolios"
    />
  )
}

export default InvestmentChart
