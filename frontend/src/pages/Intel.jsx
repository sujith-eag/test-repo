export default function Intel() {
  return (
    <section>
      <div className="page-heading">
        <div className="eyebrow">Mission Briefing</div>
        <h1>Hawkins Shadow Protocol Intel</h1>
        <p>
          A rogue signal has surfaced around Hawkins Lab-style systems: forgotten endpoints, exposed browser traces, encoded transmissions, and weak vault controls. Your objective is to recover protocol fragments and submit each confirmed flag. The theme is inspired by strange signals and gates, but all solves rely on cyber clues.
        </p>
      </div>

      <div className="grid">
        <div className="panel mission-panel">
          <h3>Objective</h3>
          <p>Investigate the provided challenge board and recover valid CTF flags.</p>
        </div>
        <div className="panel mission-panel">
          <h3>Allowed Scope</h3>
          <p>Use only this event site and the challenge surfaces it exposes. Standard web recon is allowed, but hosting infrastructure, accounts, and unrelated services are out of scope.</p>
        </div>
        <div className="panel mission-panel">
          <h3>Operator Notes</h3>
          <p>Browser DevTools, headers, source inspection, simple decoding, and careful input testing will help.</p>
        </div>
      </div>
    </section>
  )
}