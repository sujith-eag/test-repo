export default function Intel() {
  return (
    <section>
      <div className="page-heading">
        <div className="eyebrow">Mission Briefing</div>
        <h1>Shadow Protocol Intel</h1>
        <p>
          A rogue signal has surfaced across forgotten endpoints, exposed browser traces,
          encoded transmissions, and weak vault controls. Your objective is to recover
          protocol fragments and submit each confirmed flag.
        </p>
      </div>

      <div className="grid">
        <div className="panel mission-panel">
          <h3>Objective</h3>
          <p>Investigate the provided challenge board and recover valid CTF flags.</p>
        </div>
        <div className="panel mission-panel">
          <h3>Allowed Scope</h3>
          <p>Use the application pages and routes under <code>/vuln/*</code>. Do not attack infrastructure.</p>
        </div>
        <div className="panel mission-panel">
          <h3>Operator Notes</h3>
          <p>Browser DevTools, headers, source inspection, simple decoding, and careful input testing will help.</p>
        </div>
      </div>
    </section>
  )
}