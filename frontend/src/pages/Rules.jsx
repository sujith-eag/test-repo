export default function Rules() {
  return (
    <section data-rules-gate="CTF{rules_gate_marker}">
      <div className="page-heading">
        <div className="eyebrow">Rules of Engagement</div>
        <h1>Event Rules</h1>
        <p>Keep the operation fair, safe, and focused on the intended Hawkins Shadow Protocol challenges.</p>
      </div>

      <div className="panel rules-list">
        <ul>
          <li>Only interact with this event site and challenge-related surfaces exposed by it.</li>
          <li>Do not attack Render, hosting infrastructure, databases directly, accounts, or unrelated services.</li>
          <li>Standard browser inspection, source review, headers, storage, encoding, and endpoint testing are allowed.</li>
          <li>Only attack or test the provided challenge routes, pages, and authorized lab endpoints.</li>
          <li>No brute forcing user accounts, login routes, or other participants.</li>
          <li>Do not share flags with other operators or teams.</li>
          <li>Duplicate correct submissions do not award extra points.</li>
          <li>Respect the event team and report platform issues responsibly.</li>
        </ul>
      </div>
    </section>
  )
}