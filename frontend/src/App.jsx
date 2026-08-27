import { useState } from 'react'

function App() {
  const [rj, setRj] = useState('')
  const [SK, setSK] = useState('')
  const [EM, setEM] = useState('')
  const [n, setN] = useState('')
  const [result, setResult] = useState(null)

  async function calculate() {
    const response = await fetch('http://127.0.0.1:8000/api/calculate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        rj: Number(rj) / 100,
        SK: Number(SK),
        EM: Number(EM),
        n: Number(n),
      }),
    })

    const data = await response.json()
    setResult(data)
  }

  return (
    <main className="app">
      <header className="app__header">
        <h1>Investment Calculator</h1>
        <p>Berechne den zukünftigen Wert deiner Anlage.</p>
      </header>

      <form
        className="calc-form"
        onSubmit={(e) => {
          e.preventDefault()
          calculate()
        }}
      >
        <label className="field">
          <span className="field__label">Jährliche Rendite (%)</span>
          <input
            type="number"
            step="0.1"
            placeholder="z. B. 8"
            value={rj}
            onChange={(e) => setRj(e.target.value)}
            required
          />
        </label>

        <label className="field">
          <span className="field__label">Startkapital (CHF)</span>
          <input
            type="number"
            step="100"
            min="0"
            placeholder="z. B. 40000"
            value={SK}
            onChange={(e) => setSK(e.target.value)}
            required
          />
        </label>

        <label className="field">
          <span className="field__label">Monatliche Einzahlung (CHF)</span>
          <input
            type="number"
            step="50"
            min="0"
            placeholder="z. B. 1000"
            value={EM}
            onChange={(e) => setEM(e.target.value)}
            required
          />
        </label>

        <label className="field">
          <span className="field__label">Anlagehorizont (Jahre)</span>
          <input
            type="number"
            step="1"
            min="1"
            placeholder="z. B. 40"
            value={n}
            onChange={(e) => setN(e.target.value)}
            required
          />
        </label>

        <button type="submit" className="btn">
          Berechnen
        </button>
      </form>

      {result && (
        <section className="result" aria-live="polite">
          <span className="result__label">Zukünftiger Wert</span>

          <strong className="result__value">
            {Number(result.total_future_value).toLocaleString('de-CH', {
              style: 'currency',
              currency: 'CHF',
            })}
          </strong>
        </section>
      )}
    </main>
  )
}

export default App