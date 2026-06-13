import { Link } from 'react-router-dom'

const devtoolsItems = [
  {
    title: 'Elements',
    text: 'Inspect HTML, hidden attributes, data-* markers, comments, and invisible page fragments.',
  },
  {
    title: 'Console',
    text: 'Look for client-side messages and run small JavaScript snippets while testing browser-only clues.',
  },
  {
    title: 'Network',
    text: 'Watch API calls, response bodies, status codes, request headers, and methods used by the app.',
  },
  {
    title: 'Application / Storage',
    text: 'Review cookies, localStorage, sessionStorage, and other browser-side traces.',
  },
]

const conceptItems = [
  'Change query parameters and compare responses.',
  'Try nearby object IDs when a route accepts an identifier.',
  'Inspect response headers, not only response bodies.',
  'Read public files such as robots.txt, humans.txt, and static assets.',
  'Test whether an endpoint behaves differently with GET, POST, or PUT.',
  'Edit JSON request fields when working with isolated API labs.',
]

export default function Learn() {
  return (
    <div className="learn-page">
      <section className="page-heading learn-hero">
        <p className="eyebrow">Operator Training</p>
        <h1>Learn the CTF Workflow</h1>
        <p>
          Hawkins Shadow Protocol is built for practice. Use this page as a field guide for safe,
          beginner-friendly techniques that help you understand how web, API, recon, frontend,
          encoding, and crypto challenges are usually solved.
        </p>
        <div className="hero-actions">
          <Link className="btn btn-primary" to="/challenges">Open Challenges</Link>
          <Link className="btn btn-ghost" to="/submit">Submit a Flag</Link>
        </div>
      </section>

      <section className="learn-section panel">
        <div>
          <p className="eyebrow">Step 01</p>
          <h2>Basic solving loop</h2>
          <p>
            Every challenge is a small investigation. Start with the description, read the hint,
            observe the target, test one idea at a time, then submit the recovered flag.
          </p>
        </div>
        <ol className="learn-steps">
          <li>Read the title, category, description, difficulty, and hint.</li>
          <li>Identify the likely technique: inspect, decode, change a parameter, or call an API.</li>
          <li>Use the browser or curl to observe the response carefully.</li>
          <li>Recover a flag that looks like the event flag format.</li>
          <li>Submit it once, then move to the next challenge.</li>
        </ol>
      </section>

      <section className="learn-section">
        <div className="page-heading compact-heading">
          <p className="eyebrow">Browser Toolkit</p>
          <h2>DevTools areas to check</h2>
          <p>
            Browser DevTools are enough for many beginner CTF tasks. Open them with right-click
            Inspect, or with your browser shortcut.
          </p>
        </div>
        <div className="grid two learn-card-grid">
          {devtoolsItems.map((item) => (
            <article className="panel learn-card" key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="learn-section panel">
        <div className="learn-split">
          <div>
            <p className="eyebrow">Terminal Toolkit</p>
            <h2>curl basics</h2>
            <p>
              curl is useful when you need to see headers, change methods, or send JSON without
              relying on the browser address bar.
            </p>
          </div>
          <div className="terminal-card" aria-label="curl command examples">
            <pre><code>{`curl http://localhost:5000/path
curl -i http://localhost:5000/path
curl -X POST http://localhost:5000/path
curl -X PUT http://localhost:5000/path
curl -X POST http://localhost:5000/api/path \\
  -H "Content-Type: application/json" \\
  -d '{"role":"guest"}'`}</code></pre>
          </div>
        </div>
      </section>

      <section className="learn-section">
        <div className="page-heading compact-heading">
          <p className="eyebrow">Core Concepts</p>
          <h2>What to practice</h2>
          <p>
            These are common CTF habits. They do not give away exact answers, but they help you
            choose the right direction when a challenge feels quiet.
          </p>
        </div>
        <div className="grid three">
          {conceptItems.map((item) => (
            <article className="panel mini-learn-card" key={item}>
              <span className="learn-dot" aria-hidden="true" />
              <p>{item}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="learn-section panel">
        <p className="eyebrow">Encoding and Crypto</p>
        <h2>Encoding is not encryption</h2>
        <p>
          Many beginner challenges use reversible transformations. Base64 stores data in a safe
          text format, hex represents bytes, and ROT/Caesar shifts letters. If a payload looks
          structured, try identifying the layer before assuming it is encrypted.
        </p>
        <div className="terminal-card spaced-terminal">
          <pre><code>{`Base64 example: SGVsbG8=
Hex example: 48 65 6c 6c 6f
ROT13 example: synt -> flag`}</code></pre>
        </div>
      </section>

      <section className="learn-section panel warning-panel">
        <p className="eyebrow">Safety Boundary</p>
        <h2>Stay inside the training range</h2>
        <p>
          Only test this CTF site and its intentionally vulnerable lab areas. Do not attack Render,
          GitHub, third-party services, real login systems, or infrastructure outside the event.
        </p>
        <ul className="learn-list">
          <li>Use the challenge board, public assets, and isolated training routes.</li>
          <li>Do not brute force real authentication or platform accounts.</li>
          <li>Do not run destructive scans or denial-of-service tests.</li>
          <li>When in doubt, stop and ask an organizer.</li>
        </ul>
      </section>
    </div>
  )
}
